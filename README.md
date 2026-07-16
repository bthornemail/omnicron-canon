# Omnicron Canon

The Omnicron extension authority for the OMI protocol ecosystem.

## What This Repo Is

This is the normative extension authority for the Omnicron system.

It extends OMI without replacing it.

```text
omi-canon
    foundational authority
        │
        ▼
omnicron-canon
    extension authority
        │
        ├───────────────┬───────────────┬───────────────┐
        ▼               ▼               ▼               ▼
    omnicron-port   omnicron-isa   omnicron-lisp   omnicron-epistemic-model
    declaration     execution      readable syntax  integration
```

## Repository Structure

```
omnicron-canon/
├── README.md
├── AGENTS.md
├── 00-EXTENSION-AUTHORITY.md
├── 01-COBS-CONS.md
├── 02-EPISTEMIC-CELL.md
├── 03-EPISTEMIC-SCOPE.md
├── 04-LOGOS-NOMOS-PATHOS.md
├── 05-MIQUEL-INTEGRITY.md
├── 06-EPISTEMIC-ACTIVATION.md
├── 07-OMNICRON-PORT.md
├── 08-OMNICRON-ISA.md
├── 09-OMNICRON-LISP.md
├── 10-VALIDATION-AND-RECEIPT.md
├── 11-CONFORMANCE.md
└── dev-docs/
```

## Canonical Spine

| File | Description |
|------|-------------|
| `00-EXTENSION-AUTHORITY.md` | Inheritance chain from omi-canon |
| `01-COBS-CONS.md` | COBS-CONS codec definition |
| `02-EPISTEMIC-CELL.md` | Smallest encoded object |
| `03-EPISTEMIC-SCOPE.md` | FS/GS/RS/US scope positions |
| `04-LOGOS-NOMOS-PATHOS.md` | Integrity dimensions |
| `05-MIQUEL-INTEGRITY.md` | Miquel [8,4,4] profile |
| `06-EPISTEMIC-ACTIVATION.md` | Ternary activation model |
| `07-OMNICRON-PORT.md` | Dormant route declarations |
| `08-OMNICRON-ISA.md` | Execution semantics |
| `09-OMNICRON-LISP.md` | Readable syntax |
| `10-VALIDATION-AND-RECEIPT.md` | Authority boundaries |
| `11-CONFORMANCE.md` | Conformance profiles |

## Key Terminology

- **Omicron** — deterministic CONS relation (lower layer)
- **Omnicron** — CONS + COBS determinism (this repo's focus)
- **Canonical notation:** `omi---imo?O_o`
- **Scope positions:** `FS/GS/RS/US`
- **Integrity dimensions:** `LOGOS/NOMOS/PATHOS`
- **Compact profile:** Hamming `[7,4,3]`
- **Extended profile:** Miquel `[8,4,4]`

## Authority Chain

```text
OMI defines:
  NULL, PAIR, CAR, CDR
  FS/GS/RS/US
  OMI-IMO notation
  validation boundary
  receipt authority

Omnicron extends:
  CONS with COBS framing
  scope cells with coded integrity
  LOGOS/NOMOS/PATHOS incidence
  Hamming and Miquel profiles
  ternary epistemic activation
  Omnicron-Port, Omnicron-ISA, Omnicron-Lisp
```

## dev-docs/

The `dev-docs/` folder contains historical derivation records.

These files are preserved as context but are not part of the canonical spine.

## Canonical Lock

```text
Omnicron extends OMI without replacing it.
Extension does not replace foundation.
Foundation governs where extension is silent.
Canon governs where implementation conflicts.
```