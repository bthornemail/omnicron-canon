# 06-LL-MM-NN-DELTA-RING

## LL/MM/NN Temporal Delta Window

**Status:** Canonical authority
**Layer:** Omnicron temporal delta window
**Inherits:** 00-EXTENSION-AUTHORITY, 01-COBS-CONS

---

## 1. Purpose

This document defines the canonical temporal delta window of the Gnomic Omicron gauge ring.

```text
LL = previous delta
MM = present delta
NN = forward delta
```

LL/MM/NN are NOT deprecated names.

They are canonical temporal-delta coordinates.

They do not replace FS/GS/RS/US.

---

## 2. Canonical Separation

Three independent coordinate families:

```text
Scope4:
  (FS, GS, RS, US)
  epistemic scope coordinates

DeltaWindow:
  (LL, MM, NN)
  previous / present / forward delta values

Integrity3:
  (LOGOS, NOMOS, PATHOS)
  integrity and relational axes
```

These are not competing names for the same fields.

---

## 3. DeltaPosition vs DeltaWindow

DeltaPosition is an enum selecting which temporal slot is active:

```c
typedef enum {
    OMNICRON_DELTA_LL = 0, /* previous */
    OMNICRON_DELTA_MM = 1, /* present */
    OMNICRON_DELTA_NN = 2  /* forward */
} OmnicronDeltaPosition;
```

DeltaWindow holds all three delta values simultaneously:

```c
typedef struct {
    uint8_t ll; /* previous delta */
    uint8_t mm; /* present delta */
    uint8_t nn; /* forward delta */
} OmnicronDeltaWindow;
```

The active-position enum can remain separate:

```c
typedef enum {
    OMNICRON_DELTA_LL = 0,
    OMNICRON_DELTA_MM = 1,
    OMNICRON_DELTA_NN = 2
} OmnicronDeltaPosition;
```

This distinction matters because:

```text
LL-MM-NN
```

describes the relation among previous, present, and forward deltas, not just one selected label.

---

## 4. Temporal Correspondence

Each delta position maps to an integrity axis:

```text
LL(previous)  is evaluated through LOGOS
MM(present)   is evaluated through NOMOS
NN(forward)   is evaluated through PATHOS
```

Canonical association:

```c
static const OmnicronIntegrityAxis OMNICRON_DELTA_AXIS[3] = {
    OMNICRON_AXIS_LOGOS,   /* LL */
    OMNICRON_AXIS_NOMOS,   /* MM */
    OMNICRON_AXIS_PATHOS   /* NN */
};
```

---

## 5. Operational Integrity Checks

The integrity axes are relational, not static properties:

```c
LogosResult  logos_check(const DeltaValue* ll, const DeltaValue* mm);
NomosResult  nomos_check(const DeltaValue* mm);
PathosResult pathos_check(const DeltaValue* mm, const DeltaValue* nn);
```

Where:

```text
LOGOS(LL, MM)
  continuity proof from previous to present

NOMOS(MM)
  present admissibility or rule satisfaction

PATHOS(MM, NN)
  forward projection compatibility
```

This preserves their role as relational axes.

---

## 6. Sliding Window Semantics

The default profile is sliding window (not cyclic ring):

```text
LL → MM → NN
```

After advancement:

```text
LL' = MM
MM' = NN
NN' = newly projected delta
```

This is a sliding temporal window, not literal causal travel from future back to past.

The window advances without rewriting history.

---

## 7. Delta Window Interpretation

A continuation can be represented as:

```text
LL --Δ→ MM --Δ→ NN
```

where:

```text
LL
  retained or inherited relation

MM
  presently resolved candidate

NN
  projected or continued relation
```

And the three axes constrain the transition:

```text
LOGOS(LL, MM)
  checks continuity from previous to present

NOMOS(MM)
  checks admissibility at the present delta

PATHOS(MM, NN)
  checks projection from present to forward
```

This gives a clearer reading than treating LOGOS/NOMOS/PATHOS as only static parity names.

---

## 8. Formal Types

```c
typedef enum {
    OMNICRON_DELTA_LL = 0, /* previous */
    OMNICRON_DELTA_MM = 1, /* present */
    OMNICRON_DELTA_NN = 2  /* forward */
} OmnicronDeltaPosition;

typedef enum {
    OMNICRON_AXIS_LOGOS  = 0,
    OMNICRON_AXIS_NOMOS  = 1,
    OMNICRON_AXIS_PATHOS = 2
} OmnicronIntegrityAxis;

typedef struct {
    uint8_t ll; /* previous delta */
    uint8_t mm; /* present delta */
    uint8_t nn; /* forward delta */
} OmnicronDeltaWindow;

typedef enum {
    OMNICRON_CHECK_FAILED  = -1,
    OMNICRON_CHECK_PENDING = 0,
    OMNICRON_CHECK_PASSED  = 1
} OmnicronCheckState;
```

---

## 9. Delta Window Representation

DeltaWindow may be represented as:

One-hot encoding for position:

```text
LL MM NN
100 = previous
010 = present
001 = forward
```

Or enum value:

```text
0 = LL
1 = MM
2 = NN
```

The canon freezes the enum representation for position selection.

---

## 10. COBS-CONS with the Delta Window

The framed relation becomes:

```text
FΔ[
  LL : previous
  MM : present
  NN : forward
]
```

or operationally:

```text
LL
  → COBS-CONS transition
MM
  → COBS-CONS continuation
NN
```

The gauge ring can select or mark the active temporal position:

```text
FΔ_LL
FΔ_MM
FΔ_NN
```

A possible carrier-neutral frame is:

```text
FΔ(LL)
  encoded previous relation
FΔ(MM)
  encoded present relation
FΔ(NN)
  encoded forward relation
```

The concrete octet representation remains a carrier profile; FΔ, LL, MM, and NN should not yet be assumed to be literal single-byte values.

---

## 11. Relation to Ternary Activation

The temporal delta and activation state are distinct:

```text
LL / MM / NN
  where the relation lies temporally

-1 / 0 / +1
  epistemic activation classification
```

For example:

```text
LL:
  previously accepted relation

MM:
  currently unresolved candidate

NN:
  forward positive projection
```

This does NOT mean:

```text
LL = -1
MM = 0
NN = +1
```

unless a specific profile explicitly defines that mapping. Temporal position and epistemic state are independent axes.

A state may therefore be:

```text
(delta = LL, activation = +1)
(delta = MM, activation = 0)
(delta = NN, activation = 0)
```

---

## 12. Relation to Projection

FS/GS/RS/US determines what part of a relation is projected.

LL/MM/NN determines which temporal delta is being viewed.

```text
project(
  relation,
  delta = NN,
  scope_mask = FS|RS
)
```

means:

```text
show the file/source and record portions
of the forward delta projection
```

It still does not validate or receipt the projection.

---

## 13. Revised Data Model

```c
typedef struct {
    uint8_t scope4;       /* FS GS RS US */
    OmnicronDeltaWindow delta_window;  /* LL MM NN */
    uint8_t integrity3;   /* LOGOS NOMOS PATHOS */
    int8_t activation;    /* -1, 0, +1 */

    uint8_t accepted;
    uint8_t validated;
    uint8_t receipted;
} OmnicronEpistemicState;
```

---

## 14. Canonical Lock

```text
LL-MM-NN is a three-value temporal delta window.

LL holds the previous delta.
MM holds the present delta.
NN holds the forward delta.

LOGOS checks continuity from LL to MM.
NOMOS checks admissibility at MM.
PATHOS checks projection from MM to NN.

The window advances without rewriting history:

  LL' = MM
  MM' = NN
  NN' = newly projected delta

Scope4 remains independent of Delta3.

FS, GS, RS, and US remain the independent
four-position epistemic scope.

FΔ frames or advances the delta relation.

Temporal continuation, integrity, activation,
validation, and receipt remain distinct operations.
```

---

## 15. Historical Note

Any document saying:

```text
LL/MM/NN are deprecated
```

is now superseded.

The corrected doctrine is:

```text
LL/MM/NN are canonical temporal-delta coordinates.

They do not replace FS/GS/RS/US.

FS/GS/RS/US define epistemic scope.

LL/MM/NN define previous, present, and forward delta position.

LOGOS/NOMOS/PATHOS govern the corresponding delta axes.

FΔ identifies the Gnomic Omicron gauge-ring transition.
```
