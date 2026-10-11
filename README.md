# Riello RS Monitoring

Custom Home Assistant integration for monitoring a Riello RS Monitoring installation.

## Stable release

**v1.1.3**

This is the tested baseline of the integration supplied for this repository.

### Verified with

- Home Assistant Core 2026.10.1
- 39 working Riello entities/sensors in the tested installation
- Riello web values checked against Home Assistant
- Grafana data import verified
- Login and updates verified
- Diagnostic owner entity
- Diagnostic revision entity

### v1.1.3

- Corrected the state-class handling of annual, monthly and total self-consumed energy values.
- These entities no longer use `total_increasing`, because the Riello portal can legitimately report a lower value than the previous reading.
- Existing values are passed through without artificially forcing them to increase.

## Installation

Copy `custom_components/riello_rs` into `/config/custom_components/riello_rs/` and restart Home Assistant. Configure the integration through Home Assistant.

## Note

This is a custom integration and is not an official Riello integration.
