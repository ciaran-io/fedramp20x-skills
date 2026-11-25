# Certification classes (A, B and C)

The skills cover FedRAMP 20x Class A, Class B and Class C. Class D is out of scope. The class comes from `class` in `engagement.json` (see `engagement-folder.md`). Every deliverable states the class in its envelope, and `check_deliverable.py` checks rule sources against that class.

Read the class differences from the pinned rules data at run time. Do not work from this page alone:

```
python scripts/frmr.py compare --class b --to c   # Class B against Class C
python scripts/frmr.py compare --class a --to c   # Class A against Class C
python scripts/frmr.py rules --class a --affects Providers
python scripts/frmr.py ksis --class a
```

`compare` lists the rules and KSIs that apply at one class only, the changed force and timeframes, the rules whose statement text differs (named, not shown) and the KSIs that are optional at the class. Cite the rule ID for every class difference you use.

## Pass the class to every script

- `frmr.py rules`, `ksis`, `show`, `search` and `lint`: `--class a`, `--class b` or `--class c`.
- `incident_timeline.py --rating N --class a`: the PAIN timeframes differ by class. The output gives the force of each rule at the class (`rule_force`).
- `scn_timeline.py notices --class a`: the script stops when a Significant Change Notification rule does not apply at the class. Say so in the deliverable and ask the consultant how the client handles the change.

## Class B

At FRMR 2026.11.02.01 (commit `64fa769`), Class B has the same 157 provider rules as Class C.

- Twelve rules change force or timeframe: CCM-QTR-MTG, CMU-CSO-UVM, CPO-CSX-CPM, FRC-CSX-VVK, SDR-CSX-KMT, VDR-TFR-MVX, VDR-TFR-PCD, VDR-TFR-PDD, VDR-TFR-PSD, VER-TFR-EVU, VER-TFR-IRI and VER-TFR-MRH.
- IEC-CSO-IIR, IEC-CSO-OIR, IEC-CSO-FIR and VDR-TFR-PVR have their own PAIN timeframes at Class B.
- Other rules differ in statement text only. `compare` names them.
- Five KSIs are optional at Class B: KSI-CNA-EIS, KSI-MLA-ALA, KSI-SVC-PRR, KSI-SVC-RUD and KSI-SVC-VCM. An optional KSI that the client does not address is not a gap. Record it as optional with the client's decision, and rate a gap only when the client says it addresses the KSI.

## Class A

Class A uses lists, not subset applicability, to say which other rules apply:

| List | Force at Class A | `frmr.py` field |
|---|---|---|
| FRC-CLA-MFR | MUST, with the artifacts or mapping in the Certification Package | `class_a_list`, `class_a_force` |
| FRC-CLA-RFR | SHOULD (if applicable) | same |
| FRC-CLA-OFR | MAY (if applicable) | same |

- `frmr.py rules --class a` adds every rule named in the three lists, each marked with its list and force. Use `class_a_force` as the force at Class A. Where the rule record has no Class A variant, the list applies the rule as written.
- FRC-CLA-MFR also names KSIs. `frmr.py ksis --class a` marks them with `class_a_list`. The data holds 41 KSIs at Class A; the five KSIs optional at Class B do not apply.
- A Class A certification needs a certification from an approved alternative framework, completed within the past 12 months (FRC-CLA-ASF), and the materials from that assessment (FRC-CLA-EAM). The `20x-class-a-readiness` skill checks these.
- Independent verification and validation of the package is optional (FRC-CLA-IVV).
- A SHOULD or MAY rule that the client does not address is not a gap. Report it as a recommendation, with the list ID as the criterion.

## Ratings by class

Rate a finding against the force the rule has at the client's class. A MUST at Class C can be a SHOULD at Class B or a MAY at Class A. When the class is not recorded, stop and ask; do not assume Class C.
