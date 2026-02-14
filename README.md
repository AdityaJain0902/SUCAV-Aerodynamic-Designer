# ✈️ SUCAV Conceptual Design Tool

### A Python framework for the preliminary aerodynamic analysis of Supersonic Unmanned Combat Aerial Vehicles.

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Status](https://img.shields.io/badge/Status-Prototype-orange)
![Domain](https://img.shields.io/badge/Domain-Aerospace_Engineering-red)

## 📖 Overview
This tool streamlines the conceptual design phase for SUCAVs by automating the calculation of aerodynamic coefficients. Unlike standard linear solvers, this program integrates **non-linear aerodynamic plots** and empirical formulas specific to the supersonic flight regime, allowing for higher-fidelity performance estimation in the early design stages.

## ⚙️ Key Features
* **Parametric Input:** Accepts user-defined geometry (Wing area, Aspect Ratio, Sweep angle, Mach number, etc.).
* **Non-Linear Data Handling:** Utilizes digitized historical data and non-linear interpolation to estimate Lift ($C_L$) and Drag ($C_D$) coefficients where standard linear theory breaks down.
* **Supersonic Regime Analysis:** Specifically tuned for compressible flow equations relevant to Mach 1.2+.
* **Performance Outputs:** Generates detailed reports on Lift-to-Drag ratios ($L/D$), static margin, and range capabilities.

## 🧮 How It Works
The code follows a standard conceptual design workflow:
1.  **Input Vector:** User defines the mission profile and constraints.
2.  **Geometry Sizing:** Initial sizing based on constraint analysis.
3.  **Aerodynamic Solver:**
    * Calculates Wave Drag using cross-sectional area distribution.
    * Calculates Friction Drag using component build-up method.
    * Interpolates non-linear stability derivatives.
4.  **Output:** Plots of $C_L$ vs $\alpha$ and Drag Polars.

## 🛠️ Tech Stack
* **Python:** Core logic and calculation engine.
* **NumPy/SciPy:** Handling arrays and interpolation of non-linear datasets.
* **Matplotlib:** Visualizing the drag polars and performance envelopes.

## 🚀 Getting Started
```bash
# Clone the repository
git clone [https://github.com/YourUsername/SUCAV-Aerodynamic-Designer.git](https://github.com/YourUsername/SUCAV-Aerodynamic-Designer.git)

# Install dependencies
pip install numpy matplotlib scipy

# Run the analysis
python main_design.py
