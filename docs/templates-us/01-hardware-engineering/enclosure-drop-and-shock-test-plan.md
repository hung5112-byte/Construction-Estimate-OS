# P-HWE-18: Enclosure Drop & Shock Test Plan (ME)

#### Description
A mechanical-robustness test plan (drop, shock, optionally MIL-STD-810) defining heights, faces, samples, and pass criteria for a rugged device.

#### Information to collect (ask the user before generating)
1. Target spec (e.g. 1.0 m / 1.2 m drop, MIL-STD-810H methods)?
2. Device config (with/without dock, screen protector)?
3. Drop surface (concrete, steel) and orientations?
4. Sample size and acceptance (cosmetic vs. functional)?
5. Instrumentation (high-speed video, accelerometer)?

#### Suggested template
Structure:
- Test matrix: height, faces/edges/corners, cycles, samples
- Surface + fixture definition
- Pass/fail criteria: functional + cosmetic + payment integrity
- Post-test inspection + teardown plan
- Failure handling: containment, root-cause, redesign loop

Confirm the structure before generating.

#### File-generation prompt
```
Create a Enclosure Drop & Shock Test Plan (ME).

CONTEXT:
- Spec: [height/MIL-STD methods] — Config: [device/dock]
- Surface: [concrete/steel] — Samples: [n] — Accept: [criteria]

FORMAT:
- Drop/shock matrix table; surface/fixture notes
- Pass/fail criteria (functional + cosmetic)
- Inspection + failure-handling procedure

RULES: state functional AND cosmetic pass criteria separately; payment/contactless function must be verified post-test; cite the drop spec source [verify].
```

---
✍️ Author: Brian H. Doan
