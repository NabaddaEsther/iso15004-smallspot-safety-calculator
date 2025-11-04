**Author**
Esther Nabadda
ACH Laboratory, Eye Clinic UKB

**Overview**
This repository provides a Python implementation of the ISO 15004-2:2025 retinal safety evaluation for ophthalmic instruments emitting pulsed visible light between 400–500 nm.
The calculator is optimized for small-spot retinal exposures (≤ 0.03 mm), as defined for immobilized-eye conditions such as in confocal or scanning ophthalmoscopes.
It computes both thermal and photochemical retinal exposure limits and determines which mechanism governs the safety margin under a given set of parameters.

**Features**
-Simple, interactive console interface
-Accepts intuitive metric prefixes (u, m, n, p) for input power values
-Implements ISO 15004-2:2025 exposure rules for pulsed and continuous sources
-Distinguishes between thermal and blue-light (photochemical) hazards
-Uses fixed 0.03 mm retinal diameter per ISO Table 6 for immobilized-eye cases
-Incorporates wavelength-dependent spectral weighting functions:
  R(λ) — retinal thermal weighting
  B(λ) — blue-light photochemical weighting
-Applies time-dependent substitution rules for R(λ):
  If pulse duration < 10⁻¹¹ s → set R(λ)=1 for R < 1
  If exposure > 10 s → set R(λ)=1 for R > 1

**How to Use**
Run the calculator from a terminal: python ISO_Smallspot_Safety_Calculator.py

**Example**
Enter wavelength (nm): 450  
Enter exposure duration (s): 0.1  
Enter power at pupil (u, m, n, or p suffix): 5u  

**Output**
Calculated thermal and photochemical radiant exposures
Identified governing hazard mechanism
Margin relative to ISO Group 1 limit
Safe stationary-beam exposure time (immobilized eye)

**Intended Use**
This tool was developed for research and laboratory validation of small-spot ophthalmic light sources according to ISO 15004-2:2025.
It is intended for engineering and safety assessment purposes within controlled lab settings and should not replace certified ISO compliance testing.

License
MIT License © 2025 Esther Nabadda, ACH Laboratory, Eye Clinic UKB
