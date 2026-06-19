# P-HWE-26: System Requirements Specification (SRS)

#### Description
The top-level requirements of record for a product — functional, performance, environmental, regulatory, and interface requirements, each testable and traceable.

#### Information to collect (ask the user before generating)
1. Product and its primary use cases?
2. Functional + performance requirements (with numbers)?
3. Environmental + mechanical requirements (IP, drop, temp)?
4. Regulatory/cert requirements (FCC, UL, PCI/EMV)?
5. External interfaces (power, network, payment, peripherals)?

#### Suggested template
Structure:
- Scope + use cases + assumptions
- Requirements by category (functional, performance, environmental, regulatory, interface), each with an ID and a verification method
- Constraints + assumptions
- Traceability hooks (req IDs for DVP&R and RTM)
- Open items / TBDs

Confirm the structure before generating.

#### File-generation prompt
```
Create a System Requirements Specification (SRS).

CONTEXT:
- Product: [model] — Use cases: [...]
- Categories: functional/performance/environmental/regulatory/interface

FORMAT:
- Numbered requirements table: ID, requirement, value, verification method
- Category sections; constraints/assumptions
- Open-items (TBD) list

RULES: every requirement has a unique ID, a measurable value, and a verification method (test/analysis/inspection/demo); vague 'should be fast' wording is rejected.
```

---
✍️ Author: Brian H. Doan
