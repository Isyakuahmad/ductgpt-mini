# DuctGPT-Mini 🧪⚛️

> A DIY, open-source reimplementation of DuctGPT-style natural-language
> screening for tungsten-based fusion alloys.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-research%20prototype-orange)

## 🎯 What This Is

DuctGPT-Mini lets you **query tungsten alloy candidates in plain English**
("find ductile W alloys with Ta, bulk modulus above 250 GPa") and get
ranked results using data from the Materials Project, a machine-learning
property predictor, and an LLM tool-calling layer.

It is inspired by [Ames National Laboratory's DuctGPT], which is not
publicly available. This repo reconstructs the core workflow with
free, open tools.

## ✨ Features

- 🔍 **Natural-language alloy screening** via LLM function calling
- 📊 **Pugh-ratio ductility proxy** computed automatically
- 🤖 **RandomForest / ALIGNN** property prediction
- 🌐 **Optional Streamlit UI** for interactive exploration
- 🧪 **Reproducible** — one command regenerates the dataset

## 🏗️ Architecture
