# RFC: Simplex Ladder & Incidence Algebra v1

**Status:** Draft  
**Version:** 1.0  
**Audience:** ULP / Port-Lattice / Port-Matroid ecosystem implementers  
**Scope:** A _domain-independent_ incidence model that (1) defines the “ladder” growth, (2) provides Pascal simplex coefficients as the canonical counting law, and (3) supplies a formal incidence algebra suitable for AWK/Haskell validators and spine gates.

---

## 0. Motivation

The ecosystem already enforces deterministic closure at the seam. This RFC adds a _structural_ invariant: a canonical incidence model that can be used to:

- classify objects by rank (point/edge/face/tetra/simplex),
- count adjacency budgets deterministically (allocation/protocol/federation),
- gate projections (local vs federated), and
- provide a single algebra shared by geometry, logs, and “shapes as reference frames.”

This RFC intentionally avoids naming solids. Shapes are treated as **relational reference frames** characterized by incidence and duality.

---

## 1. Terminology and Normative Keywords

The keywords **MUST**, **SHOULD**, **MAY** are normative.

- **Rank** `r`: dimension index (0=vertex/point, 1=edge, 2=face, 3=tetra cell, …).
- **Simplex** `Δ^n`: the abstract n-simplex (n-dimensional simplex).
- **Incidence** `x ⊑ y`: “x is incident to y” / “x is a face of y” (rank(x) ≤ rank(y)).
- **Flag**: a strictly increasing chain of incident elements.
- **Dual** `x*`: order-reversing mapping swapping vertices ↔ facets (when defined).
- **Signature**: canonical summary of incidence counts.

---

## 2. Data Model

### 2.1 Atoms

An **Incidence Structure** `I` consists of:

- a finite set of elements `E`,
- a rank function `rk : E → {0..n}`,
- an incidence relation `⊑ ⊆ E×E`.

### 2.2 Well-formedness (MUST)

For all `x,y,z ∈ E`:

1. **Reflexive:** `x ⊑ x`
2. **Transitive:** `x ⊑ y ∧ y ⊑ z ⇒ x ⊑ z`
3. **Antisymmetric-on-same-rank:** `x ⊑ y ∧ y ⊑ x ∧ rk(x)=rk(y) ⇒ x=y`
4. **Rank monotone:** `x ⊑ y ⇒ rk(x) ≤ rk(y)`

This makes `(E, ⊑)` a graded poset.

---

## 3. Canonical Simplex Counts (Pascal Simplex Coefficients)

This section derives the canonical coefficients that govern how many k-faces an n-simplex has.

### 3.1 Faces of an n-simplex

An abstract n-simplex `Δ^n` has `n+1` vertices.  
A k-face is determined by choosing `k+1` vertices.

**Theorem (Face Count):**  
Number of k-faces of `Δ^n` is:

```latex

f_k(Δ^n) = \binom{n+1}{k+1}
```

**Derivation:** choose the vertex subset defining the face; each subset uniquely determines a face.

Examples:

- `Δ^0`: vertices = 1
- `Δ^1`: vertices = 2, edges = 1
- `Δ^2`: vertices = 3, edges = 3, faces = 1
- `Δ^3`: vertices = 4, edges = 6, triangular faces = 4, tetra cells = 1

This is the **Pascal triangle** along the simplex.

### 3.2 Pascal simplex (multinomial) coefficients

For _lattice / block_ constructions you want the coefficient law that counts compositions across multiple axes.

For integers summing to , the multinomial coefficient:

```latex

\binom{N}{a_1,\dots,a_m} = \frac{N!}{a_1!\cdots a_m!}
```

**Interpretation (Normative):**  
When your system composes adjacency budgets across `m` independent constraint axes (e.g., variant/invariant/covariant/contravariant), the canonical count of distinct allocations at total “mass” `N` is multinomial.

### 3.3 5³ block and layered shells (advisory but actionable)

A `5×5×5` block has shell decomposition by Chebyshev radius `d` from center:

- `d=0`: 1 core
- `d=1`: 3³−1 = 26
- `d=2`: 5³−3³ = 98 Total 1+26+98 = 125.

This gives a canonical **(core, inner shell, outer shell)** partition useful for “local/boundary/global” gating.

---

## 4. Formal Incidence Algebra

We define an algebra on incidence structures to support composition, duality detection, and canonical signatures.

### 4.1 Incidence matrix

Let `E_k = { x ∈ E | rk(x)=k }`.  
Define boundary incidence (rank-adjacent):

```latex

B_k[x,y] = 1 \iff x \in E_{k-1}, y \in E_k, x \prec y
```

This is the Hasse relation by rank.

### 4.2 Operators

Define:

- **Up operator** by multiplication with
- **Down operator** by multiplication with

These generalize adjacency lifts and can drive deterministic “growth tracking” or “allocation propagation.”

### 4.3 Composition

Given incidence structures `I=(E,⊑,rk)` and `J=(F,⊑,rk)`:

- **Disjoint sum** `I ⊕ J`: union with no cross-incidence (MUST preserve ranks).
- **Gluing along a shared subposet** `I ⊔_K J`: identify an isomorphic substructure `K`.  
    This MUST be fail-closed unless the identification is canonical (hashable mapping).

### 4.4 Duality and self-duality

A **duality** for rank `n` is a bijection `* : E → E` such that:

- `rk(x*) = n - rk(x)`
- `x ⊑ y ⇔ y* ⊑ x*` (order-reversing)

**Self-dual detection (MUST for a “self-dual” claim):**

- there exists such a bijection `*` and
- its induced action preserves canonical signatures (below).

(Implementations MAY use backtracking with pruning via signatures; for spine gating use small fixtures / bounded search.)

### 4.5 Canonical signature

For each rank `k`, define the multiset of degree pairs:

- upward degree: `deg↑(x) = |{ y ∈ E_{k+1} : x ≺ y }|`
- downward degree: `deg↓(x) = |{ z ∈ E_{k-1} : z ≺ x }|`

A canonical signature is the tuple:

```latex

Sig(I) = \Big(\; |E_0|,\dots,|E_n|;\; \text{sorted multisets of }(deg↓,deg↑)\text{ by rank} \;\Big)
```

**Canonicalization (MUST):**

- Sort within each rank by `(deg↓,deg↑, stable_id)` where `stable_id` is a deterministic digest of the element’s incident neighborhood (see 4.6).

### 4.6 Canonical element digests (for deterministic ordering)

Define neighborhood digest for `x`:

- gather incident neighbors in ranks `rk(x)±1`
- represent as sorted list of their provisional digests
- hash the serialization

Iterate from rank 0 upward (or use Weisfeiler–Lehman refinement style) until stable.  
Fail closed if refinement does not stabilize within bounded iterations (configurable cap).

---

## 5. “Ladder” Growth Laws as Normalized Names

This RFC normalizes your growth patterns into named operators:

### 5.1 Radix-4 lift (Simplex Lift)

**Definition:** `Lift4(S)` is the operator that grows a structure by one simplex-vertex layer, increasing adjacency capacity by 4-way vertex incidence.

Operationally, implement as:

- introduce a new rank (or new layer) whose face counts follow `binom(n+1, k+1)`
- or, in block mode, expand shell radius by 1 within the `5³` partition.

### 5.2 Logical doubling (Binary Composition)

`Compose2(C)` doubles capacity by pairing states:

- capacity sequence: 16→32→64→128→…  
    This is a tensor product on state space: `C ⊗ {0,1}`.

### 5.3 Quadratic growth (Square Law)

`Square(C) = C²` governs “resolution” style joins:

- 256×256 = 65536 is a grid-resolution join (state×state).

### 5.4 Exponential / logarithmic factorizations

These are not separate semantics, just different decompositions of the same count in the commutative semiring . Implementations MUST treat them as _accounting identities_, not different protocols, unless the protocol explicitly binds a decomposition.

---

## 6. Validation Requirements (Spine Gate Ready)

A validator for this RFC MUST provide:

1. Parse a structure (elements with ranks + cover incidences).
2. Check well-formedness axioms (2.2).
3. Compute `Sig(I)` deterministically (4.5–4.6).
4. Optional: attempt duality witness `*` under bounds for self-dual claims (4.4).
5. Emit a canonical digest of `Sig(I)` for gating.

---

## 7. Canonical Encoding

This RFC is compatible with your seam “string membrane” approach.

### 7.1 Canonical JSON (for fixtures)

Represent an incidence structure as:

- `n` (max rank)
- `elements`: list of `{id, rank}`
- `covers`: list of pairs `[lower_id, upper_id]` where `rk(upper)=rk(lower)+1`

All numeric-like values MUST be emitted as strings if they cross the seam.

### 7.2 Digest

Canonical digest is:

- canonical JSON serialization (stable key order, no whitespace variation)
- sha256 of bytes
- output as `sha256:<hex>`

---

## 8. Security & Fail-Closed Rules

Implementations MUST fail closed on:

- rank gaps in covers,
- incidence cycles that violate graded poset axioms,
- non-deterministic canonicalization (ordering depends on runtime hash seeds),
- duality claims without a witness mapping,
- exceeded caps (max elements, max covers, max refinement iterations).

---

## 9. Appendix A: Minimal Examples

### A.1 Tetrahedron as simplex Δ³

Counts via :

- vertices: C(4,1)=4
- edges: C(4,2)=6
- faces: C(4,3)=4
- cell: C(4,4)=1

Signature sanity checks:

- each vertex has deg↑=3 edges
- each edge has deg↓=2 vertices, deg↑=2 faces
- each face has deg↓=3 edges, deg↑=1 cell

---

# Next deliverables you asked for (I can write immediately next)

1. **Executable AWK validator** for this RFC (parse → check axioms → compute Sig → digest → optional dual search under caps)
2. **Golden fixtures**: Δ², Δ³, cube/octa incidence posets as reference frames (without naming them)
3. **Haskell typed model** (GADTs for rank, safe cover edges, canonical signature computation)

Say “go AWK” or “go Haskell” and I’ll produce the full code + fixtures + a spine gate step name like `[1b/9] incidence-signature`.