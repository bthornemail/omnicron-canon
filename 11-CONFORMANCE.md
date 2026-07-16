# 11-CONFORMANCE

## Conformance Profiles and Vectors

**Status:** Canonical authority
**Layer:** Omnicron conformance requirements
**Inherits:** 00-EXTENSION-AUTHORITY through 10-VALIDATION-AND-RECEIPT

---

## 1. Purpose

This document defines conformance profiles and required test vectors for the Omnicron system.

Conformance is divided into profiles to allow incremental implementation.

---

## 2. Conformance Profiles

### 2.1 Core Profile

```text
FS/GS/RS/US
CONS
authority flags
validation boundary
receipt boundary
```

A core profile implementation MUST:

```text
preserve FS/GS/RS/US scope topology
preserve CONS pair structure
preserve authority flags
preserve validation boundary
preserve receipt boundary
```

### 2.2 Compact Profile

```text
Hamming [7,4,3]
external frame-integrity witness
```

A compact profile implementation MUST:

```text
encode and decode Hamming [7,4,3]
correct single-bit errors
detect multi-bit errors
use external frame-integrity witness
```

### 2.3 Extended Profile

```text
Miquel / extended Hamming [8,4,4]
single-error correction
double-error detection
```

An extended profile implementation MUST:

```text
encode and decode Miquel [8,4,4]
correct single-point errors
detect double-point errors
use six-circle incidence checks
```

### 2.4 Stream Profile

```text
COBS encode/decode
external NUL delimiter
canonical frame termination
```

A stream profile implementation MUST:

```text
encode and decode COBS
preserve external NUL delimiter
use canonical frame termination
```

### 2.5 Language Profile

```text
Omnicron-Lisp parsing and lowering
```

A language profile implementation MUST:

```text
parse Omnicron-Lisp syntax
lower to Omnicron-ISA
preserve OMI-Lisp inheritance
```

### 2.6 ISA Profile

```text
deterministic executable semantics
```

An ISA profile implementation MUST:

```text
preserve deterministic replay
preserve fixed-width execution
preserve non-authority defaults
```

---

## 3. Required Vectors

### 3.1 Scope Vectors

```text
all 16 source quartets
```

For each `(FS, GS, RS, US) ∈ GF(2)^4`:

```text
(0,0,0,0) (0,0,0,1) (0,0,1,0) (0,0,1,1)
(0,1,0,0) (0,1,0,1) (0,1,1,0) (0,1,1,1)
(1,0,0,0) (1,0,0,1) (1,0,1,0) (1,0,1,1)
(1,1,0,0) (1,1,0,1) (1,1,1,0) (1,1,1,1)
```

### 3.2 Miquel Codewords

```text
all 16 valid Miquel codewords
```

For each source quartet, the corresponding valid Miquel cell.

### 3.3 Single-Bit Corruptions

```text
all 128 single-bit corruptions
```

For each of 16 source quartets × 8 bit positions:

```text
16 × 8 = 128
```

Each MUST be correctable.

### 3.4 Two-Bit Corruptions

```text
all 448 distinct two-bit corruption cases
```

For each of 16 source quartets × C(8,2) bit pairs:

```text
16 × 28 = 448
```

Each MUST be detected and rejected.

### 3.5 COBS Vectors

```text
COBS empty frame
COBS embedded-zero frames
COBS 254-byte run
malformed code-byte zero
truncated frame
```

### 3.6 CONS Vectors

```text
CONS continuation failure
```

### 3.7 Activation Vectors

```text
activation boundary cases
```

For each of:

```text
integrity = -1 → activation = -1
integrity = 0, validation = rejected → activation = -1
integrity = 0, validation = accepted → activation = +1
```

---

## 4. Conformance Requirements

A conforming implementation MUST:

```text
pass all required vectors for its claimed profiles
document which profiles it implements
preserve all invariants defined in the canonical spine
```

A conforming implementation MUST NOT:

```text
claim a profile it does not implement
skip required test vectors
violate authority boundaries
```

---

## 5. Conformance Statement

A conformance statement MUST include:

```text
implementation name
version
claimed profiles
test results
```

Example:

```text
implementation: omnicron-reference-impl
version: 1.0.0
profiles: core, compact, extended, stream
test results: all vectors pass
```

---

## 6. Canonical Lock

```text
Conformance is divided into profiles:
  core, compact, extended, stream, language, ISA

Required vectors include:
  all 16 source quartets
  all 16 valid Miquel codewords
  all 128 single-bit corruptions
  all 448 distinct two-bit corruption cases
  COBS empty frame
  COBS embedded-zero frames
  COBS 254-byte run
  malformed code-byte zero
  truncated frame
  CONS continuation failure
  activation boundary cases

A conforming implementation MUST pass all required vectors
for its claimed profiles.
```