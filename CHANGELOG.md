# Changelog

## [1.1.3] - 2026-08

### Fixed
- Corrected state-class handling for annual, monthly and total self-consumed energy entities.
- Removed the incorrect `total_increasing` declaration for values that can decrease when reported by the Riello portal.

### Verified
- 39 entities operating correctly.
- Values verified against the Riello web portal.
- Login and updates stable.
- Grafana import stable.
- Owner and revision diagnostic entities verified.
- Tested with Home Assistant Core 2026.8.3.

## [1.1.2] - 2026-08

### Added
- Diagnostic revision entity showing the installed integration revision.
- Diagnostic owner entity.

## [1.1.1] - 2026-08

### Added
- Owner information exposed as a diagnostic entity.
