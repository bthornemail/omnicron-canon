# LOGOS/NOMOS/PATHOS Hamming-Coded COBS-CONS

## Omnicron-Epistemic-Model Integration

**Status:** Canonical Defined Model
**Layer:** Omnicron COBS-CONS Integrity Surface
**Replaces:** Deprecated `LL/MM/NN` transition terminology
**Preserves:** `FS/GS/RS/US` as canonical pre-language scope topology

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

This replacement does not restore the older three-field argument model.

It introduces three finite check relations over the four canonical scope positions:

```text
FS
GS
RS
US
```

The complete epistemic code surface is:

```text
FS/GS/RS/US
+
LOGOS/NOMOS/PATHOS
=
7-position relational codeword
```

Canonical statement:

```text
FS/GS/RS/US carries scope.
LOGOS/NOMOS/PATHOS checks scope.
```

---

## 2. Authority Boundary

The four scope positions are authoritative memory-topology data:

```text
FS = file scope
GS = group scope
RS = record scope
US = unit scope
```

The three check positions are derived relations:

```text
LOGOS  = coherence relation
NOMOS  = ordering and boundary relation
PATHOS = continuity and carried-state relation
```

They MUST NOT be interpreted as additional scope levels.

They MUST NOT replace FS, GS, RS, or US.

They MUST be derived from the four scope-bearing data positions.

Therefore:

```text
scope is primary
check relation is derived
```

---

## 3. Hamming `[7,4,3]` Arrangement

The canonical seven-position arrangement uses the standard Hamming parity positions:

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

where:

```text
L = LOGOS
N = NOMOS
F = FS
P = PATHOS
G = GS
R = RS
U = US
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

---

## 4. Check Relations

Using even parity, the three relations are:

```text
LOGOS  = FS XOR GS XOR US
NOMOS  = FS XOR RS XOR US
PATHOS = GS XOR RS XOR US
```

Equivalently, each relation checks its Hamming incidence set:

```text
LOGOS checks positions:
  1, 3, 5, 7

NOMOS checks positions:
  2, 3, 6, 7

PATHOS checks positions:
  4, 5, 6, 7
```

The complete parity equations are:

```text
LOGOS XOR FS XOR GS XOR US = 0

NOMOS XOR FS XOR RS XOR US = 0

PATHOS XOR GS XOR RS XOR US = 0
```

These equations define a lawful seven-position epistemic codeword.

---

## 5. Epistemic Interpretation

The three relations have distinct roles.

### 5.1 LOGOS

LOGOS checks whether the selected scope content forms a coherent readable relation.

```text
LOGOS:
  Does the carried scope agree with its relational form?
```

Its incidence relation is:

```text
FS, GS, US
```

This connects:

```text
file
group
unit
```

as the readable relational path.

LOGOS does not decide truth.

It checks structural coherence.

---

### 5.2 NOMOS

NOMOS checks whether record and unit placement obey the declared scope law.

```text
NOMOS:
  Does the carried scope obey its boundary and ordering law?
```

Its incidence relation is:

```text
FS, RS, US
```

This connects:

```text
file
record
unit
```

as the normative boundary path.

NOMOS does not accept state.

It checks whether the scope arrangement obeys the declared structure.

---

### 5.3 PATHOS

PATHOS checks whether the carried unit remains continuous through group and record containment.

```text
PATHOS:
  Has the carried state remained connected through traversal?
```

Its incidence relation is:

```text
GS, RS, US
```

This connects:

```text
group
record
unit
```

as the continuity and carriage path.

PATHOS is not emotional authority.

It names the condition under which the carried state remains perceptible and continuous through the relation.

---
### Miquel Extended Encoding Rule

The Omnicron-Epistemic-Model SHALL use the Miquel configuration as the canonical geometric presentation of its extended Hamming `[8,4,4]` integrity cell.

The four canonical source features are:

```text
FS
GS
RS
US
```

These four source bits SHALL be encoded into eight symmetric point positions:

```text
P000 P001 P010 P011
P100 P101 P110 P111
```

The encoded positions SHALL be checked by six four-point incidence relations:

```text
LOGOS−  LOGOS+
NOMOS−  NOMOS+
PATHOS− PATHOS+
```

Each point SHALL lie on exactly one circle from each complementary pair.

Each circle SHALL contain exactly four points.

The resulting six-by-eight binary incidence matrix SHALL have rank four over `GF(2)`. Its kernel SHALL be the extended Hamming `[8,4,4]` code.

A zero syndrome SHALL indicate no detected corruption.

A single-point syndrome SHALL consist of exactly one failed circle from each LOGOS, NOMOS, and PATHOS pair. The three failed-circle selections SHALL identify the corrupted point.

A detected single-point corruption MAY be corrected, after which all six incidence checks MUST be recomputed.

A syndrome inconsistent with a single Miquel point, including a detected double-point corruption, MUST NOT be corrected as a single error. It MUST be rejected or retained as an unresolved candidate.

LOGOS, NOMOS, and PATHOS SHALL be interpreted as three complementary incidence dimensions, not as three independent stored parity bits.

COBS SHALL preserve frame boundaries.

CONS SHALL preserve relational continuation.

The Miquel configuration SHALL preserve extended-code incidence.

Validation and receipt alone SHALL accept state.

---

## 6. Syndrome

On reception, the decoder recomputes the three checks.

The syndrome is:

```text
sLOGOS
sNOMOS
sPATHOS
```

where:

```text
sLOGOS =
  LOGOS XOR FS XOR GS XOR US

sNOMOS =
  NOMOS XOR FS XOR RS XOR US

sPATHOS =
  PATHOS XOR GS XOR RS XOR US
```

The syndrome value is interpreted as:

```text
syndrome =
    sLOGOS
  + 2 × sNOMOS
  + 4 × sPATHOS
```

Therefore:

| Syndrome | Position | Meaning                      |
| -------: | -------: | ---------------------------- |
|    `000` |     none | no detected single-bit error |
|    `001` |        1 | LOGOS                        |
|    `010` |        2 | NOMOS                        |
|    `011` |        3 | FS                           |
|    `100` |        4 | PATHOS                       |
|    `101` |        5 | GS                           |
|    `110` |        6 | RS                           |
|    `111` |        7 | US                           |

A nonzero syndrome identifies the position of a presumed single-bit error.

Canonical correction rule:

```text
if syndrome != 0:
    flip codeword[syndrome]
```

After correction, all three relations MUST be recomputed.

---

## 7. Error-Correction Boundary

The Hamming `[7,4,3]` surface guarantees:

```text
single-bit error correction
```

It does not, by itself, safely distinguish every double-bit error from a single-bit error.

Therefore an Omnicron implementation MUST choose one of two profiles.

### Profile A: Hamming `[7,4,3]` with External Receipt Integrity

Use:

```text
Hamming [7,4,3]
+
frame length
+
receipt hash or checksum
```

Hamming corrects one local bit.

The receipt or frame-level integrity check rejects an incorrectly corrected multi-bit corruption.

### Profile B: Extended Hamming `[8,4,4]`

Add one overall parity bit:

```text
[LOGOS NOMOS FS PATHOS GS RS US OMNION]
```

where:

```text
OMNION =
  LOGOS XOR NOMOS XOR FS XOR PATHOS XOR GS XOR RS XOR US
```

This profile provides:

```text
single-error correction
double-error detection
```

Canonical distinction:

```text
[7,4,3] = SEC
[8,4,4] = SECDED
```

The extended bit MUST NOT be treated as a fifth scope or fourth epistemic principle.

It is only the total-codeword parity witness.

---

## 8. COBS-CONS Integration

COBS and Hamming occupy different layers.

```text
COBS:
  preserves stream framing and encoded zero boundaries

Hamming:
  preserves local four-bit feature integrity

CONS:
  preserves relational traversal

FS/GS/RS/US:
  preserves scope topology
```

Canonical stack:

```text
raw scope feature
↓
FS/GS/RS/US four-bit symbol
↓
derive LOGOS/NOMOS/PATHOS
↓
form seven-bit epistemic codeword
↓
pack codewords into bytes
↓
COBS encode the byte stream
↓
transport
↓
COBS decode
↓
unpack Hamming codewords
↓
syndrome check and correction
↓
recover FS/GS/RS/US
↓
reconstruct CONS relations
↓
validate
↓
receipt
```

COBS MUST be applied after the Hamming-coded features have been packed into bytes.

On reception, COBS MUST be decoded before Hamming codewords are interpreted.

---

## 9. COBS Feature Adjustment

Standard COBS operates on bytes.

The epistemic Hamming unit operates on four data bits and produces seven coded bits.

Therefore the implementation MUST define a deterministic bit-packing rule.

The recommended packing is two Hamming codewords per 16-bit carrier:

```text
bits 15..9 = codeword A
bit  8     = reserved or extension parity A

bits 7..1  = codeword B
bit  0     = reserved or extension parity B
```

For the `[7,4,3]` profile:

```text
bit 8 = 0
bit 0 = 0
```

For the extended `[8,4,4]` profile:

```text
bit 8 = OMNION_A
bit 0 = OMNION_B
```

This gives:

```text
two 4-bit scope symbols
→ one 16-bit encoded carrier
```

The 16-bit carrier is then serialized into two bytes according to the canonical OMI byte order.

COBS operates on those serialized bytes.

---

## 10. CONS Interpretation

The Hamming codeword may be represented as an epistemic CONS pair:

```text
(
  FS GS RS US
  .
  LOGOS NOMOS PATHOS
)
```

Canonical interpretation:

```text
CAR = four scope-bearing data positions
CDR = three derived relational checks
```

Therefore:

```text
CAR = what is carried
CDR = how continuation is checked
```

Expanded:

```lisp
(
  (fs gs rs us)
  .
  (logos nomos pathos)
)
```

This is not a conventional Lisp pair containing seven independent values.

It is an Omnicron relational lowering:

```text
scope quartet
paired with
derived integrity triad
```

The pair is lawful only when all three parity relations vanish.

---

## 11. COBS-CONS Run Relation

At the stream level:

```text
CAR = current decoded nonzero run
CDR = next COBS run
NULL = reconstructed zero boundary
```

Inside each decoded run:

```text
CAR = FS/GS/RS/US feature quartet
CDR = LOGOS/NOMOS/PATHOS check triad
```

This gives two nested CONS levels:

```text
stream CONS:
  run . continuation

epistemic CONS:
  scope . check
```

Canonical nesting:

```lisp
(
  ((fs gs rs us) . (logos nomos pathos))
  .
  next-run
)
```

Thus COBS-CONS preserves both:

```text
external stream continuity
internal epistemic coherence
```

---

## 12. Omnicron-Epistemic Quadrant

The four FS/GS/RS/US bits are not merely arbitrary message data.

They form the local four-position epistemic observation surface.

One canonical interpretation is:

```text
FS = enclosing source is visible
GS = relational grouping is visible
RS = record boundary is visible
US = carried unit is visible
```

LOGOS/NOMOS/PATHOS then inspect overlapping projections of that surface:

```text
LOGOS:
  source-group-unit coherence

NOMOS:
  source-record-unit law

PATHOS:
  group-record-unit continuity
```

This gives three intersecting views over one four-position scope object.

No check relation owns the whole object independently.

Their agreement establishes local codeword consistency.

---

## 13. Validation and Acceptance

A valid Hamming codeword does not establish semantic truth.

It establishes only that the local feature survived carriage according to the selected integrity profile.

Canonical invariant:

```text
Hamming validity is not semantic acceptance.
COBS validity is not semantic acceptance.
CONS well-formedness is not semantic acceptance.
Scope resolution is not semantic acceptance.
```

The complete authority order remains:

```text
decode
correct
resolve
interpret
validate
receipt
```

Only validation and receipt accept state.

---

## 14. Canonical Invariants

A conforming implementation MUST preserve:

```text
decode_cobs(encode_cobs(bytes)) = bytes
```

It MUST preserve:

```text
recover_hamming(encode_hamming(scope4)) = scope4
```

for an uncorrupted codeword.

For one corrupted bit, it MUST preserve:

```text
recover_hamming(flip_one_bit(encode_hamming(scope4))) = scope4
```

For the `[7,4,3]` profile, a frame-level integrity witness MUST guard against unrecognized multiple-bit corruption.

For the `[8,4,4]` profile, a detected double-bit error MUST be rejected and MUST NOT be corrected as a single-bit error.

The decoder MUST NOT allow an integrity correction to:

```text
create new scope
change address authority
accept a declaration
emit an accepted receipt without validation
```

---

## 15. Canonical Formula

```text
DATA =
  FS GS RS US

CHECK =
  LOGOS NOMOS PATHOS

CODE =
  Hamming(DATA, CHECK)
```

With:

```text
LOGOS  = FS XOR GS XOR US
NOMOS  = FS XOR RS XOR US
PATHOS = GS XOR RS XOR US
```

And:

```text
Omnicron Epistemic Cell =
  CONS(DATA, CHECK)
```

Expanded:

```text
Omnicron Epistemic Cell =
  (
    FS GS RS US
    .
    LOGOS NOMOS PATHOS
  )
```

---

## 16. Complete Layer Stack

```text
NUL
  origin and reconstructed frame boundary

FS/GS/RS/US
  four-position pre-language scope topology

LOGOS/NOMOS/PATHOS
  three-position Hamming integrity relation

CONS
  scope/check and run/continuation pairing

COBS
  zero-safe deterministic stream framing

F*
  operator or gauge dialect

OMI-Lisp / Lambda Canon Block
  candidate declaration surface

validation
  acceptance decision

receipt
  durable accepted-state witness
```

---

## 17. Final Authority Statement

```text
LL/MM/NN is deprecated.

LOGOS/NOMOS/PATHOS replaces it as a derived three-relation
integrity surface over the four canonical FS/GS/RS/US scope positions.

The resulting 4+3 arrangement forms an Omnicron Hamming [7,4,3]
epistemic codeword.

FS/GS/RS/US carries scope.
LOGOS/NOMOS/PATHOS checks the carried relation.
CONS preserves relational traversal.
COBS preserves stream boundaries.
Validation and receipt alone accept state.
```
