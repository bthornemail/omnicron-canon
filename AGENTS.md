# AGENTS

## What This Repo Is

This is the normative extension authority for the **Omnicron system**.

It extends OMI without replacing it.

The canonical spine defines the Omnicron extension in 12 numbered documents (00-11).

## Repo Structure

- `00-EXTENSION-AUTHORITY.md` through `11-CONFORMANCE.md` — canonical spine
- `dev-docs/` — historical derivation records (not canonical)
- `README.md` — repository overview
- `AGENTS.md` — this file

## Key Conventions

- Canonical notation: `omi---imo?O_o`
- Scope positions: `FS/GS/RS/US`
- Integrity dimensions: `LOGOS/NOMOS/PATHOS`
- Compact profile: Hamming `[7,4,3]`
- Extended profile: Miquel `[8,4,4]`
- Activation: `{-1, 0, +1}`
- Authority order: integrity → correction → interpretation → validation → activation → receipt

## Authority Rules

### Inheritance

```text
where Omnicron is silent: OMI governs
where Omnicron explicitly extends OMI: Omnicron governs the extension only
where an implementation conflicts with canon: canon governs
```

### Non-Authority

```text
decode success does not validate
correction success does not accept
activation candidate does not receipt
projection does not accept
interpretation does not validate
```

### Strongest Invariant

```text
integrity is not truth
correction is not acceptance
activation magnitude is not authority
projection is not receipt
```

## What to Be Careful About

- Do not confuse Omicron (CONS determinism) with Omnicron (CONS + COBS determinism)
- Do not treat integrity checking as validation
- Do not treat correction as acceptance
- Do not treat activation as receipt
- Do not confuse control bytes (0x1C-0x1F) with scope bits (FS/GS/RS/US)
- The 8-tuple `Q Σ L R δ s t r` is a pedagogical scaffold, not canonical structure

## Modifying Canonical Files

Canonical spine files (00-11) are normative.

Changes to canonical files require:

```text
clear authority justification
consistency check with all other canonical files
verification that no invariants are violated
```

## Repository Chain

```text
omi-canon → omnicron-canon → omnicron-port, omnicron-isa, omnicron-lisp → omnicron-epistemic-model
```