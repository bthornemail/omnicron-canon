# 09-OMNICRON-LISP

## Omnicron-Lisp

**Status:** Canonical authority
**Layer:** Omnicron readable syntax
**Inherits:** 00-EXTENSION-AUTHORITY, 02-EPISTEMIC-CELL, 08-OMNICRON-ISA

---

## 1. Purpose

This document defines Omnicron-Lisp, a language profile over OMI-Lisp.

Omnicron-Lisp is not an unrelated language.

It is OMI-Lisp plus explicit codec, integrity, scope-cell, and activation forms.

---

## 2. OMI-Lisp Inheritance

OMI-Lisp provides:

```text
readable relational declaration
CONS pairs
CAR/CDR traversal
NULL boundary
```

Omnicron-Lisp inherits all OMI-Lisp forms.

---

## 3. Omnicron-Lisp Extension

Omnicron-Lisp adds:

```text
explicit codec declarations
scope cell forms
integrity check forms
activation state forms
```

---

## 4. Canonical Surface

Example canonical surface:

```lisp
(omnicron
  (scope
    (fs 1)
    (gs 0)
    (rs 1)
    (us 0))
  (codec miquel-844)
  (cons payload continuation))
```

A more compact declarative form:

```lisp
(cell
  :scope  #b1010
  :codec  miquel-844
  :state  unresolved)
```

A decoded and inspected representation:

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

---

## 5. Scope Forms

### 5.1 Scope Declaration

```lisp
(scope
  (fs <value>)
  (gs <value>)
  (rs <value>)
  (us <value>))
```

where `<value>` is 0 or 1.

### 5.2 Scope Bit Vector

```lisp
(scope #bFSGSRSUS)
```

Example:

```lisp
(scope #b1010)
```

defines:

```text
FS = 1
GS = 0
RS = 1
US = 0
```

---

## 6. Codec Forms

### 6.1 Compact Profile

```lisp
(codec hamming-743)
```

### 6.2 Extended Profile

```lisp
(codec miquel-844)
```

---

## 7. Cell Forms

### 7.1 Cell Declaration

```lisp
(cell
  :scope <scope>
  :codec <codec>
  :state <state>)
```

where:

```text
<scope> = scope declaration
<codec> = codec profile
<state> = unresolved | valid | invalid
```

### 7.2 Cell with Integrity

```lisp
(cell
  :scope (scope #b1010)
  :codec miquel-844
  :integrity
    ((logos- 1)
     (logos+ 0)
     (nomos- 1)
     (nomos+ 0)
     (pathos- 1)
     (pathos+ 0)))
```

---

## 8. CONS Forms

### 8.1 Epistemic CONS

```lisp
(cons scope integrity)
```

Example:

```lisp
(cons
  (fs gs rs us)
  (logos nomos pathos))
```

### 8.2 Stream CONS

```lisp
(cons run continuation)
```

Example:

```lisp
(cons
  (cell :scope (scope #b1010) :codec miquel-844)
  next-run)
```

---

## 9. Activation Forms

### 9.1 Activation State

```lisp
(activation <value>)
```

where `<value>` is:

```text
-1 = invalid
 0 = unresolved
+1 = valid
```

### 9.2 Activation Declaration

```lisp
(activation
  (cell :scope (scope #b1010) :codec miquel-844)
  :state +1)
```

---

## 10. Lowering

The lowering path is:

```text
Omnicron-Lisp
  ↓
OMI-compatible lexer/parser
  ↓
Omnicron AST annotations
  ↓
scope quartet extraction
  ↓
Miquel encoding
  ↓
byte packing
  ↓
COBS encoding
  ↓
Omnicron-ISA instruction stream
  ↓
VM execution
  ↓
candidate activation
  ↓
validation and receipt
```

---

## 11. Parser Reuse

The original OMI-Lisp parser and compiler can likely be reused substantially.

The extension should be concentrated in:

```text
AST node kinds
codec annotations
new lowering rules
new instructions
new test fixtures
```

rather than replacing the whole compiler.

---

## 12. Notation Inheritance

OMI-IMO notation remains inherited:

```text
omi---imo
```

and:

```text
o-FS-GS-RS-US/FS/GS/RS/US?REGISTER?STACK@CAR@CDR
```

because the extension changes carriage and integrity, not the foundational route topology.

---

## 13. Canonical Lock

```text
Omnicron-Lisp is a language profile over OMI-Lisp.

It adds explicit codec, integrity, scope-cell, and activation forms.

It does not replace OMI-Lisp.
It inherits OMI-Lisp syntax and semantics.

The OMI-IMO notation remains inherited.
The extension changes carriage and integrity, not route topology.
```