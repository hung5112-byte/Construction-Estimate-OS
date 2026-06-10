# P-OPS-N3: Field Deployment Checklist

#### Description
A site-deployment checklist for installing electronic devices in the field — site readiness, configuration verification, install steps, acceptance sign-off, and spares. Turns deployments from heroics into a repeatable operation.

#### Information to collect (ask the user before generating)
1. Device type(s) and typical site profile? (count per site, environment)
2. Who installs — own staff, partner, or customer self-install?
3. Network/power prerequisites at the site?
4. Configuration done at kitting or on-site?
5. What counts as "accepted"? (test transaction, connectivity check, sign-off)

#### Suggested template
Structure:
- **Pre-deployment**: site survey items (power, network, mounting, access),
  kit verification (devices, firmware/config version, cables, consumables),
  spares decision, scheduled window + site contact
- **On-site install**: physical install steps, connectivity bring-up,
  configuration/provisioning verification, functional acceptance test
- **Acceptance**: acceptance criteria, sign-off (name/date), photos, serial
  numbers recorded against the site
- **Closeout**: inventory updated (deployed status), exceptions logged,
  return shipment for replaced/failed units via RMA
- **Rollback**: what to do when install fails (spare swap, revert, escalate)

Confirm the structure before generating.

#### File-generation prompt
```
Create a Field Deployment Checklist.

CONTEXT:
- Device(s): [models] — Installer: [staff/partner/customer]
- Site prerequisites: [power/network/mounting]
- Acceptance: [criteria]

FORMAT:
- Three-phase checklist (pre-deployment / on-site / closeout) with checkboxes
- Acceptance block (criteria, sign-off, serials, photos)
- Exception & rollback procedure
- Inventory/RMA update steps

TONE: field-usable, terse imperatives. LENGTH: 1-2 pages.
```

---
✍️ Author: Brian H. Doan
