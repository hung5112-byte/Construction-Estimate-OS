# P-SVC-04: Site Survey Form

#### Description
The pre-deployment site survey — power, network, mounting, access, and contacts captured before any install is scheduled. No install into a site that hasn't passed this form; it's the difference between an install and a second trip.

#### Information to collect (ask the user before generating)
1. Device type(s) being deployed and their site prerequisites?
2. Survey method? (on-site walk, remote with customer photos, questionnaire)
3. Site contact roles needed? (facilities, IT/network, security/badging)
4. Network requirements? (ethernet/Wi-Fi/cellular, ports/firewall rules, static IPs)
5. Installation window constraints? (business hours, freezes)

#### Suggested template
Structure:
- **Site header**: site name/ID, address, contacts (name/role/phone), survey date, surveyor
- **Power**: outlets at mount points (count/type), circuit availability, UPS requirement
- **Network**: connection type, ports/firewall rules needed [from the device's network spec],
  signal strength at mount points (cellular/Wi-Fi), static IP/DHCP decision
- **Physical**: mount locations with photos, clearances, cable runs, environmental
  concerns (heat, moisture, tamper exposure)
- **Access & scheduling**: badging/escort needs, allowed windows, freight/elevator access
- **Gaps table**: requirement not met → owner (us/customer), due date — install blocked until cleared
- **Verdict**: READY / READY WITH ACTIONS (dated) / NOT READY

Confirm the structure before generating.

#### File-generation prompt
```
Create a Site Survey Form.

CONTEXT:
- Device(s): [models + prerequisites] — Method: [on-site/remote]
- Network needs: [spec] — Window constraints: [hours/freezes]

FORMAT:
- Site header with contacts; power/network/physical/access sections with
  checkboxes + photo placeholders; gaps table with owners and dates
- Verdict block gating the install schedule

RULES: a gap without an owner blocks scheduling; photos accompany every mount
location; network rules are confirmed by the customer's IT contact by name.
```

---
✍️ Author: Brian H. Doan
