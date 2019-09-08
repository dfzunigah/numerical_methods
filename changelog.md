# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- :soon: A plotting function for Newton-Rapshon method.
- :soon: Minor appearance stuff. 

## [0.0.2] (2019/09/08)
### Added
- Added Newton-Rapshon method and its theory.
- Added secant method and its theory.
- Added bisection method and its theory.
- Added Regula Falsi method and its theory.
- A tabulating function for double-point methods (bisection, secant, regula_falsi)
- A plotting function for fixed point method.
- A plotting function for root-finding methods (bisection, secant, regula_falsi), except Newton-Rapshon.

### Fixed
- Fixed a bug which was rendering the table for the Newton-Raphson method in the wrong order.
- Examples of some background functions weren't right.
- Regula Falsi method was yielding a wrong result.

### Removed
- User friendly user input.

## [0.0.1] (2019/09/06)
### Added
- Theory of the fixed point iteration method.
- Foolproof fixed point algorithm.

### Changed
- Separated background functions in a different file.
- All own functions are now documented.

### Removed
- Non-foolproof own fixed point algorithms.
