# 08-OMNICRON-ISA

## Omnicron-ISA

**Status:** Canonical authority
**Layer:** Omnicron execution semantics
**Inherits:** 00-EXTENSION-AUTHORITY, 02-EPISTEMIC-CELL, 05-MIQUEL-INTEGRITY, 01-COBS-CONS

---

## 1. Purpose

This document defines the behaviors of the Omnicron-ISA before opcode numbers.

The Omnicron-ISA extends OMI-ISA with instructions for encoding, decoding, integrity checking, and activation.

---

## 2. Required Operations

The following operations are required:

```text
SCOPE_PACK
SCOPE_UNPACK

H743_ENCODE
H743_DECODE

M844_ENCODE
M844_CHECK
M844_CORRECT
M844_DECODE

COBS_ENCODE
COBS_DECODE

CONS_LINK
CONS_NEXT

ACTIVATE3
```

The names may change, but each operation needs:

```text
input types
output types
flags
failure conditions
state effects
authority effects
```

---

## 3. Scope Operations

### 3.1 SCOPE_PACK

```text
input:
  FS, GS, RS, US ∈ {0, 1}

output:
  Scope4 ∈ GF(2)^4

flags:
  none

failure conditions:
  none (all inputs are binary)

state effects:
  produces Scope4 from four binary inputs

authority effects:
  none
```

### 3.2 SCOPE_UNPACK

```text
input:
  Scope4 ∈ GF(2)^4

output:
  FS, GS, RS, US ∈ {0, 1}

flags:
  none

failure conditions:
  none (Scope4 is always valid)

state effects:
  extracts four binary features from Scope4

authority effects:
  none
```

---

## 4. Compact Hamming Operations

### 4.1 H743_ENCODE

```text
input:
  Scope4 ∈ GF(2)^4

output:
  CompactCell7 ∈ GF(2)^7

flags:
  none

failure conditions:
  none (encoding always succeeds)

state effects:
  produces CompactCell7 from Scope4

authority effects:
  none
```

### 4.2 H743_DECODE

```text
input:
  CompactCell7 ∈ GF(2)^7

output:
  Scope4 ∈ GF(2)^4 ∪ {⊥}

flags:
  CORRECTED: correction was applied
  UNCORRECTABLE: error cannot be corrected

failure conditions:
  syndrome does not match any valid pattern
  external frame-integrity witness fails

state effects:
  recovers Scope4 or indicates failure

authority effects:
  none
```

---

## 5. Miquel Operations

### 5.1 M844_ENCODE

```text
input:
  Scope4 ∈ GF(2)^4

output:
  MiquelCell8 ∈ GF(2)^8

flags:
  none

failure conditions:
  none (encoding always succeeds)

state effects:
  produces MiquelCell8 from Scope4

authority effects:
  none
```

### 5.2 M844_CHECK

```text
input:
  MiquelCell8 ∈ GF(2)^8

output:
  Syndrome6 ∈ GF(2)^6

flags:
  ZERO: no error detected
  SINGLE: single-point error detected
  MULTI: multi-point error detected

failure conditions:
  none (check always succeeds)

state effects:
  computes six circle checks

authority effects:
  none
```

### 5.3 M844_CORRECT

```text
input:
  MiquelCell8 ∈ GF(2)^8
  Syndrome6 ∈ GF(2)^6

output:
  MiquelCell8 ∈ GF(2)^8

flags:
  CORRECTED: correction was applied
  UNCORRECTABLE: error cannot be corrected

failure conditions:
  syndrome does not match any valid pattern
  correction does not produce zero syndrome

state effects:
  flips identified point if correctable

authority effects:
  none
```

### 5.4 M844_DECODE

```text
input:
  MiquelCell8 ∈ GF(2)^8

output:
  Scope4 ∈ GF(2)^4 ∪ {⊥}

flags:
  CORRECTED: correction was applied
  UNCORRECTABLE: error cannot be corrected

failure conditions:
  uncorrectable error

state effects:
  recovers Scope4 or indicates failure

authority effects:
  none
```

---

## 6. COBS Operations

### 6.1 COBS_ENCODE

```text
input:
  bytes

output:
  encoded_bytes

flags:
  none

failure conditions:
  none (encoding always succeeds)

state effects:
  applies COBS stuffing

authority effects:
  none
```

### 6.2 COBS_DECODE

```text
input:
  encoded_bytes

output:
  bytes

flags:
  none

failure conditions:
  malformed COBS frame
  truncated frame

state effects:
  removes COBS stuffing

authority effects:
  none
```

---

## 7. CONS Operations

### 7.1 CONS_LINK

```text
input:
  car: any value
  cdr: any value

output:
  pair: (car . cdr)

flags:
  none

failure conditions:
  none (CONS always succeeds)

state effects:
  creates a CONS pair

authority effects:
  none
```

### 7.2 CONS_NEXT

```text
input:
  pair: (car . cdr)

output:
  cdr: any value

flags:
  none

failure conditions:
  none (CDR always succeeds)

state effects:
  extracts continuation from pair

authority effects:
  none
```

---

## 8. Activation Operation

### 8.1 ACTIVATE3

```text
input:
  integrity_result: {-1, 0, +1}
  validation_result: {rejected, accepted}

output:
  activation: {-1, 0, +1}

flags:
  none

failure conditions:
  none

state effects:
  computes ternary activation

authority effects:
  none
```

The activation rules:

```text
if integrity_result = -1:
  activation = -1

if integrity_result = 0 and validation_result = rejected:
  activation = -1

if integrity_result = 0 and validation_result = accepted:
  activation = +1
```

---

## 9. Canonical Non-Authority Rule

The following must never be confused:

```text
decode success does not validate
correction success does not accept
activation candidate does not receipt
```

The implementation can later assign fixed opcode values.

---

## 10. Deterministic Replay

The Omnicron-ISA MUST preserve deterministic replay.

For the same input, the output must be identical.

The execution must be reproducible.

---

## 11. Fixed-Width Execution

The Omnicron-ISA MUST preserve fixed-width execution.

Each operation has a defined input and output size.

The execution time must be bounded.

---

## 12. Non-Authority Defaults

The Omnicron-ISA MUST preserve non-authority defaults.

Operations do not validate.

Operations do not accept state.

Operations do not receipt.

---

## 13. Separation of Concerns

The Omnicron-ISA MUST separate:

```text
correction from validation
activation from receipt
```

Correction restores candidates.

Validation determines admissibility.

Activation classifies state.

Receipt records accepted state.

---

## 14. Canonical Lock

```text
Omnicron-ISA defines behaviors before opcode numbers.

Required operations:
  SCOPE_PACK, SCOPE_UNPACK
  H743_ENCODE, H743_DECODE
  M844_ENCODE, M844_CHECK, M844_CORRECT, M844_DECODE
  COBS_ENCODE, COBS_DECODE
  CONS_LINK, CONS_NEXT
  ACTIVATE3

Canonical non-authority rule:
  decode success does not validate
  correction success does not accept
  activation candidate does not receipt
```