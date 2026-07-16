# 06-EPISTEMIC-ACTIVATION

## Ternary Epistemic Activation

**Status:** Canonical authority
**Layer:** Omnicron activation model
**Inherits:** 02-EPISTEMIC-CELL, 05-MIQUEL-INTEGRITY

---

## 1. Purpose

This document defines the ternary epistemic activation model.

The activation model classifies the state of an epistemic cell after integrity processing, correction, and validation.

---

## 2. Ternary Activation

The canonical activation is:

```text
-1 = invalid, contradicted, malformed, or uncorrectable
 0 = lawful but unresolved candidate
+1 = validated and receipted state
```

The integrity result is not itself the activation.

---

## 3. Activation States

### 3.1 Invalid (−1)

```text
-1 = invalid, contradicted, malformed, or uncorrectable
```

This state indicates:

```text
uncorrectable integrity error
malformed frame
contradicted scope
```

An invalid cell MUST NOT be corrected as a single-point error.

It MUST be rejected or retained as unresolved diagnostic state.

### 3.2 Unresolved (0)

```text
0 = lawful but unresolved candidate
```

This state indicates:

```text
integrity corrected successfully
scope recovered successfully
but validation not yet performed
```

A corrected but not yet validated candidate remains:

```text
0
```

### 3.3 Validated (+1)

```text
+1 = validated and receipted state
```

This state indicates:

```text
integrity corrected successfully
scope recovered successfully
validation accepted
receipt recorded
```

Integrity correction alone MUST NOT produce `+1`.

Only validation and receipt produce `+1`.

---

## 4. Activation Pipeline

The complete activation pipeline is:

```text
binary syndrome
  ↓
correction classification
  ↓
recovered scope
  ↓
optional weighted aggregation
  ↓
validation
  ↓
ternary activation
  ↓
receipt
```

The integrity result is not itself the activation.

---

## 5. Activation Rules

### 5.1 Uncorrectable Error

```text
syndrome does not match any valid pattern
  ↓
activation = -1
```

### 5.2 Correctable Error

```text
syndrome matches one point
correction succeeds
all checks vanish
  ↓
activation = 0 (candidate)
```

### 5.3 Validated State

```text
activation = 0 (candidate)
validation accepts
receipt recorded
  ↓
activation = +1
```

---

## 6. Weighted Generalized Aggregation

The weighted generalized mean MUST remain optional and separately parameterized.

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

---

## 7. Aggregation Parameters

The model MUST specify:

```text
weights
p exponent
normalization
thresholds
missing-value behavior
```

No default weights or thresholds should be called canonical until they are explicitly defined.

---

## 8. Ternary Quantizer

A ternary quantizer MAY use:

```text
M_p < θ−        → -1
θ− ≤ M_p < θ+   →  0
M_p ≥ θ+        → +1
```

However, the final positive activation still requires validation and receipt.

---

## 9. Activation vs. Integrity

The integrity result is not itself the activation.

```text
binary syndrome
  ↓
correction classification
  ↓
recovered scope
  ↓
optional weighted aggregation
  ↓
validation
  ↓
ternary activation
  ↓
receipt
```

Integrity correction alone MUST NOT produce `+1`.

Correction restores candidates.

Validation determines admissibility.

Receipt alone records accepted state.

---

## 10. Canonical Lock

```text
-1 = invalid, contradicted, malformed, or uncorrectable
 0 = lawful but unresolved candidate
+1 = validated and receipted state

Integrity correction alone MUST NOT produce +1.
Correction restores candidates.
Validation determines admissibility.
Receipt alone records accepted state.
```