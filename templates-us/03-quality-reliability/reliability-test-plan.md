# P-QR-03: Reliability Test Plan

#### Description
A reliability campaign plan beyond functional DVT — accelerated life, thermal cycling, HALT/HASS, drop/vibration, connector endurance — with sample-size math and acceptance criteria set before the chambers run. Reliability is statistics; this plan treats it that way.

#### Information to collect (ask the user before generating)
1. Product and the field-life claim to support? (years, cycles, environment)
2. Failure modes of concern? (from FMEA, field history, or new-design risk)
3. Tests in scope? (thermal cycle, damp heat, HALT, drop, vibration, connector cycles, battery aging)
4. Sample budget and where samples come from? (which build)
5. Schedule constraint? (which gate consumes the results)

#### Suggested template
Structure:
- **Objective table**: field-life claim → test, acceleration model/assumption
  [acceleration factors are assumptions — state them; verify against standards where applicable]
- **Test matrix**: test, condition/profile, duration/cycles, sample size,
  acceptance criterion (failures allowed at what confidence), equipment/lab
- **Sample plan**: build/lot, configuration, serialization, pre-test baseline data
- **Failure handling**: every failure gets a mechanism analysis (feeds 8D);
  test continues vs. halts rules
- **Reporting**: interim cadence, final report content, gate it feeds
- **Handoffs**: mechanisms to engineering, lab bookings, results into the gate review

Confirm the structure before generating.

#### File-generation prompt
```
Create a Reliability Test Plan.

CONTEXT:
- Product: [model] — Life claim: [X years / N cycles in environment]
- Concerns: [failure modes] — Sample budget: [n from build Y] — Gate: [date]

FORMAT:
- Objective table with acceleration assumptions stated
- Test matrix (condition, duration, n, acceptance criterion w/ confidence)
- Sample plan with baselines; failure-handling rules; reporting + handoffs

RULES: acceptance criteria and sample sizes are set before testing;
shrinking n to fit schedule must state the confidence cost;
every failure gets a mechanism, not a retest.
```

---
✍️ Author: Brian H. Doan
