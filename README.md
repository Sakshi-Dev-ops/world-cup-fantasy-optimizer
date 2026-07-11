# 🏆 World Cup Fantasy Optimization Engine

An advanced, cross-platform algorithmic tool designed to compute the mathematically optimal roster configuration for World Cup Fantasy football leagues. 

This project demonstrates a multi-language architecture: high-performance data processing and constraint solving handled via compiled **C++**, bound seamlessly to a modern, responsive web application via **Python & Streamlit**.

## 🚀 Key Features
* **C++ Core Engine:** Utilizes an optimized 0/1 Multi-Constraint Knapsack algorithm implemented using Dynamic Programming to respect strict budget limitations and country roster caps.
* **Predictive Analytics:** Implements a weighted trend formula factoring in recent performance form against historical baseline data.
* **Interactive UX:** Built-in interactive dashboard allowing real-time "What-If" scenario tracking, custom budget filtering, and beautiful visual budget allocation charts.

## 🛠️ Tech Stack & Architecture
* **Backend:** C++17 (Dynamic Programming, Memory-Safe Structs)
* **Frontend:** Python 3.x, Streamlit, Pandas
* **Interoperability:** `ctypes` foreign function interface

## 📦 Compilation & Setup
1. Compile the C++ shared library:
   ```bash
   # For Linux/macOS
   g++ -O3 -shared -fPIC -o liboptimizer.so optimizer.cpp
   
   # For Windows
   g++ -O3 -shared -o liboptimizer.dll optimizer.cpp
