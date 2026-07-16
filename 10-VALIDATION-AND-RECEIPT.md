# 10-VALIDATION-AND-RECEIPT

## Validation and Receipt Boundaries

**Status:** Canonical authority
**Layer:** Omnicron authority boundaries
**Inherits:** 00-EXTENSION-AUTHORITY, 06-EPISTEMIC-ACTIVATION

---

## 1. Purpose

This document freezes the full authority order for the Omnicron system.

It defines the exact boundaries between integrity, correction, validation, and receipt.

---

## 2. Complete Authority Order

The complete authority order is:

```text
parse
  ↓
encode or decode
  ↓
classify integrity
  ↓
correct or reject
  ↓
recover scope
  ↓
reconstruct CONS
  ↓
resolve
  ↓
interpret
  ↓
aggregate
  ↓
validate
  ↓
activate
  ↓
receipt
```

---

## 3. Strongest Invariant

The strongest invariant is:

```text
integrity is not truth
correction is not acceptance
activation magnitude is not authority
projection is not receipt
```

---

## 4. Validation Boundary

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

---

## 5. Validation Rules

### 5.1 Validation Authority

Validation is an authority decision.

It determines whether a candidate is admissible.

It is not the same as integrity checking.

### 5.2 Validation Criteria

Validation MUST consider:

```text
scope correctness
relation well-formedness
contextual admissibility
policy compliance
```

### 5.3 Validation Result

The validation result is:

```text
rejected:
  candidate is not admissible

accepted:
  candidate is admissible
```

---

## 6. Receipt Boundary

Receipt is the durable record of accepted state.

It is not the same as validation.

It is not the same as projection.

### 6.1 Receipt Authority

Receipt is the final authority step.

It records accepted state.

It does not accept state.

### 6.2 Receipt Record

A receipt record MUST contain:

```text
scope snapshot
integrity result
validation result
activation state
timestamp (optional)
```

### 6.3 Receipt Invariant

```text
receipt alone records accepted state.
validation alone determines admissibility.
integrity alone restores candidates.
projection alone displays state.
```

---

## 7. Authority Separation

The following must never be confused:

```text
integrity
  restores candidates

correction
  repairs candidates

validation
  determines admissibility

activation
  classifies state

receipt
  records accepted state

projection
  displays state
```

---

## 8. Non-Authority Defaults

The following MUST NOT be confused:

```text
decode success does not validate
correction success does not accept
activation candidate does not receipt
projection does not accept
interpretation does not validate
```

---

## 9. Canonical Order

The canonical order is:

```text
integrity
  ↓
correction
  ↓
interpretation
  ↓
validation
  ↓
activation
  ↓
receipt
```

Each step has its own authority.

No step may replace another step.

---

## 10. Canonical Lock

```text
integrity is not truth
correction is not acceptance
activation magnitude is not authority
projection is not receipt

Validation determines admissibility.
Receipt alone records accepted state.

The authority order is:
  integrity → correction → interpretation → validation → activation → receipt
```