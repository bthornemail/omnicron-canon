# 07-OMNICRON-PORT

## Omnicron-Port

**Status:** Canonical authority
**Layer:** Omnicron route declaration
**Inherits:** 00-EXTENSION-AUTHORITY, 02-EPISTEMIC-CELL, 01-COBS-CONS

---

## 1. Purpose

This document defines Omnicron-Port, the dormant route declaration surface for the Omnicron system.

Omnicron-Port extends OMI-Port with codec profiles, encoded cells, and integrity state.

---

## 2. OMI-Port Inheritance

OMI-Port already defines a dormant route declaration rather than an active connection.

The inherited route is:

```text
source × target × F* gauge
→ OMI-IMO route candidate
```

OMI-Port explicitly declares routes without connecting, validating, accepting, or receipting them.

---

## 3. Omnicron-Port Extension

Omnicron-Port adds:

```text
codec profile
encoded-cell profile
COBS frame declaration
integrity state
correction state
activation candidate
```

It MUST preserve:

```text
accepted  = 0
validated = 0
receipted = 0
```

---

## 4. Canonical Transform

The OMI transform is:

```text
PortTensor_G(source, target)
→ OMI-IMO route candidate
```

The Omnicron transform is:

```text
OmnicronPortTensor_G,C(source, target)
→ encoded COBS-CONS route candidate
```

where:

```text
G = F* gauge
C = integrity/codec profile
```

For example:

```text
C = H743
C = MIQUEL844
```

The gauge still selects how the source-target pleth is read; it does not become validation authority.

---

## 5. Omnicron-Port Object Model

A useful canonical shape is:

```c
typedef enum {
    OMNICRON_CODEC_HAMMING_743 = 0,
    OMNICRON_CODEC_MIQUEL_844  = 1
} Omnicron_CodecProfile;

typedef enum {
    OMNICRON_CELL_INVALID      = -1,
    OMNICRON_CELL_UNRESOLVED   = 0,
    OMNICRON_CELL_VALID        = 1
} Omnicron_CellState;

typedef struct {
    OMI_PortRoute base;

    Omnicron_CodecProfile codec;

    uint8_t encoded_cell;
    uint8_t syndrome[6];

    uint8_t corrected;
    uint8_t correction_index;
    uint8_t detected_double_error;

    Omnicron_CellState state;
} Omnicron_PortRoute;
```

Required inherited defaults remain:

```text
accepted  = 0
validated = 0
receipted = 0
```

---

## 6. Omnicron-Port Fields

### 6.1 Base Fields (Inherited from OMI-Port)

```text
source:
  URI-CIDR source scope

target:
  URI-CIDR target scope

F* gauge:
  operator or gauge dialect

FS/GS/RS/US route:
  scope route

OMI-IMO candidate:
  route candidate
```

### 6.2 Extension Fields (Omnicron-Port)

```text
codec:
  integrity profile (H743 or MIQUEL844)

encoded_cell:
  the encoded epistemic cell

syndrome:
  integrity syndrome (up to 6 checks)

corrected:
  whether correction was applied

correction_index:
  index of corrected point

detected_double_error:
  whether double error detected

state:
  cell state (INVALID, UNRESOLVED, VALID)
```

---

## 7. Authority Boundary

Omnicron-Port:

```text
declares routes
declares codec profiles
declares integrity state

does NOT validate
does NOT accept state
does NOT receipt
```

The dormant declaration boundary is preserved.

---

## 8. ABI Requirements

The current OMI-Port ABI is intentionally:

```text
strict C99
non-I/O
no atomics
no runtime connection authority
```

These requirements should be retained for the Omnicron-Port base ABI.

---

## 9. Canonical Lock

```text
Omnicron-Port extends OMI-Port with codec profiles and integrity state.

It preserves the dormant declaration boundary:
  accepted  = 0
  validated = 0
  receipted = 0

The gauge selects how the source-target pleth is read.
The codec profile selects the integrity encoding.
Validation and receipt remain external.
```