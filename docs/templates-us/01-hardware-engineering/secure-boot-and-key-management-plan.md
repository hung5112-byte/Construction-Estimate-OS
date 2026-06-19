# P-HWE-24: Secure Boot & Key Management Plan (FW)

#### Description
The plan for the device root of trust — secure-boot chain, key generation/storage/rotation, signing process, and provisioning — central to PCI/EMV and anti-tamper.

#### Information to collect (ask the user before generating)
1. Secure-boot mechanism (SoC OTP/eFuse, signed images)?
2. Key hierarchy (root, signing, encryption) and storage (HSM, secure element)?
3. Signing process + who holds keys?
4. Provisioning at the factory (key injection, attestation)?
5. Compliance scope (PCI PTS, EMVCo)?

#### Suggested template
Structure:
- Root of trust + secure-boot chain
- Key hierarchy: roles, algorithms, lengths, storage (HSM/SE)
- Signing workflow + access control + audit
- Factory provisioning + attestation
- Rotation/revocation + incident response; compliance mapping

Confirm the structure before generating.

#### File-generation prompt
```
Create a Secure Boot & Key Management Plan (FW).

CONTEXT:
- Secure boot: [OTP/eFuse/signed] — Keys: [hierarchy/storage]
- Provisioning: [factory flow] — Compliance: [PCI PTS/EMVCo]

FORMAT:
- Root-of-trust + boot-chain description
- Key hierarchy + storage table; signing workflow
- Provisioning, rotation/revocation, compliance mapping

RULES: private signing keys must reside in an HSM/secure element with documented access control and audit; map controls to PCI PTS / EMVCo requirements [verify with assessor].
```

---
✍️ Author: Brian H. Doan
