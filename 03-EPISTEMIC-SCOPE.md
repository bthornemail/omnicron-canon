# 03-EPISTEMIC-SCOPE

## Omnicron Epistemic Scope

**Status:** Canonical authority
**Layer:** Omnicron scope topology
**Inherits:** 00-EXTENSION-AUTHORITY

---

## 1. Purpose

This document defines the four canonical scope positions before their meanings.

The Omnicron system follows the OMI foundation of place before symbol and pathway before interpretation.

---

## 2. Scope Positions

The four canonical scope positions are:

```text
FS = file/source scope
GS = group scope
RS = record scope
US = unit scope
```

These are positions, not interpretations.

The positions are fixed. The meanings may vary by context.

---

## 3. Position Definitions

### 3.1 FS — File/Source Scope

```text
FS:
  the enclosing source or file scope
```

FS is the outermost scope boundary.

It names the source from which the carried state originates.

### 3.2 GS — Group Scope

```text
GS:
  the relational grouping scope
```

GS is the scope of aggregation or grouping.

It names the relational context in which the carried state is grouped.

### 3.3 RS — Record Scope

```text
RS:
  the record boundary scope
```

RS is the scope of record boundaries.

It names the structural boundary within which the carried state is recorded.

### 3.4 US — Unit Scope

```text
US:
  the carried unit scope
```

US is the innermost scope.

It names the unit of state that is carried through the relation.

---

## 4. Scope Topology

The four positions form a topology:

```text
FS (outermost)
  ↓
GS
  ↓
RS
  ↓
US (innermost)
```

This topology is fixed.

The inheritance relation is:

```text
FS contains GS
GS contains RS
RS contains US
```

---

## 5. Scope as Bits

Each scope position is one binary feature:

```text
FS ∈ {0, 1}
GS ∈ {0, 1}
RS ∈ {0, 1}
US ∈ {0, 1}
```

The scope source is:

```text
Scope4 = (FS, GS, RS, US) ∈ GF(2)^4
```

---

## 6. Scope vs. Control Bytes

The scope bits are related to but not identical with control bytes.

### 6.1 Control Bytes

```text
0x1C = FS (control byte)
0x1D = GS (control byte)
0x1E = RS (control byte)
0x1F = US (control byte)
```

These are byte values in the OMI-IMO route frame.

### 6.2 Scope Bits

```text
FS = one binary feature inside an epistemic cell
GS = one binary feature inside an epistemic cell
RS = one binary feature inside an epistemic cell
US = one binary feature inside an epistemic cell
```

These are bits inside the encoded cell.

### 6.3 Distinction

```text
control byte:
  a byte value in the route frame
  0x1C, 0x1D, 0x1E, 0x1F

scope bit:
  a binary feature inside an epistemic cell
  FS, GS, RS, US ∈ {0, 1}

scope field:
  a fixed-width value inside the OMI-IMO route frame
```

These are related but not identical representations.

The distinction prevents a control byte such as `0x1C` from being confused with the one-bit FS feature.

---

## 7. Scope in the Epistemic Cell

The scope positions are the data input to the integrity encoder:

```text
Scope4 =
  (FS, GS, RS, US)
  ↓
integrity encoding
  ↓
CompactCell7 or MiquelCell8
```

The scope positions are recovered after decoding:

```text
CompactCell7 or MiquelCell8
  ↓
syndrome correction
  ↓
Scope4 = (FS, GS, RS, US)
```

---

## 8. Scope in CONS

The scope positions form the CAR of the epistemic CONS pair:

```text
Cell =
  (Scope4 . IntegritySurface)
  =
  ((FS GS RS US) . integrity)
```

The scope is what is carried.

The integrity is how continuation is checked.

---

## 9. Canonical Lock

```text
FS, GS, RS, US are positions.
They are not interpretations.
They are not control bytes.
They are binary features inside epistemic cells.

FS is file/source scope.
GS is group scope.
RS is record scope.
US is unit scope.

The topology is fixed.
The positions are fixed.
The meanings may vary by context.
```