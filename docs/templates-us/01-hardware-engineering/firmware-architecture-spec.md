# P-HWE-22: Firmware Architecture Specification (FW)

#### Description
The firmware architecture of record — layers, RTOS/scheduler, boot chain, update mechanism, security boundaries, and resource budgets for an embedded device.

#### Information to collect (ask the user before generating)
1. SoC/MCU, RTOS or bare-metal, and toolchain?
2. Boot chain (ROM -> bootloader -> app) and update method (OTA/USB)?
3. Security boundaries (secure boot, keys, payment isolation)?
4. Major modules and their interfaces?
5. Resource budgets (flash, RAM, CPU)?

#### Suggested template
Structure:
- Layered architecture: HAL, drivers, services, app
- Boot + update chain with rollback/anti-bricking
- Security model: secure boot, key storage, payment/EMV isolation
- Module/interface map + concurrency model
- Resource budget (flash/RAM/CPU) + headroom

Confirm the structure before generating.

#### File-generation prompt
```
Create a Firmware Architecture Specification (FW).

CONTEXT:
- SoC: [part] — RTOS: [...] — Toolchain: [...]
- Boot/update: [chain/OTA] — Security: [secure boot/keys]

FORMAT:
- Architecture description + layer diagram (text)
- Boot/update + security sections
- Module/interface table; resource budget table

RULES: the update path must define rollback/anti-bricking behavior; payment/EMV code isolation boundary must be explicit [verify against PCI PTS].
```

---
✍️ Author: Brian H. Doan
