# Asset inventory (test input)

> TEST INPUT. Seeded faults for the 20x-scope-review tests.

| ID | System | Holds agency data | Notes |
|---|---|---|---|
| A1 | Web application | Yes: agency user records | Runs in the production cloud account |
| A2 | Database | Yes | |
| A3 | Analytics service (third party) | Usage metrics with agency user IDs | Run by another company |
| A4 | Build server | No | Deploys A1 |
| A5 | Ticketing tool | No, by policy | Support staff are told not to paste agency data |
