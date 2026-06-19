# P-HWE-19: Ingress Protection (IP) Test Plan (ME)

#### Description
An IP-rating verification plan (e.g. IP54) covering dust and water test methods, sample prep, and acceptance — critical for restaurant/industrial duty cycles.

#### Information to collect (ask the user before generating)
1. Target IP rating (IP54, IP65, ...)?
2. Sealed openings (USB-C, speaker, mic, buttons, seams)?
3. Test methods per IEC 60529 for the rating?
4. Sample condition (new, post-drop, aged gaskets)?
5. Functional check after exposure?

#### Suggested template
Structure:
- Rating + the two digits' meaning; methods per IEC 60529
- Seal map: each opening and its sealing approach
- Test sequence: dust then water (or per standard), durations
- Acceptance: no harmful ingress + functional pass
- Aging/robustness: test after drop and gasket aging

Confirm the structure before generating.

#### File-generation prompt
```
Create a Ingress Protection (IP) Test Plan (ME).

CONTEXT:
- Rating: [IPxx] — Openings: [USB-C/speaker/buttons/seams]
- Sample condition: [new/post-drop/aged]

FORMAT:
- Method table per IEC 60529 (test, duration, criteria)
- Seal map; acceptance definition
- Post-exposure functional check

RULES: reference IEC 60529 method numbers for the claimed rating [verify with lab]; require a functional check after exposure, not just visual.
```

---
✍️ Author: Brian H. Doan
