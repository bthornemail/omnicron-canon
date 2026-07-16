# 02-EPISTEMIC-CELL

## Omnicron Epistemic Cell

**Status:** Canonical authority
**Layer:** Omnicron encoded object definition
**Inherits:** 00-EXTENSION-AUTHORITY, 03-EPISTEMIC-SCOPE

---

## 1. Purpose

This document defines the smallest encoded object in the Omnicron system: the epistemic cell.

The epistemic cell is the atomic unit of coded scope. It carries four scope features through integrity encoding, transport, and recovery.

---

## 2. Epistemic Source Cell

The epistemic source cell is four binary scope features:

```text
Scope4 =
  (FS, GS, RS, US)
  ∈ GF(2)^4
```

where:

```text
FS = file/source scope bit
GS = group scope bit
RS = record scope bit
US = unit scope bit
```

The source cell is the uncoded input to the integrity encoder.

It is the raw scope before any protection is applied.

---

## 3. Compact Encoded Cell

The compact encoded cell uses the Hamming `[7,4,3]` code:

```text
CompactCell7 =
  Hamming743(Scope4)
  ∈ GF(2)^7
```

The compact cell has:

```text
4 data bits (scope features)
3 check bits (LOGOS, NOMOS, PATHOS)
minimum Hamming distance 3
```

The compact cell provides single-error correction when protected by an external frame-integrity witness.

---

## 4. Canonical Extended Cell

The canonical extended cell uses the Miquel-presented extended Hamming `[8,4,4]` code:

```text
MiquelCell8 =
  ExtendedHamming844(Scope4)
  ∈ GF(2)^8
```

The Miquel cell has:

```text
8 encoded positions (symmetric)
6 four-point incidence checks
3 checks through each point
24 total incidences
minimum Hamming distance 4
```

The Miquel cell provides:

```text
single-error correction
double-error detection
```

The Miquel cell is the canonical extended profile.

---

## 5. Type Relation

The canonical type relation is:

```text
Scope4 =
  GF(2)^4

CompactCell7 =
  Hamming743(Scope4)

MiquelCell8 =
  ExtendedHamming844(Scope4)
```

The encoding functions are:

```text
encode_compact : Scope4 → CompactCell7
decode_compact : CompactCell7 → Scope4

encode_miquel : Scope4 → MiquelCell8
decode_miquel : MiquelCell8 → Scope4
```

The decoding functions are partial:

```text
decode_compact :
  CompactCell7 → Scope4 ∪ {⊥}

decode_miquel :
  MiquelCell8 → Scope4 ∪ {⊥}
```

where `⊥` indicates an uncorrectable error.

---

## 6. Cell as CONS Pair

The epistemic cell may be represented as a CONS pair:

```text
Cell =
  (Scope4 . IntegritySurface)
```

For the compact profile:

```text
Cell7 =
  ((FS GS RS US) . (LOGOS NOMOS PATHOS))
```

For the Miquel profile:

```text
Cell8 =
  ((FS GS RS US) . (LOGOS− LOGOS+ NOMOS− NOMOS+ PATHOS− PATHOS+))
```

Canonical interpretation:

```text
CAR = what is carried (scope)
CDR = how continuation is checked (integrity)
```

---

## 7. Cell as Byte

The Miquel cell maps directly to one byte:

```text
bit 7 = P111
bit 6 = P110
bit 5 = P101
bit 4 = P100
bit 3 = P011
bit 2 = P010
bit 1 = P001
bit 0 = P000
```

This mapping is canonical unless a profile explicitly declares another bit order.

The Miquel cell therefore aligns with COBS:

```text
one encoded epistemic cell
=
one byte
```

A zero-valued encoded byte is legal at the integrity layer and is handled by COBS stuffing.

---

## 8. Cell Lifecycle

The complete cell lifecycle is:

```text
scope source
  ↓
integrity encoding
  ↓
byte packing
  ↓
COBS encoding
  ↓
transport
  ↓
COBS decoding
  ↓
byte unpacking
  ↓
syndrome classification
  ↓
correction or rejection
  ↓
scope recovery
  ↓
validation
  ↓
receipt
```

The cell is a candidate throughout this lifecycle.

Only validation and receipt accept the cell as state.

---

## 9. Canonical Lock

```text
Scope4 is the source.
CompactCell7 is the compact encoded cell.
MiquelCell8 is the canonical extended encoded cell.

Encoding protects scope.
Decoding recovers scope.
Correction restores candidates.
Validation accepts state.
Receipt records accepted state.
```