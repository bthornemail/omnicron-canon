# LOGOS/NOMOS/PATHOS COBS-CONS Integrity Model

## Hamming and Miquel Encoding for the Omnicron-Epistemic-Model

**Version:** `1.0.0-draft`  
**Status:** Canonical Defined Model  
**Layer:** Omnicron COBS-CONS Integrity Surface  
**Replaces:** Deprecated `LL/MM/NN` transition terminology  
**Preserves:** `FS/GS/RS/US` as canonical pre-language scope topology  
**Canonical Extended Geometry:** Miquel configuration / extended Hamming `[8,4,4]`

---

## 0. Purpose

This document defines how the Omnicron-Epistemic-Model protects four canonical scope features:

```text
FS
GS
RS
US
```

using three derived epistemic dimensions:

```text
LOGOS
NOMOS
PATHOS
```

The compact profile uses the binary Hamming `[7,4,3]` code.

The canonical extended profile uses the Miquel configuration as a symmetric geometric presentation of the extended Hamming `[8,4,4]` code.

The complete separation of responsibility is:

```text
FS/GS/RS/US
  carries scope topology

LOGOS/NOMOS/PATHOS
  defines three integrity dimensions

Hamming or Miquel incidence
  detects and corrects local corruption

CONS
  preserves relational continuation

COBS
  preserves deterministic zero-safe framing

validation
  decides acceptance

receipt
  records accepted state
```

---

## 1. Canonical Replacement

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

## 2. Authority Boundary

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

## 3. Hamming `[7,4,3]` Arrangement

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

## 4. Compact Check Relations

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

## 5. Compact Syndrome

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

# Part II — Canonical Miquel Extended Profile

## 6. Miquel Configuration

The canonical extended encoding uses the Miquel configuration:

```text
8 points
6 circles
4 points on each circle
3 circles through each point
```

Configuration notation:

```text
(8_3 6_4)
```

The eight points are represented as the vertices of a cube:

```text
P000 P001 P010 P011
P100 P101 P110 P111
```

The six circles are arranged as three complementary pairs:

```text
LOGOS−   LOGOS+
NOMOS−   NOMOS+
PATHOS−  PATHOS+
```

Each point lies on exactly one circle from each pair.

Each point therefore has a three-bit incidence address:

```text
LOGOS sign
NOMOS sign
PATHOS sign
```

Example:

```text
P101 lies on:
  LOGOS+
  NOMOS−
  PATHOS+
```

---

## 7. Miquel Incidence Sets

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

## 8. Why Six Checks Produce a Four-Dimensional Code

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

## 9. Miquel Encoder

The uncoded source word is:

```text
m =
  (FS, GS, RS, US)
  ∈ GF(2)^4
```

The encoder maps the source word to an eight-point codeword:

```text
E :
  GF(2)^4 → GF(2)^8
```

A systematic implementation MAY preserve the four source bits in selected positions and derive four parity positions.

The canonical geometric model MUST nevertheless treat all eight encoded points as symmetric carrier positions.

Therefore:

```text
logical source:
  four scope bits

encoded carrier:
  eight peer positions

integrity surface:
  six Miquel circles
```

The exact generator matrix MUST be fixed by the implementation profile and MUST satisfy all six Miquel incidence equations.

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

The single-point correction rule is:

```text
if syndrome matches exactly one Miquel point:
    flip that point
    recompute all six checks
```

The decoder MUST accept the correction only if all six checks vanish after recomputation.

---

## 11. Extended Error Classification

The Miquel `[8,4,4]` profile provides:

```text
single-error correction
double-error detection
```

Canonical classification:

### No detected error

```text
all six checks = 0
```

Action:

```text
continue to decoding and validation
```

### Correctable single-point error

```text
syndrome equals one point-incidence column
```

Action:

```text
flip the identified point
recompute all six checks
continue only if the result is zero
```

### Detected non-single error

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

## 12. LOGOS/NOMOS/PATHOS as Dimensions

In the Miquel profile, LOGOS, NOMOS, and PATHOS are not stored parity bits.

They are three complementary incidence dimensions:

```text
LOGOS− / LOGOS+
NOMOS− / NOMOS+
PATHOS− / PATHOS+
```

Their interpretations are:

### LOGOS

```text
coherence
readable relational agreement
symbolic consistency
```

Question:

```text
Does the carried scope agree with its relational form?
```

### NOMOS

```text
order
boundary law
declared structural conformity
```

Question:

```text
Does the carried scope obey its declared ordering and boundary law?
```

### PATHOS

```text
continuity
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

# Part III — COBS-CONS Integration

## 13. Layer Separation

The integrity code, COBS, and CONS operate at different layers:

```text
Miquel/Hamming:
  protects local feature integrity

COBS:
  preserves zero-safe stream framing

CONS:
  preserves relational traversal

FS/GS/RS/US:
  preserves scope topology
```

Canonical stack:

```text
FS/GS/RS/US source feature
↓
Hamming [7,4,3] compact encoding
or
Miquel [8,4,4] extended encoding
↓
pack encoded cells into bytes
↓
COBS encode
↓
transport
↓
COBS decode
↓
unpack encoded cells
↓
syndrome classification
↓
correction or rejection
↓
recover FS/GS/RS/US
↓
CONS reconstruction
↓
interpretation
↓
validation
↓
receipt
```

COBS MUST be applied after integrity encoding has been packed into bytes.

On reception, COBS MUST be decoded before Hamming or Miquel syndrome evaluation.

---

## 14. Byte Packing

### 14.1 Compact Profile

A Hamming `[7,4,3]` cell occupies seven bits.

Recommended canonical packing:

```text
bit 7     = profile or reserved bit
bits 6..0 = Hamming codeword
```

Two compact cells MAY be packed into one 16-bit carrier.

The profile bit MUST have a fixed interpretation.

### 14.2 Miquel Extended Profile

A Miquel `[8,4,4]` cell occupies exactly one byte:

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

The Miquel profile therefore aligns naturally with COBS:

```text
one encoded epistemic cell
=
one byte
```

COBS then treats that encoded byte as ordinary payload.

A zero-valued encoded byte is legal at the integrity layer and is handled by COBS stuffing.

---

## 15. CONS Interpretation

At the epistemic level:

```text
CAR =
  FS/GS/RS/US source quartet

CDR =
  integrity relation
```

For the compact profile:

```lisp
(
  (fs gs rs us)
  .
  (logos nomos pathos)
)
```

For the Miquel profile:

```lisp
(
  (fs gs rs us)
  .
  (
    logos- logos+
    nomos- nomos+
    pathos- pathos+
  )
)
```

This is a relational lowering, not a claim that every check is an independent semantic value.

At the stream level:

```text
CAR = current decoded COBS run
CDR = continuation to the next run
NULL = reconstructed zero boundary
```

The complete nested relation is:

```lisp
(
  (
    scope-source
    .
    integrity-surface
  )
  .
  next-run
)
```

Thus:

```text
epistemic CONS
  binds source to integrity

stream CONS
  binds run to continuation
```

---

# Part IV — Perceptron and Activation

## 16. COBS-CONS Miquel Perceptron

The complete deterministic unit MAY be called:

```text
COBS-CONS Miquel Epistemic Perceptron
```

Its structure is:

```text
four binary scope inputs
↓
eight-point extended encoding
↓
six binary Miquel incidence checks
↓
COBS-CONS carriage
↓
syndrome classification
↓
correction or rejection
↓
scope recovery
↓
weighted epistemic aggregation
↓
ternary activation
↓
validation
↓
receipt
```

It is a deterministic coded perceptron.

It is not, by itself, a trained statistical neural network.

The integrity stage uses exact `GF(2)` arithmetic.

A later aggregation stage MAY use fixed, declared, or learned weights.

---

## 17. Binary Integrity and Ternary Activation

The Miquel syndrome is binary:

```text
each circle check ∈ {0,1}
```

The activation MAY be ternary:

```text
A ∈ {-1, 0, +1}
```

Canonical interpretation:

```text
-1 = invalid, contradicted, malformed, or uncorrectable
 0 = lawful but unresolved candidate
+1 = validated and receipted state
```

Integrity correction alone MUST NOT produce `+1`.

Canonical order:

```text
integrity
→ correction
→ interpretation
→ validation
→ activation
→ receipt
```

A corrected but not yet validated candidate remains:

```text
0
```

An uncorrectable frame becomes:

```text
-1
```

A fully validated and receipted frame becomes:

```text
+1
```

---

## 18. Weighted Generalized Aggregation

Hamming and Miquel incidence do not compute a mean.

They compute exact parity constraints.

A weighted generalized mean MAY be applied only after the scope features have been recovered.

For recovered channel values:

```text
xFS, xGS, xRS, xUS
```

and nonnegative weights:

```text
wFS, wGS, wRS, wUS
```

define:

```text
M_p =
(
  (
    wFS × xFS^p
  + wGS × xGS^p
  + wRS × xRS^p
  + wUS × xUS^p
  )
  /
  (
    wFS + wGS + wRS + wUS
  )
)^(1/p)
```

The model MUST specify:

```text
channel domain
weight domain
value of p
normalization
thresholds
missing-channel behavior
```

A ternary quantizer MAY use:

```text
M_p < θ−        → -1
θ− ≤ M_p < θ+   →  0
M_p ≥ θ+        → +1
```

However, the final positive activation still requires validation and receipt.

---

# Part V — Validation and Invariants

## 19. Validation Boundary

A valid codeword does not establish semantic truth.

A valid COBS frame does not establish semantic truth.

A well-formed CONS relation does not establish semantic truth.

Canonical invariant:

```text
integrity is not acceptance
framing is not acceptance
scope is not acceptance
correction is not acceptance
projection is not acceptance
```

The complete authority order is:

```text
decode
classify
correct or reject
recover
resolve
interpret
validate
activate
receipt
```

---

## 20. Conformance Invariants

A conforming implementation MUST preserve:

```text
decode_cobs(encode_cobs(bytes)) = bytes
```

For the compact profile:

```text
decode_hamming(encode_hamming(scope4)) = scope4
```

For every single-bit corruption:

```text
decode_hamming(flip_one_bit(encode_hamming(scope4))) = scope4
```

provided the external frame-integrity witness passes.

For the Miquel profile:

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

## 21. Canonical Formulas

### Compact profile

```text
DATA =
  FS GS RS US

CHECK =
  LOGOS NOMOS PATHOS

CODE7 =
  Hamming743(DATA)
```

With:

```text
LOGOS  = FS XOR GS XOR US
NOMOS  = FS XOR RS XOR US
PATHOS = GS XOR RS XOR US
```

### Extended profile

```text
DATA =
  FS GS RS US

CODE8 =
  Miquel844(DATA)

CHECK6 =
  (
    LOGOS− LOGOS+
    NOMOS− NOMOS+
    PATHOS− PATHOS+
  )
```

Where:

```text
H_Miquel × CODE8^T = 0
```

over `GF(2)`.

---

## 22. Complete Layer Stack

```text
NUL
  origin and reconstructed COBS frame boundary

FS/GS/RS/US
  four-position pre-language scope topology

LOGOS/NOMOS/PATHOS
  three complementary integrity dimensions

Hamming [7,4,3]
  compact seven-position correction profile

Miquel / extended Hamming [8,4,4]
  canonical symmetric eight-position SECDED profile

CONS
  source/integrity and run/continuation relation

COBS
  deterministic zero-safe stream framing

F*
  operator or gauge dialect

OMI-Lisp / Lambda Canon Block
  candidate declaration surface

weighted aggregation
  optional post-integrity activation magnitude

ternary activation
  invalid / unresolved / accepted classification

validation
  authority decision

receipt
  durable accepted-state witness
```

---

## 23. Final Authority Statement

```text
LL/MM/NN is deprecated.

LOGOS/NOMOS/PATHOS replaces it as three derived integrity
dimensions over the four canonical FS/GS/RS/US scope features.

Hamming [7,4,3] remains the compact correction profile.

The Miquel configuration is the canonical geometric presentation
of the extended Hamming [8,4,4] integrity cell.

Its eight encoded positions are symmetric.
Its six four-point incidence circles form three complementary
LOGOS, NOMOS, and PATHOS pairs.

COBS preserves frame boundaries.
CONS preserves relational continuation.
Miquel incidence preserves extended-code integrity.
Weighted aggregation may determine candidate activation magnitude.
Validation and receipt alone accept state.
```

---

## 24. One-Sentence Summary

The Omnicron-Epistemic-Model encodes the four FS/GS/RS/US scope features through either a compact Hamming `[7,4,3]` cell or a canonical Miquel-presented extended Hamming `[8,4,4]` cell, transports those cells through COBS-CONS, classifies their integrity through LOGOS/NOMOS/PATHOS incidence, and only after correction, interpretation, validation, and receipt lowers the recovered state into a ternary epistemic activation.