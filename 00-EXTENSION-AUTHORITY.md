# 00-EXTENSION-AUTHORITY

## Omnicron Extension Authority

**Status:** Canonical authority
**Layer:** Omnicron extension definition
**Inherits:** omi-canon foundational authority

---

## 1. Inheritance Rule

Omnicron extends OMI without replacing it.

```text
OMI defines:
  NULL
  PAIR
  CAR
  CDR
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
  Omnicron-Port
  Omnicron-ISA
  Omnicron-Lisp
```

---

## 2. Canonical Authority Chain

```text
where Omnicron is silent:
  OMI governs

where Omnicron explicitly extends OMI:
  Omnicron governs the extension only

where an implementation conflicts with canon:
  canon governs
```

---

## 3. Repository Chain

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
        │               │               │               │
        └───────────────┴───────────────┴───────────────┘
                            │
                            ▼
                  omnicron-epistemic-model
                  composes all surfaces
```

---

## 4. What Omnicron Inherits from OMI

### 4.1 Foundational Relation

```text
NULL → Pair → CAR → CDR
```

This is the relational root before symbolic names are projected.

### 4.2 Scope Topology

```text
FS = file/source scope
GS = group scope
RS = record scope
US = unit scope
```

FS/GS/RS/US remains the canonical scope topology.

### 4.3 Notation Surface

```text
omi---imo?O_o
```

and:

```text
o-FS-GS-RS-US/FS/GS/RS/US?REGISTER?STACK@CAR@CDR
```

### 4.4 Authority Boundaries

```text
validation accepts state
receipt records accepted state
projection displays but does not accept
interpretation explains but does not validate
```

---

## 5. What Omnicron Adds

### 5.1 COBS-CONS Framing

```text
CONS:
  relational composition and continuation

COBS:
  zero-safe byte-stream framing

COBS-CONS:
  CONS relations transported through deterministic COBS framing
```

### 5.2 Coded Epistemic Cells

```text
Scope4 =
  GF(2)^4

CompactCell7 =
  Hamming743(Scope4)

MiquelCell8 =
  ExtendedHamming844(Scope4)
```

### 5.3 LOGOS/NOMOS/PATHOS Integrity

```text
Compact profile:
  three derived parity positions

Miquel profile:
  three paired incidence dimensions
```

### 5.4 Ternary Epistemic Activation

```text
-1 = invalid, contradicted, malformed, or uncorrectable
 0 = lawful but unresolved candidate
+1 = validated and receipted state
```

### 5.5 Implementation Surfaces

```text
Omnicron-Port:
  dormant route declarations with codec profiles

Omnicron-ISA:
  deterministic encoded operations

Omnicron-Lisp:
  readable declarations with integrity forms
```

---

## 6. Non-Destructive Extension

Omnicron does not:

```text
replace OMI authority
override OMI scope topology
change OMI notation surface
remove validation boundaries
remove receipt authority
```

Omnicron does:

```text
extend CONS with COBS framing
add coded integrity to scope cells
add LOGOS/NOMOS/PATHOS incidence dimensions
add Hamming and Miquel codec profiles
add ternary epistemic activation
define implementation surfaces
```

---

## 7. Canonical Lock

```text
OMI is foundational.
Omnicron is extension.
Extension does not replace foundation.
Foundation governs where extension is silent.
Canon governs where implementation conflicts.
```

---

## 8. Final Statement

```text
Omnicron extends OMI without replacing it.

OMI supplies the foundational relation, scope topology,
route notation, execution discipline, validation boundary,
and receipt authority.

Omnicron adds COBS-CONS framing, coded epistemic cells,
LOGOS/NOMOS/PATHOS integrity dimensions, the canonical
Miquel-presented extended Hamming [8,4,4] profile,
and bounded ternary activation.

Omnicron-Port declares encoded routes.
Omnicron-ISA executes encoded operations.
Omnicron-Lisp expresses encoded declarations.
The Omnicron-Epistemic-Model composes those surfaces.

Correction restores candidates.
Validation determines admissibility.
Receipt alone records accepted state.
```