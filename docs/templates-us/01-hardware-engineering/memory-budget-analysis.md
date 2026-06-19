# P-HWE-25: Memory & Storage Budget Analysis (FW)

#### Description
A flash/RAM/storage budget proving the firmware fits today and leaves headroom for OTA images and future features — avoids the late-stage 'out of flash' crisis.

#### Information to collect (ask the user before generating)
1. SoC memory map: flash, RAM, external storage (eMMC) sizes?
2. Image layout (bootloader, app, OTA slot A/B, filesystem, logs)?
3. Current usage per region?
4. OTA strategy (A/B dual-bank?) and image size?
5. Growth headroom target?

#### Suggested template
Structure:
- Memory map table: region, size, used, free, %
- OTA layout: dual-bank sizing + scratch/space needs
- RAM budget: static + peak heap/stack per mode
- Logs/filesystem growth + wear (eMMC) considerations
- Headroom assessment + actions if tight

Confirm the structure before generating.

#### File-generation prompt
```
Create a Memory & Storage Budget Analysis (FW).

CONTEXT:
- SoC: [flash/RAM/eMMC sizes] — Layout: [boot/app/A-B/fs]
- OTA: [A-B?/image size] — Headroom target: [%]

FORMAT:
- Memory-map table with used/free/%
- OTA + RAM budget tables
- Headroom verdict + actions

RULES: dual-bank OTA must show both slots fit with scratch space; RAM budget uses peak (not average) stack/heap; eMMC wear noted for log-heavy designs.
```

---
✍️ Author: Brian H. Doan
