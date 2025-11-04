**ISO 15004-2:2025 Small-Spot Retinal Safety Calculator**

**Author**
Esther Nabadda
ACH Laboratory, Eye Clinic UKB

**Overview**
This repository contains a Python-based implementation of the ISO 15004-2:2025 retinal safety evaluation for ophthalmic instruments operating in the 400–500 nm wavelength range.
The tool is designed for small-spot retinal exposure conditions (≤ 0.03 mm), representative of immobilized-eye configurations such as confocal or scanning ophthalmoscopes.
It provides a structured way to evaluate both thermal and photochemical retinal exposure limits and determine which limit governs under specific exposure parameters.

**Features**
Interactive console interface for direct input
Accepts power inputs with metric suffixes (u, m, n, p)
Implements the ISO 15004-2:2025 exposure framework for pulsed and time-limited instruments
Evaluates both thermal and blue-light photochemical hazards
Fixed 0.03 mm retinal aperture for immobilized-eye calculations
Includes wavelength-dependent weighting functions:
  R(λ) — retinal thermal weighting
  B(λ) — blue-light photochemical weighting
Automatically applies substitution rules for R(λ):
  If pulse duration < 10⁻¹¹ s → use R(λ) = 1 where R < 1
  If exposure > 10 s → use R(λ) = 1 where R > 1

**Usage**
Run the calculator from a terminal window:
python ISO_Smallspot_Safety_Calculator.py

**Example**
Enter wavelength (nm): 450  
Enter exposure duration (s): 0.1  
Enter power at pupil (u, m, n, or p suffix): 5u  

Output
The program returns:
Calculated thermal and photochemical radiant exposures
The governing hazard (thermal or photochemical)
Margin relative to the ISO Group 1 exposure limit
Estimated safe exposure duration for an immobilized eye

**Purpose**
This calculator was developed for research use within ACH Laboratory, Eye Clinic UKB, to support design verification and risk assessment of ophthalmic laser systems.
It is intended for internal validation and educational purposes and should not be used as a substitute for formal ISO certification testing.

**License**
MIT License © 2025 Esther Nabadda, ACH Laboratory, Eye Clinic UKB
