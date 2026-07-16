# 05-MIQUEL-INTEGRITY

## Miquel [8,4,4] Integrity Profile

**Status:** Canonical authority
**Layer:** Omnicron extended integrity
**Inherits:** 02-EPISTEMIC-CELL, 04-LOGOS-NOMOS-PATHOS

---

## 1. Purpose

This document defines the canonical extended integrity profile: the Miquel-presented extended Hamming `[8,4,4]` code.

The Miquel configuration is the canonical geometric presentation of the extended Hamming `[8,4,4]` integrity cell.

---

## 2. Configuration

The Miquel configuration has:

```text
8 points
6 circles
4 points on each circle
3 circles through each point
24 total incidences
```

Configuration notation:

```text
(8_3 6_4)
```

This matches the Tetragrammatron witness count.

---

## 3. Point Ordering

The eight points are represented as the vertices of a cube:

```text
P000 P001 P010 P011
P100 P101 P110 P111
```

The point indices correspond to the three incidence dimensions:

```text
bit 2 = LOGOS sign
bit 1 = NOMOS sign
bit 0 = PATHOS sign
```

Example:

```text
P101 lies on:
  LOGOS+ (bit 2 = 1)
  NOMOS− (bit 1 = 0)
  PATHOS+ (bit 0 = 1)
```

---

## 4. Bit Ordering

The canonical bit ordering for the Miquel cell is:

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

---

## 5. Six Incidence Masks

The six four-point incidence relations are:

```text
LOGOS−  = {P000, P001, P010, P011}
LOGOS+  = {P100, P101, P110, P111}

NOMOS−  = {P000, P001, P100, P101}
NOMOS+  = {P010, P011, P110, P111}

PATHOS− = {P000, P010, P100, P110}
PATHOS+ = {P001, P011, P101, P111}
```

Every circle contains four points.

Every point occurs in exactly three circles.

---

## 6. Parity-Check Matrix

The binary incidence matrix is:

```text
           000 001 010 011 100 101 110 111

LOGOS−     1   1   1   1   0   0   0   0
LOGOS+     0   0   0   0   1   1   1   1

NOMOS−     1   1   0   0   1   1   0   0
NOMOS+     0   0   1   1   0   0   1   1

PATHOS−    1   0   1   0   1   0   1   0
PATHOS+    0   1   0   1   0   1   0   1
```

Over `GF(2)`, this matrix has rank four.

Therefore its kernel has dimension:

```text
8 − 4 = 4
```

and contains:

```text
2^4 = 16
```

codewords.

Its minimum nonzero codeword weight is four.

Therefore:

```text
kernel(Miquel incidence matrix)
=
extended Hamming [8,4,4]
```

---

## 7. Why Six Checks Produce a Four-Dimensional Code

The six circle equations are intentionally redundant.

For each opposite pair:

```text
LOGOS− XOR LOGOS+   = total parity
NOMOS− XOR NOMOS+   = total parity
PATHOS− XOR PATHOS+ = total parity
```

Therefore the three pair sums agree.

The visible integrity surface contains six checks, but only four are linearly independent.

Canonical interpretation:

```text
six visible incidence checks
four independent algebraic constraints
four source degrees of freedom
```

This redundancy gives geometric symmetry without changing the code dimension.

---

## 8. Generator Matrix

The generator matrix maps the four source bits to the eight encoded bits:

```text
G : GF(2)^4 → GF(2)^8
```

A systematic implementation preserves the four source bits in selected positions and derives four parity positions.

The canonical geometric model nevertheless treats all eight encoded points as symmetric carrier positions.

The exact generator matrix MUST be fixed by the implementation profile and MUST satisfy all six Miquel incidence equations.

---

## 9. Encoding Algorithm

The encoding function is:

```text
encode_miquel844 : Scope4 → MiquelCell8
```

where:

```text
Scope4 = (FS, GS, RS, US) ∈ GF(2)^4
MiquelCell8 ∈ GF(2)^8
```

The encoding MUST satisfy:

```text
H_Miquel × encode_miquel844(scope4)^T = 0
```

over `GF(2)`, where `H_Miquel` is the parity-check matrix.

---

## 10. Miquel Syndrome

On reception, recompute the six circle checks:

```text
σ =
(
  σLOGOS−,
  σLOGOS+,
  σNOMOS−,
  σNOMOS+,
  σPATHOS−,
  σPATHOS+
)
```

A zero syndrome is:

```text
000000
```

and indicates no detected corruption.

A single-point error causes exactly three failed checks:

```text
one of LOGOS− or LOGOS+
one of NOMOS− or NOMOS+
one of PATHOS− or PATHOS+
```

The selected signs identify one unique point.

Example:

```text
failed checks:
  LOGOS+
  NOMOS−
  PATHOS+

identified point:
  P101
```

---

## 11. Syndrome Classification

### 11.1 No Detected Error

```text
all six checks = 0
```

Action:

```text
continue to decoding and validation
```

### 11.2 Correctable Single-Point Error

```text
syndrome equals one point-incidence column
```

Action:

```text
flip the identified point
recompute all six checks
continue only if the result is zero
```

### 11.3 Detected Non-Single Error

```text
syndrome does not equal zero
and does not equal one point-incidence column
```

Action:

```text
reject
or
retain as unresolved diagnostic state
```

It MUST NOT be corrected as a single-point error.

---

## 12. Single-Error Correction

The single-point correction rule is:

```text
if syndrome matches exactly one Miquel point:
    flip that point
    recompute all six checks
```

The decoder MUST accept the correction only if all six checks vanish after recomputation.

---

## 13. Double-Error Detection

The Miquel `[8,4,4]` profile provides:

```text
single-error correction
double-error detection
```

A detected double-bit error MUST be rejected and MUST NOT be corrected as a single-bit error.

It MUST be rejected or retained as an unresolved candidate.

---

## 14. Decoding Algorithm

The decoding function is:

```text
decode_miquel844 : MiquelCell8 → Scope4 ∪ {⊥}
```

where `⊥` indicates an uncorrectable error.

The decoding algorithm:

```text
1. compute six circle checks
2. classify syndrome:
   a. if zero: recover scope
   b. if matches one point: flip point, recompute, verify
   c. otherwise: reject
3. extract scope bits from corrected cell
```

---

## 15. Canonical Formulas

### 15.1 Source

```text
DATA =
  FS GS RS US
```

### 15.2 Encoded Cell

```text
CODE8 =
  Miquel844(DATA)
```

### 15.3 Incidence Checks

```text
CHECK6 =
  (
    LOGOS− LOGOS+
    NOMOS− NOMOS+
    PATHOS− PATHOS+
  )
```

### 15.4 Parity Equation

```text
H_Miquel × CODE8^T = 0
```

over `GF(2)`.

---

## 16. Conformance Invariants

A conforming implementation MUST preserve:

```text
decode_miquel(encode_miquel(scope4)) = scope4
```

For every single-point corruption:

```text
decode_miquel(flip_one_point(encode_miquel(scope4))) = scope4
```

For every detected two-point corruption:

```text
decode_miquel(flip_two_points(encode_miquel(scope4))) = reject
```

The decoder MUST NOT allow integrity correction to:

```text
create new scope
change address authority
accept a declaration
invent missing payload
emit an accepted receipt without validation
```

---

## 17. Canonical Lock

```text
The Miquel configuration is the canonical geometric presentation
of the extended Hamming [8,4,4] integrity cell.

8 points, 6 circles, 4 points per circle, 3 circles through each point.

The parity-check matrix has rank four.
The kernel contains 16 codewords.
Minimum nonzero weight is four.

Single-error correction is mandatory.
Double-error detection is mandatory.
Double-error correction is forbidden.

Correction restores candidates.
Validation accepts state.
Receipt records accepted state.
```