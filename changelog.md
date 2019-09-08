# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] (2019/09/08)
### Added
- **bg_functions:** A plotting function for Newton-Rapshon method.
- **1 - Rootfinding_methods:** Minor appearance stuff. 

### Fixed
- **bg_functions:** Plotting functions didn't worked well if the result was a negative number.

## [0.0.2] (2019/09/07)
### Added
- **1 - Rootfinding_methods:** Added Newton-Rapshon method and its theory.
- **1 - Rootfinding_methods:** Added secant method and its theory.
- **1 - Rootfinding_methods:** Added bisection method and its theory.
- **1 - Rootfinding_methods:** Added Regula Falsi method and its theory.
- **bg_functions:** A tabulating function for double-point methods (bisection, secant, regula_falsi)
- **bg_functions:** A plotting function for fixed point method.
- **bg_functions:** A plotting function for root-finding methods (bisection, secant, regula_falsi), except Newton-Rapshon.

### Fixed
- **bg_functions:** Fixed a bug which was rendering the table for the Newton-Raphson method in the wrong order.
- **1 - Rootfinding_methods:** Examples of some background functions weren't right.
- **1 - Rootfinding_methods:** Regula Falsi method was yielding a wrong result.

### Removed
- **1 - Rootfinding_methods:** User friendly user input. But now it's easier to modify entries.

## [0.0.1] (2019/09/06)
### Added
- **1 - Rootfinding_methods:** Theory of the fixed point iteration method.
- **1 - Rootfinding_methods:** Foolproof fixed point algorithm.

### Changed
- Separated background functions in a different file.
- All own functions are now documented.

### Removed
- Non-foolproof own fixed point algorithms.
