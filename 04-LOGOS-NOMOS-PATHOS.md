# 04-LOGOS-NOMOS-PATHOS

## LOGOS/NOMOS/PATHOS Integrity Dimensions

**Status:** Canonical authority
**Layer:** Omnicron integrity surface
**Inherits:** 02-EPISTEMIC-CELL, 03-EPISTEMIC-SCOPE

---

## 1. Purpose

This document defines the three derived integrity dimensions: LOGOS, NOMOS, and PATHOS.

These dimensions have two profile-dependent realizations:

```text
Compact profile:
  three derived parity positions

Miquel profile:
  three paired incidence dimensions
```

They should not be simultaneously described as both stored parity bits and geometric axes without identifying the active profile.

---

## 2. Canonical Replacement

The deprecated relation:

```text
LL/MM/NN
```

is replaced by:

```text
LOGOS/NOMOS/PATHOS
```

This is not a direct renaming of three old variables.

The former three-field argument authority is removed.

LOGOS, NOMOS, and PATHOS are newly defined as three derived integrity dimensions over the four canonical scope features:

```text
FS
GS
RS
US
```

Canonical statement:

```text
FS/GS/RS/US carries scope.
LOGOS/NOMOS/PATHOS checks the carried relation.
```

---

## 3. Authority Boundary

The four scope features remain primary:

```text
FS = file scope
GS = group scope
RS = record scope
US = unit scope
```

The three epistemic dimensions are derived:

```text
LOGOS  = coherence dimension
NOMOS  = ordering and boundary-law dimension
PATHOS = continuity and carried-state dimension
```

They MUST NOT be interpreted as additional scope levels.

They MUST NOT replace FS, GS, RS, or US.

They MUST NOT independently accept state.

Canonical invariant:

```text
scope is primary
integrity is derived
acceptance is external
```

---

# Part I — Compact Hamming Profile

## 4. Compact Arrangement

The compact seven-position arrangement is:

```text
position 1 = LOGOS
position 2 = NOMOS
position 3 = FS
position 4 = PATHOS
position 5 = GS
position 6 = RS
position 7 = US
```

Compact form:

```text
[L N F P G R U]
```

The positions are divided as:

```text
check positions: 1, 2, 4
data positions:  3, 5, 6, 7
```

This gives:

```text
4 data bits
3 check bits
minimum Hamming distance 3
```

Canonical code designation:

```text
Hamming [7,4,3]
```

This profile provides single-error correction when protected by an external frame-integrity witness.

---

## 5. Compact Check Relations

Using even parity:

```text
LOGOS  = FS XOR GS XOR US
NOMOS  = FS XOR RS XOR US
PATHOS = GS XOR RS XOR US
```

Equivalently:

```text
LOGOS XOR FS XOR GS XOR US = 0
NOMOS XOR FS XOR RS XOR US = 0
PATHOS XOR GS XOR RS XOR US = 0
```

The three incidence sets are:

```text
LOGOS:
  positions 1, 3, 5, 7

NOMOS:
  positions 2, 3, 6, 7

PATHOS:
  positions 4, 5, 6, 7
```

---

## 6. Compact Syndrome

On reception:

```text
sLOGOS =
  LOGOS XOR FS XOR GS XOR US

sNOMOS =
  NOMOS XOR FS XOR RS XOR US

sPATHOS =
  PATHOS XOR GS XOR RS XOR US
```

The syndrome index is:

```text
syndrome =
    sLOGOS
  + 2 × sNOMOS
  + 4 × sPATHOS
```

| Syndrome | Position | Meaning |
|---:|---:|---|
| `000` | none | no detected single-bit error |
| `001` | 1 | LOGOS |
| `010` | 2 | NOMOS |
| `011` | 3 | FS |
| `100` | 4 | PATHOS |
| `101` | 5 | GS |
| `110` | 6 | RS |
| `111` | 7 | US |

A nonzero syndrome identifies the position of a presumed single-bit error.

Canonical correction:

```text
if syndrome != 0:
    flip codeword[syndrome]
```

After correction, all three parity equations MUST be recomputed.

The compact profile MUST also use a frame-level length, checksum, hash, receipt witness, or equivalent integrity mechanism to reject unrecognized multi-bit corruption.

---

## 7. Compact Interpretation

In the compact profile, LOGOS, NOMOS, and PATHOS are parity positions.

They are derived from the four scope features.

They check the structural coherence of the scope arrangement.

### 7.1 LOGOS

```text
LOGOS checks:
  source-group-unit coherence
```

Question:

```text
Does the carried scope agree with its relational form?
```

### 7.2 NOMOS

```text
NOMOS checks:
  source-record-unit law
```

Question:

```text
Does the carried scope obey its declared ordering and boundary law?
```

### 7.3 PATHOS

```text
PATHOS checks:
  group-record-unit continuity
```

Question:

```text
Has the carried state remained connected through traversal?
```

---

# Part II — Miquel Profile

## 8. Miquel Incidence Dimensions

In the Miquel profile, LOGOS, NOMOS, and PATHOS are not stored parity bits.

They are three complementary incidence dimensions:

```text
LOGOS− / LOGOS+
NOMOS− / NOMOS+
PATHOS− / PATHOS+
```

Each dimension has two complementary circles.

Each point lies on exactly one circle from each pair.

---

## 9. Miquel Incidence Sets

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

The resulting binary incidence matrix is:

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

## 10. Miquel Interpretation

In the Miquel profile, LOGOS, NOMOS, and PATHOS are geometric axes.

They are not stored parity bits.

They are complementary incidence dimensions that constrain the eight-point codeword.

### 10.1 LOGOS

```text
LOGOS− / LOGOS+
  coherence axis
```

Interpretation:

```text
readable relational agreement
symbolic consistency
```

Question:

```text
Does the carried scope agree with its relational form?
```

### 10.2 NOMOS

```text
NOMOS− / NOMOS+
  ordering axis
```

Interpretation:

```text
boundary law
declared structural conformity
```

Question:

```text
Does the carried scope obey its declared ordering and boundary law?
```

### 10.3 PATHOS

```text
PATHOS− / PATHOS+
  continuity axis
```

Interpretation:

```text
carriage
perceptible connection through traversal
```

Question:

```text
Has the carried state remained connected through traversal?
```

No one dimension independently owns or accepts the encoded state.

Their paired incidence constrains the complete eight-point codeword.

---

## 11. Profile Distinction

The two profiles must not be confused:

```text
Hamming [7,4,3]:
  LOGOS/NOMOS/PATHOS are parity positions
  derived from scope features
  checked by parity equations

Miquel [8,4,4]:
  LOGOS/NOMOS/PATHOS are complementary incidence axes
  six four-point circles
  three pairs through each point
```

Canonical distinction:

```text
Compact profile:
  LOGOS/NOMOS/PATHOS are parity positions

Miquel profile:
  LOGOS/NOMOS/PATHOS are complementary incidence axes
```

They should not be simultaneously described as both stored parity bits and geometric axes without identifying the active profile.

---

## 12. Canonical Lock

```text
LOGOS/NOMOS/PATHOS are three derived integrity dimensions.

In the compact profile, they are parity positions.
In the Miquel profile, they are complementary incidence axes.

They are not additional scope levels.
They do not replace FS, GS, RS, or US.
They do not independently accept state.

Scope is primary.
Integrity is derived.
Acceptance is external.
```