# Class A readiness tests

Apply each test with the rules data at Class A (`scripts/frmr.py show <ID> --class a`). Cite the rule ID; do not copy statement text.

| Test | Rule | Check | Finding when it fails |
|---|---|---|---|
| R1 | FRC-CLA-ASF | The framework is one the rule lists | High: no approved framework |
| R2 | FRC-CLA-ASF | The certification or equivalent process, with any independent assessment, was completed within 12 months before the planned submission date. Name the date used as completion and why | High if outside the window; a decision question if the completion date is unclear |
| R3 | FRC-CLA-ASF | The window stays open long enough for the planned submission and review. Give the date it closes | Observation when it closes within 3 months of the planned submission |
| R4 | FRC-CLA-EAM | Each material the rule names for the framework is in the inputs | High for a missing material |
| R5 | FRC-CLA-EAM | Each material is current: a bridge or gap letter covers the time since the report period ended; the next report has an estimated date | Moderate |
| R6 | FRC-CLA-ASF, MAS-CSO-IIR | The assessed scope covers the offering and every information resource in the scope record | Moderate for a part outside the assessed scope; High if the core service is outside it |
| R7 | FRC-CLA-MFR and the FRC-CLA subset | Each mandatory rule and KSI maps to client material, with the Class A force and timeframes | Rate by `finding-ratings.md` against the MUST force |
| R8 | FRC-CLA-RFR, FRC-CLA-OFR, FRC-CLA-IVV | Each recommended or optional rule has a recommendation | Never a gap |
| R9 | All | `frmr.py lint --class a` reports no error and no ID that does not apply at Class A | Fix before validation |
