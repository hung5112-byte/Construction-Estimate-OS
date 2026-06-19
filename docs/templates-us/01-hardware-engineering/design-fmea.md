# P-HWE-29: Design FMEA (DFMEA)

#### Description
A design-level failure-mode-and-effects analysis — systematically rates failure modes by severity/occurrence/detection and drives design actions on the top risks.

#### Information to collect (ask the user before generating)
1. Product/subsystem scope of the DFMEA?
2. Functions and their failure modes to consider?
3. Severity/occurrence/detection scale in use (1-10)?
4. RPN or AP (action-priority) threshold for action?
5. Known field failures to seed the analysis?

#### Suggested template
Structure:
- Function -> potential failure mode -> effect (severity)
- Causes (occurrence) + current controls (detection)
- S/O/D ratings + RPN or AP
- Top risks above threshold -> recommended actions + owners
- Re-rating after actions

Confirm the structure before generating.

#### File-generation prompt
```
Create a Design FMEA (DFMEA).

CONTEXT:
- Scope: [subsystem] — Scale: [1-10] — Threshold: [RPN/AP]
- Seed failures: [field data]

FORMAT:
- DFMEA table: function, failure mode, effect(S), cause(O), control(D), RPN/AP
- Action list for items above threshold (owner, due)
- Re-rated RPN/AP after actions

RULES: every failure mode above the action threshold must have an assigned action and owner; severity ratings for safety/payment effects are justified, not guessed.
```

---
✍️ Author: Brian H. Doan
