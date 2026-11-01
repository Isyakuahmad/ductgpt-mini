"""Natural-language alloy screening agent with OpenAI-compatible tool calling."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

try:
    from src.screen import screen_alloys
except ModuleNotFoundError:  # Direct-script fallback
    from screen import screen_alloys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "sample_W_alloys.csv"
TOOL_NAME = "screen_alloys"

TOOLS = [{
    "type": "function",
    "function": {
        "name": TOOL_NAME,
        "description": (
            "Screen the local tungsten-alloy dataset using Pugh ratio, "
            "minimum bulk modulus, and required chemical elements. Use this "
            "when the user asks to find, filter, or compare alloy candidates."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "max_pugh": {
                    "type": "number",
                    "description": "Maximum allowed Pugh ratio (G/K); lower values are used as a ductility heuristic.",
                    "default": 0.57,
                },
                "min_K": {
                    "type": ["number", "null"],
                    "description": "Minimum bulk modulus K in GPa; null means no minimum.",
                },
                "elements": {
                    "type": ["array", "null"],
                    "items": {"type": "string"},
                    "description": "Element symbols that must all occur in the alloy formula, e.g. [Ta].",
                },
            },
            "required": ["max_pugh", "min_K", "elements"],
            "additionalProperties": False,
        },
    },
}]


def run_screen_tool(arguments: dict[str, Any], data_path: Path) -> pd.DataFrame:
    """Validate tool arguments and run the deterministic local screening function."""
    allowed = {"max_pugh", "min_K", "elements"}
    unexpected = set(arguments) - allowed
    if unexpected:
        raise ValueError(f"Unexpected screen_alloys arguments: {sorted(unexpected)}")

    max_pugh = float(arguments.get("max_pugh", 0.57))
    min_k = arguments.get("min_K")
    min_k = None if min_k is None else float(min_k)
    elements = arguments.get("elements")
    if elements is not None:
        if not isinstance(elements, list) or not all(
            isinstance(item, str) and item.strip() for item in elements
        ):
            raise ValueError("'elements' must be a list of non-empty symbols or null.")
        elements = [item.strip() for item in elements]

    data = pd.read_csv(data_path)
    # The public tool schema calls this min_K; screen.py calls it min_bulk_modulus.
    return screen_alloys(
        data,
        max_pugh=max_pugh,
        min_bulk_modulus=min_k,
        elements=elements,
    )


def build_client() -> tuple[OpenAI, str]:
    load_dotenv(ROOT / ".env")
    base_url = os.getenv("OLLAMA_BASE_URL", "").strip()
    model = os.getenv("LLM_MODEL", "").strip()

    if base_url:
        client = OpenAI(
            base_url=base_url.rstrip("/"),
            api_key=os.getenv("OPENAI_API_KEY") or "ollama",
        )
        return client, model or "llama3.1"

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set OPENAI_API_KEY for OpenAI, or set OLLAMA_BASE_URL and "
            "LLM_MODEL to use an Ollama model."
        )
    return OpenAI(api_key=api_key), model or "gpt-4o-mini"


def main() -> int:
    if len(sys.argv) < 2 or not " ".join(sys.argv[1:]).strip():
        print('Usage: python src/llm_agent.py "Find ductile W alloys with Ta"', file=sys.stderr)
        return 2

    load_dotenv(ROOT / ".env")
    query = " ".join(sys.argv[1:]).strip()
    data_path = Path(os.getenv("ALLOY_DATA_PATH", str(DEFAULT_DATA))).expanduser()
    if not data_path.is_absolute():
        data_path = (Path.cwd() / data_path).resolve()
    if not data_path.is_file():
        print(f"Dataset not found: {data_path}", file=sys.stderr)
        return 2

    try:
        client, model = build_client()
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "You are DuctGPT-Mini, an assistant for exploratory tungsten-alloy "
                    "screening. Convert screening requests into screen_alloys arguments. "
                    "min_K means minimum bulk modulus in GPa; all listed elements must "
                    "occur in the formula. A low Pugh ratio is an empirical heuristic, "
                    "not proof of ductility. Never invent results or describe synthetic "
                    "fixture values as experimental measurements. Explain limitations."
                ),
            },
            {"role": "user", "content": query},
        ]

        results = pd.DataFrame()
        tool_was_called = False
        for _ in range(4):
            response = client.chat.completions.create(
                model=model, messages=messages, tools=TOOLS, tool_choice="auto"
            )
            message = response.choices[0].message
            assistant_message: dict[str, Any] = {
                "role": "assistant",
                "content": message.content,
            }
            if message.tool_calls:
                assistant_message["tool_calls"] = [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in message.tool_calls
                ]
            messages.append(assistant_message)

            if not message.tool_calls:
                print(message.content or "The model returned no text response.")
                print("\nScreening results:")
                if tool_was_called:
                    print(results.to_string(index=False) if not results.empty else "(No matching alloys.)")
                else:
                    print("(No screening tool was called; no result table is available.)")
                return 0

            for call in message.tool_calls:
                if call.function.name != TOOL_NAME:
                    output: dict[str, Any] = {"error": f"Unsupported tool: {call.function.name}"}
                else:
                    try:
                        arguments = json.loads(call.function.arguments or "{}")
                        if not isinstance(arguments, dict):
                            raise ValueError("Tool arguments must be a JSON object.")
                        results = run_screen_tool(arguments, data_path)
                        tool_was_called = True
                        output = {
                            "row_count": len(results),
                            "columns": list(results.columns),
                            "results": results.to_dict(orient="records"),
                            "data_source": str(data_path),
                        }
                    except (json.JSONDecodeError, TypeError, ValueError, OSError) as exc:
                        output = {"error": str(exc)}
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(output, default=str),
                })

        print("Error: the model reached the maximum number of tool-calling rounds.", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
