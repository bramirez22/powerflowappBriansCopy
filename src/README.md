# Source Structure Suggestion

Suggested modules:

- `parser/` - text input parsing for bus/branch/generator data
- `models/` - data structures and per-unit normalization
- `ybus/` - admittance matrix construction
- `powerflow/gs/` - Gauss-Seidel implementation
- `powerflow/nr/` - Newton-Raphson implementation
- `shortcircuit/` - fault and symmetrical component analysis
- `ui/` - web or desktop user interface
- `export/` - CSV/TXT output formatting
