# 🏆 World Cup Fantasy Optimization Engine

An advanced, cross-platform algorithmic tool designed to compute the mathematically optimal roster configuration for World Cup Fantasy football leagues. 

This project demonstrates a multi-language architecture: high-performance data processing and constraint solving handled via compiled C++, bound seamlessly to a modern, responsive web application via Python & Streamlit.

---

## 🚀 Key Features

* **C++ Core Engine:** Utilizes an optimized 0/1 Multi-Constraint Knapsack algorithm implemented using Dynamic Programming to respect strict budget limitations and country roster caps (maximum of 3 assets from any single country federation).
* **Predictive Analytics:** Implements a customizable weighted trend formula profiling recent performance form parameters directly against historical baseline metrics.
* **Interactive UX:** Built-in interactive dashboard allowing real-time "What-If" scenario tracking, custom budget filtering, tactical grid layout modules, and beautiful visual budget allocation charts.

---

## 🛠️ Tech Stack & Architecture

* **Backend:** C++17 (Dynamic Programming, Memory-Safe Structs, Explicit Pointers)
* **Frontend:** Python 3.x, Streamlit, Pandas
* **Interoperability Layer:** `ctypes` foreign function interface (FFI) for direct memory mapping

### Data System Topology
+---------------------------+        Data Marshaling (ctypes)       +----------------------------+
|   Python Presentation     |  --------------------------------->  |   Compiled C++ Core        |
|  Streamlit State Layer    |                                      |  Multi-Dim Knapsack Solver |
|  (User Input Telemetry)   |  <---------------------------------  | (Positional & Country Caps)|
+---------------------------+       Native Memory Unpacking        +----------------------------+


---

## 📦 Compilation & Setup

### 1. Compile the C++ Shared Library
Execute the native compilation sequence within your shell terminal to match your deployment environment's host architecture dependencies:

```bash
# For Linux/macOS
g++ -O3 -shared -fPIC -o liboptimizer.so optimizer.cpp

# For Windows
g++ -O3 -shared -o liboptimizer.dll optimizer.cpp
