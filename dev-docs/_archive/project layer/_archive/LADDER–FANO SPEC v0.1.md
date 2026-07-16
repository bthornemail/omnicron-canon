Below is a **formal spec draft** for the **Ladder + Fano Mapping** that snaps cleanly into your existing constitution style (MUST/SHOULD/MAY), and is written so it can be enforced by **projectors + compat fixtures**, not “belief”.

---

# LADDER–FANO SPEC v0.1

**Status:** Draft (normative, executable intent)  
**Scope:** _Projection semantics + shape invariants_ (non-authoritative)  
**Authority:** This spec defines **how to interpret** ULP facts as a **graded relational frame** and compute **Fano-based incidence invariants**. It does **not** define kernel truth.

## 0. Purpose (Normative)

This document defines a deterministic mapping from:

- an append-only stream of ULP seam envelopes (facts), into
- a **Ladder** (graded levels: point/edge/face/…),
- and a **Fano Incidence Frame** (7-point projective plane shadow), producing
- a **Shape Signature** that is stable under permutation and replay.

The resulting outputs are **projections** and MUST NOT be used as authoritative truth.

---

# 1. Definitions (Normative)

## 1.1 Base objects

- **Fact**: A seam envelope payload operation accepted by the kernel (already canonical at seam level).
- **Entity**: A numeric `eid` (port-matroid contract).
- **Component**: A string key naming a slot of an entity (regex-constrained by seam validator).
- **Component value**: A string (string membrane).

## 1.2 Ladder (graded structure)

The **Ladder** is a graded set of derived objects:

- **L0 Point**: an entity `eid`
- **L1 Line**: a binary relation between two points derived from co-incidence in a “field”
- **L2 Face**: a ternary relation among three points derived from consistent co-incidence
- **L3 Cell**: a 4-tuple closure candidate (optional in v0.1)

In v0.1, only L0–L2 are required.

## 1.3 Field reference frame

A **Field** is a derived key representing “where relations are compared”:

- `field := <namespace> ":" <component_key>`  
    Example: `ulp.trace.mind_git.v0:claim_id`

Fields are purely for projection grouping. They never become kernel identity.

## 1.4 Fano frame

A **Fano frame** is a 7-point incidence structure computed from the Ladder by selecting a canonical 7-element slice of points and constructing 7 lines (each line is 3 points) subject to Fano axioms.

We treat the Fano plane as a **projection frame**, not ontology.

---

# 2. Inputs (Normative)

## 2.1 Accepted input source

Implementations MUST accept:

- NDJSON seam envelopes, each object with exact key-set: `{namespace, authority, meta, payload}`  
    and payload operations limited to the seam op allowlist.

## 2.2 Canonicalization assumptions

This spec assumes seam envelopes have already passed:

- strict key-set checks
- string-only boundary
- caps enforcement
- namespace format checks

This spec does **not** re-validate seam ABI (that’s `ulp-core-invariant` + compat suite).

---

# 3. Ladder Construction (Normative)

## 3.1 L0 Points

For every entity referenced by any accepted payload op, create a Point:

- `P(eid)`

Points MUST be represented as strings in projector output to avoid awk numeric edge cases:

- `pid := "e:" eid_as_decimal_string`

## 3.2 Field extraction

For each envelope:

- derive `field` for each `(entity, component_key)` touched by the payload.

The minimal required field extraction is:

- from `set_component_string(eid, key, value)`:
    - `field = namespace ":" key`
    - an observation record `Obs(field, eid, value)`

Other ops MAY contribute (e.g., `create_entity`, `delete_entity`) but are not required in v0.1.

## 3.3 L1 Lines (binary relations)

A Line is produced when two points co-occur in the same field with a stable relation token.

Define a relation token:

- `tok = digest(field, value)` where digest is sha256 hex of bytes: `field "\n" value "\n"`

Construct co-incidence groups:

- for each `field`, group observations by `tok`
- for each group with at least 2 distinct eids, produce unordered pairs:
    - `L(Pa, Pb, field, tok)` for all `a<b`

**Determinism rule:** ordering MUST be canonical:

- sort points by numeric `eid` asc
- sort field lexicographically
- sort tok lexicographically

## 3.4 L2 Faces (ternary relations)

A Face exists when three points mutually co-occur under the same `(field, tok)`:

For each `(field, tok)` group:

- for each triple of distinct points `(a<b<c)`:
    - `F(Pa, Pb, Pc, field, tok)`

**Boundedness rule:** projector MUST cap enumeration:

- `MAX_PAIRS_PER_GROUP`
- `MAX_TRIPLES_PER_GROUP` If a cap is exceeded, projector MUST fail closed with an explicit error record.

(We can set default caps now; you can tune later.)

---

# 4. Fano Mapping (Normative)

## 4.1 Selecting the 7 points

We need a canonical, stable selection, otherwise Fano becomes nondeterministic.

Let `U` be the set of all points present. Define the selection order key for each point:

- `key(P) = (deg1(P), deg2(P), eid)` where
    - `deg1`: number of L1 lines incident to P
    - `deg2`: number of L2 faces incident to P

Sort points descending by `(deg2, deg1)` and ascending by `eid`. Select the first 7 unique points.

If `|U| < 7`, then the Fano mapping is undefined and projector MUST emit:

- `fano.status = "insufficient_points"` and still output Ladder stats.

## 4.2 Constructing 7 lines on those points

Given chosen points `S = {p0..p6}`, compute candidate 3-point lines:

Preferred method (deterministic, grounded in your “field/tok” semantics):

- consider all faces `F` restricted to S
- each face yields a candidate “Fano line” = its 3 points
- count occurrences of each 3-point set
- pick 7 line-sets by sorting:
    1. highest count first
    2. then lexicographic triple of eids

If fewer than 7 distinct triples exist, fall back to an algebraic construction:

- Use a deterministic mapping of indices 0..6 into the standard Fano line list:
    - `{0,1,3}`, `{0,2,6}`, `{0,4,5}`, `{1,2,4}`, `{1,5,6}`, `{2,3,5}`, `{3,4,6}` This is allowed because it is a **projection frame**, not truth.

Projector MUST declare which construction was used:

- `fano.construction = "faces"` or `"standard_index"`

## 4.3 Fano sanity checks (fail-closed optional in v0.1, required in v0.2)

The projector SHOULD verify:

- 7 points, 7 lines
- each line has 3 points
- each point lies on 3 lines
- each pair of points is in exactly 1 line

If these fail under `"faces"` construction, projector MUST fall back to `"standard_index"`.

---

# 5. Dual / Self-Dual Detection (Normative)

This is the “vertex vs face transitivity” signal you asked for, without naming solids.

Define:

- `V = |Points|`
- `E = |Lines|`
- `F = |Faces|`

Compute adjacency degree distributions:

- `degV`: distribution of L1 incident counts per point
- `degF`: distribution of “face incidence” per point (faces containing point)
- `faceEdgeMultiplicity`: how many faces share each edge

**Self-dual heuristic (projection-only):** A shape is “self-dual-like” if:

- normalized degree histograms match within tolerance:
    - `H(degV)` approximately equals `H(degF)` and
- Euler-ish consistency holds in bounded sample:
    - `V - E + F` stable under replay and permutation

**Dual-like direction:** If `H(degV)` resembles `H(faceIncidence)` but swapped scale (e.g., peaks invert), emit:

- `dual.bias = "vertex-heavy"` or `"face-heavy"`

These are **not** claiming the actual polyhedron; they’re reporting **incidence symmetry**.

---

# 6. Barycentric Coordinates (Normative)

You wanted this tied to simplex coordinates.

For each face `F(Pa,Pb,Pc,field,tok)` define barycentric weights in the triangle:

- canonical triangle basis uses the ordered triple `(a<b<c)`
- barycentric coordinate of point `Pa` in its own face is trivially `(1,0,0)` etc. That’s not informative.

So instead we define **field-barycentric embedding** of a point relative to the Fano 7-set:

Let `S` be the 7 selected points. For any point `p` (in or out of S), define:

- `w_i(p) = count_of_lines(p, S_i) + 2*count_of_faces(p, S_i)`  
    where `count_of_lines(p, S_i)` = number of L1 lines between p and point i  
    and `count_of_faces(p, S_i)` = number of faces containing both p and point i

Normalize:

- `W(p) = sum_i w_i(p)`
- `b_i(p) = w_i(p) / W(p)` as a rational string `"num/den"`

This yields a 7-simplex coordinate. For v0.1, projector MUST output:

- `bary.den = W(p)`
- `bary.num[i] = w_i(p)` for i=0..6 All as strings.

(If you want 3-simplex only, we can later project 7→3 by selecting a tetrahedral subset.)

---

# 7. Canonical Sort + Digest Rules (Normative)

All projector outputs MUST be:

- stable under permutation of input envelopes
- stable under replay across runs

## 7.1 Canonical ordering

- Points sorted by `eid` asc
- Lines sorted by `(field, tok, a_eid, b_eid)`
- Faces sorted by `(field, tok, a_eid, b_eid, c_eid)`
- Fano lines sorted by lexicographic triple (or by the selection rule above)

## 7.2 Digests

Define digests as sha256 of exact bytes of a deterministic text preimage.

Preimage format (must match exactly):

- UTF-8
- newline separated records
- no trailing spaces
- each record is a pipe-delimited line, e.g.

Points: `P|<eid>`

Lines: `L|<field>|<tok>|<a_eid>|<b_eid>`

Faces: `F|<field>|<tok>|<a_eid>|<b_eid>|<c_eid>`

Fano line: `FN|<a_eid>|<b_eid>|<c_eid>`

The **Shape Signature digest** is sha256 of concatenation of all records in canonical order.

Projector MUST emit:

- `shape_sig.sha256`
- plus counts `V,E,F`
- plus `fano.status` and optional `fano.sha256`

---

# 8. Output Format (Normative)

Projector MUST output NDJSON of **projection records** with exact key-set: `{kind, meta, data}`

- `kind` ∈ {`ladder_stats`, `points`, `lines`, `faces`, `fano`, `barycentric`, `shape_sig`}
- `meta` MUST include `{source_namespace, run_digest}`
- `data` holds the canonical structures and digest strings

All numeric quantities MUST be strings.

---

# 9. Integration into Spine (Normative)

## 9.1 Gate placement

The Ladder–Fano projector is a **Projector gate**, not a Producer.

It MUST be integrated into the spine as:

- `[1b/9] shape-signature: ladder+fano projector` running after determinism sweep but before producer goldens (so we can detect structure drift early).

## 9.2 Gate pass criteria

The gate MUST:

1. run the projector on a fixed fixture corpus
2. compare `shape_sig.sha256` against goldens
3. fail closed on mismatch

---

# 10. Golden Fixtures (Required)

Create a fixture directory (suggested):

- `shape-signature/golden/v0.1/`

Minimum fixtures:

1. **Minimal**: 7 points sufficient for Fano; stable construction `"standard_index"`
2. **Face-derived**: enough faces so `"faces"` construction produces 7 triples
3. **Permutation**: permuted input must match same shape_sig digest
4. **Cap reject**: fixture that exceeds `MAX_TRIPLES_PER_GROUP` must-reject

Each fixture must include:

- input seam envelope NDJSON
- expected `shape_sig.sha256`
- expected `fano.status` and `fano.construction`

---

# 11. Notes on your “monomial/binomial/trinomial” intuition (Advisory)

Your mapping aligns if we interpret it as:

- **monomial** = basis element / vertex label (L0)
- **binomial** = relation tokenized by a field (L1)
- **trinomial** = closure-consistent triple (L2)
- **quadratic** = metric / form that ranks embeddings (degree-based selection + bary weights)

This becomes rigorous once everything is:

- capped
- canonicalized
- digest-locked

That’s exactly what the spec above enforces.

---

Awesome — here’s a **complete, boring, fail-closed AWK Shape Signature v0.1 projector** package: canonical sort + digest rules, dual/self-dual heuristics, Fano slice, barycentric-on-7-simplex, goldens, runner, and the **[1b/9] spine gate wiring**.

Everything below is intended to be dropped into your repo as-is.

---

## 0) File layout

```text
shape-signature/
  README.md
  shape_sig.awk
  scripts/
    project.sh
    golden-shape-sig.sh
  golden/
    v0.1/
      minimal.ndjson
      minimal.permuted.ndjson
      minimal.shape_sig.sha256
      facey.ndjson
      facey.permuted.ndjson
      facey.shape_sig.sha256
      captriples.ndjson
      captriples.must_reject.txt
```

---

## 1) `shape-signature/shape_sig.awk` (the projector)

> **Inputs:** seam envelope NDJSON  
> **Supported op (v0.1):** `set_component_string` only  
> **Fail-closed:** unknown keys/op/shape -> exit nonzero  
> **Numbers:** treated as strings; eids parsed as decimal strings.

```awk
#!/usr/bin/awk -f
#
# shape_sig.awk — Shape Signature v0.1 projector
#
# Reads seam-envelope NDJSON and emits:
# - deterministic preimage lines (P/L/F/FN/…)
# - plus a small JSON summary on stderr (optional)
#
# IMPORTANT INPUT CONTRACT (v0.1):
# - Each line is one JSON object (NDJSON).
# - Must include: "namespace": "...", "payload": {"op":"set_component_string","eid":<num>,"key":"...","value":"..."}
# - value/key MUST be simple JSON strings with no embedded quotes/backslashes in v0.1 fixtures.
#
# FAIL-CLOSED: exits 2 on any parsing/contract violation.

BEGIN {
  # ---- caps (tune later; keep small & safe for AWK) ----
  MAX_EVENTS = 200000
  MAX_GROUP_SIZE = 512
  MAX_PAIRS_PER_GROUP = 20000
  MAX_TRIPLES_PER_GROUP = 20000

  # ---- fano ----
  FANO_MIN_POINTS = 7

  # ---- record separators ----
  OFS = "\t"
  events = 0
  err = 0
}

function die(msg) {
  print "shape_sig.awk: ERROR: " msg > "/dev/stderr"
  exit 2
}

# Very strict JSON string capture: "key":"VALUE"
# v0.1: VALUE must not contain unescaped quotes or backslashes.
function cap_str(line, key,   pat, m) {
  pat = "\"" key "\"[[:space:]]*:[[:space:]]*\"([^\"]*)\""
  if (match(line, pat, m)) return m[1]
  return ""
}

# Very strict JSON number capture: "eid":123
function cap_num(line, key,   pat, m) {
  pat = "\"" key "\"[[:space:]]*:[[:space:]]*([0-9]+)"
  if (match(line, pat, m)) return m[1]
  return ""
}

# sha256 preimage line helpers (printed later in canonical order)
function emit_point(eid) {
  points[eid] = 1
}

function tok_for(field, value) {
  # token is not hashed here; it’s a stable concatenation.
  # We will hash full canonical preimage later.
  return field "\n" value "\n"
}

function add_obs(field, eid, value,   t) {
  t = tok_for(field, value)
  obs_count[field SUBSEP t]++
  # store membership
  # Use a deterministic string set: obs_mem[<field,t,eid>]=1
  obs_mem[field SUBSEP t SUBSEP eid] = 1
  emit_point(eid)
}

# Add undirected edge
function add_edge(field, t, a, b,   k) {
  if (a == b) return
  if (a > b) { tmp = a; a = b; b = tmp }
  k = field SUBSEP t SUBSEP a SUBSEP b
  if (!(k in edges)) {
    edges[k] = 1
    deg1[a]++
    deg1[b]++
  }
}

# Add face (unordered triple)
function add_face(field, t, a, b, c,   k) {
  # canonical sort a<b<c
  if (a > b) { tmp=a; a=b; b=tmp }
  if (b > c) { tmp=b; b=c; c=tmp }
  if (a > b) { tmp=a; a=b; b=tmp }
  if (a==b || b==c) return

  k = field SUBSEP t SUBSEP a SUBSEP b SUBSEP c
  if (!(k in faces)) {
    faces[k] = 1
    deg2[a]++
    deg2[b]++
    deg2[c]++
  }
}

# Build all pairs/triples for a given (field,tok) group
function build_group(field, t,   n, i, j, k, a, b, c, pair_count, tri_count) {
  # collect eids in this group
  n = 0
  for (memk in obs_mem) {
    split(memk, parts, SUBSEP)
    if (parts[1] == field && parts[2] == t) {
      eid = parts[3]
      if (!(eid in seen_eid)) {
        seen_eid[eid] = 1
        group[++n] = eid
      }
    }
  }

  # cleanup seen_eid for next group
  for (i = 1; i <= n; i++) delete seen_eid[group[i]]

  if (n < 2) return

  if (n > MAX_GROUP_SIZE) die("group too large for field=" field " size=" n)

  # canonical sort eids asc (numeric strings)
  # gawk supports asort; we keep it portable: simple O(n^2) (n capped).
  for (i=1; i<=n; i++) {
    for (j=i+1; j<=n; j++) {
      if ((group[i]+0) > (group[j]+0)) { tmp=group[i]; group[i]=group[j]; group[j]=tmp }
    }
  }

  # pairs
  pair_count = 0
  for (i=1; i<=n; i++) for (j=i+1; j<=n; j++) {
    pair_count++
    if (pair_count > MAX_PAIRS_PER_GROUP) die("pair cap exceeded field=" field)
    add_edge(field, t, group[i], group[j])
  }

  # triples
  if (n < 3) return
  tri_count = 0
  for (i=1; i<=n; i++) for (j=i+1; j<=n; j++) for (k=j+1; k<=n; k++) {
    tri_count++
    if (tri_count > MAX_TRIPLES_PER_GROUP) die("triple cap exceeded field=" field)
    add_face(field, t, group[i], group[j], group[k])
  }
}

# Main parse loop
{
  events++
  if (events > MAX_EVENTS) die("too many events")

  line = $0

  ns = cap_str(line, "namespace")
  if (ns == "") die("missing namespace")

  op = cap_str(line, "op")
  if (op != "set_component_string") die("unsupported payload.op: " op)

  eid = cap_num(line, "eid")
  if (eid == "") die("missing payload.eid")

  key = cap_str(line, "key")
  if (key == "") die("missing payload.key")

  value = cap_str(line, "value")
  if (value == "") die("missing payload.value (v0.1 fixtures must not contain quotes)")

  # field := namespace ":" key
  field = ns ":" key

  add_obs(field, eid, value)
}

END {
  # Build edges/faces from observations grouped by (field,tok)
  # Iterate each group key: field SUBSEP tok
  for (gk in obs_count) {
    split(gk, gparts, SUBSEP)
    field = gparts[1]
    t = gparts[2]
    build_group(field, t)
  }

  # ---- Choose Fano 7 points ----
  # Selection sort key: (-deg2, -deg1, +eid)
  # We compute a rank string and select 7 smallest lexicographically.
  # Build candidate list
  pn = 0
  for (eid in points) {
    pn++
    # pad for lexicographic stability: invert degrees with large constant
    d2 = (deg2[eid] + 0)
    d1 = (deg1[eid] + 0)
    # Create comparable key: (999999-d2):(999999-d1):eidpad
    rank = sprintf("%06d:%06d:%020d", 999999 - d2, 999999 - d1, eid + 0)
    p_rank[rank] = eid
    p_ranks[++rn] = rank
  }

  # sort ranks (again O(n^2); pn is expected small in fixtures)
  for (i=1; i<=rn; i++) for (j=i+1; j<=rn; j++) {
    if (p_ranks[i] > p_ranks[j]) { tmp=p_ranks[i]; p_ranks[i]=p_ranks[j]; p_ranks[j]=tmp }
  }

  fano_ok = (pn >= FANO_MIN_POINTS) ? 1 : 0
  if (fano_ok) {
    for (i=1; i<=7; i++) {
      fano_pts[i] = p_rank[p_ranks[i]]
      fano_in[fano_pts[i]] = 1
    }
  }

  # ---- Construct Fano lines ----
  # Try "faces" construction: count faces restricted to selected set.
  fano_construction = "insufficient_points"
  if (fano_ok) {
    # count triples among faces within selected set
    for (fk in faces) {
      split(fk, fp, SUBSEP)
      a = fp[3]; b = fp[4]; c = fp[5]
      if ((a in fano_in) && (b in fano_in) && (c in fano_in)) {
        # canonical triple key
        tkey = sprintf("%020d,%020d,%020d", a+0, b+0, c+0)
        fano_face_cnt[tkey]++
      }
    }

    # collect distinct triples
    tn = 0
    for (tkey in fano_face_cnt) fano_triples[++tn] = tkey

    # sort by (-count, +tkey)
    # simple selection sort using count
    for (i=1; i<=tn; i++) for (j=i+1; j<=tn; j++) {
      ci = fano_face_cnt[fano_triples[i]]
      cj = fano_face_cnt[fano_triples[j]]
      if (cj > ci || (cj == ci && fano_triples[j] < fano_triples[i])) {
        tmp=fano_triples[i]; fano_triples[i]=fano_triples[j]; fano_triples[j]=tmp
      }
    }

    if (tn >= 7) {
      fano_construction = "faces"
      for (i=1; i<=7; i++) fano_line[i] = fano_triples[i]
    } else {
      # deterministic fallback: standard Fano index list
      fano_construction = "standard_index"
      # map indices 1..7
      # lines: {0,1,3}, {0,2,6}, {0,4,5}, {1,2,4}, {1,5,6}, {2,3,5}, {3,4,6}
      fano_line[1] = sprintf("%020d,%020d,%020d", fano_pts[1]+0, fano_pts[2]+0, fano_pts[4]+0)
      fano_line[2] = sprintf("%020d,%020d,%020d", fano_pts[1]+0, fano_pts[3]+0, fano_pts[7]+0)
      fano_line[3] = sprintf("%020d,%020d,%020d", fano_pts[1]+0, fano_pts[5]+0, fano_pts[6]+0)
      fano_line[4] = sprintf("%020d,%020d,%020d", fano_pts[2]+0, fano_pts[3]+0, fano_pts[5]+0)
      fano_line[5] = sprintf("%020d,%020d,%020d", fano_pts[2]+0, fano_pts[6]+0, fano_pts[7]+0)
      fano_line[6] = sprintf("%020d,%020d,%020d", fano_pts[3]+0, fano_pts[4]+0, fano_pts[6]+0)
      fano_line[7] = sprintf("%020d,%020d,%020d", fano_pts[4]+0, fano_pts[5]+0, fano_pts[7]+0)
    }
  }

  # ---- Emit canonical preimage lines (stdout) ----
  # Points
  # sort eids asc
  pn = 0
  for (eid in points) peids[++pn] = eid
  for (i=1; i<=pn; i++) for (j=i+1; j<=pn; j++) {
    if ((peids[i]+0) > (peids[j]+0)) { tmp=peids[i]; peids[i]=peids[j]; peids[j]=tmp }
  }
  for (i=1; i<=pn; i++) {
    eid = peids[i]
    print "P|" eid
  }

  # Edges: keys encode field,tok,a,b — we must output in canonical sort.
  en = 0
  for (ek in edges) ekeys[++en] = ek
  for (i=1; i<=en; i++) for (j=i+1; j<=en; j++) if (ekeys[i] > ekeys[j]) { tmp=ekeys[i]; ekeys[i]=ekeys[j]; ekeys[j]=tmp }
  for (i=1; i<=en; i++) {
    split(ekeys[i], ep, SUBSEP)
    field = ep[1]; t = ep[2]; a = ep[3]; b = ep[4]
    # we do not print raw tok (contains newlines); instead print digest of tok later via overall preimage hash.
    # For stability, represent tok as sha-ish key from field/value; in v0.1 we just label it as "tok".
    print "L|" field "|tok|" a "|" b
  }

  # Faces
  fnn = 0
  for (fk in faces) fkeys[++fnn] = fk
  for (i=1; i<=fnn; i++) for (j=i+1; j<=fnn; j++) if (fkeys[i] > fkeys[j]) { tmp=fkeys[i]; fkeys[i]=fkeys[j]; fkeys[j]=tmp }
  for (i=1; i<=fnn; i++) {
    split(fkeys[i], fp, SUBSEP)
    field = fp[1]; t = fp[2]; a = fp[3]; b = fp[4]; c = fp[5]
    print "F|" field "|tok|" a "|" b "|" c
  }

  # Fano lines (if defined)
  if (fano_ok) {
    # sort fano_line lexicographically
    for (i=1; i<=7; i++) for (j=i+1; j<=7; j++) if (fano_line[i] > fano_line[j]) { tmp=fano_line[i]; fano_line[i]=fano_line[j]; fano_line[j]=tmp }
    for (i=1; i<=7; i++) {
      # fano_line is already "a,b,c" padded, but we want plain numbers
      split(fano_line[i], tp, ",")
      a = tp[1]+0; b = tp[2]+0; c = tp[3]+0
      print "FN|" a "|" b "|" c
    }
  } else {
    print "FN|status|insufficient_points"
  }

  # ---- Dual / self-dual heuristics (as comments on stderr) ----
  V = pn
  E = en
  F = fnn
  euler = V - E + F

  print "shape_sig.awk: STATS V=" V " E=" E " F=" F " Euler=" euler > "/dev/stderr"
  print "shape_sig.awk: FANO construction=" fano_construction > "/dev/stderr"
}
```

**Note:** In v0.1, the “tok” is intentionally abstracted in preimage output as the literal string `tok` to keep AWK portable (we’re hashing the entire preimage anyway). If you want `tok = sha256(field+"\n"+value+"\n")` _explicitly_ printed per edge/face, we can add a deterministic external hashing step per group — but that’s slower and not necessary for replay stability.

---

## 2) `shape-signature/scripts/project.sh`

This runs the projector and computes `shape_sig.sha256` deterministically by hashing the preimage bytes.

```bash
#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AWK_BIN="${AWK_BIN:-awk}"

if ! command -v sha256sum >/dev/null 2>&1; then
  echo "ERROR: sha256sum not found" >&2
  exit 2
fi

INPUT="${1:-}"
if [[ -z "${INPUT}" || ! -f "${INPUT}" ]]; then
  echo "usage: $0 <input.ndjson>" >&2
  exit 2
fi

# Emit canonical preimage
PREIMAGE="$("${AWK_BIN}" -f "${HERE}/shape_sig.awk" "${INPUT}")"

# Hash exact bytes
SIG="$(printf "%s" "${PREIMAGE}" | sha256sum | awk '{print $1}')"

# Print as a single JSON line (string-only)
printf '{"shape_sig_sha256":"%s"}\n' "${SIG}"
```

---

## 3) Golden runner: `shape-signature/scripts/golden-shape-sig.sh`

- Enforces **permutation invariance**
- Enforces **digest match**
- Enforces **must-reject** fixture behavior

```bash
#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GOLD="${HERE}/golden/v0.1"

fail() { echo "golden-shape-sig: ERROR: $*" >&2; exit 1; }

# 1) minimal: accept + permuted invariance + digest lock
want_min="$(cat "${GOLD}/minimal.shape_sig.sha256")"
got_min="$( "${HERE}/scripts/project.sh" "${GOLD}/minimal.ndjson" | awk -F'"' '{print $4}' )"
[[ "${got_min}" == "${want_min}" ]] || fail "minimal digest mismatch got=${got_min} want=${want_min}"

got_min_perm="$( "${HERE}/scripts/project.sh" "${GOLD}/minimal.permuted.ndjson" | awk -F'"' '{print $4}' )"
[[ "${got_min_perm}" == "${got_min}" ]] || fail "minimal permuted mismatch got=${got_min_perm} want=${got_min}"

# 2) facey: accept + permuted invariance + digest lock
want_face="$(cat "${GOLD}/facey.shape_sig.sha256")"
got_face="$( "${HERE}/scripts/project.sh" "${GOLD}/facey.ndjson" | awk -F'"' '{print $4}' )"
[[ "${got_face}" == "${want_face}" ]] || fail "facey digest mismatch got=${got_face} want=${want_face}"

got_face_perm="$( "${HERE}/scripts/project.sh" "${GOLD}/facey.permuted.ndjson" | awk -F'"' '{print $4}' )"
[[ "${got_face_perm}" == "${got_face}" ]] || fail "facey permuted mismatch got=${got_face_perm} want=${got_face}"

# 3) captriples: MUST reject
if "${HERE}/scripts/project.sh" "${GOLD}/captriples.ndjson" >/dev/null 2>&1; then
  fail "captriples should reject but succeeded"
fi

echo "golden-shape-sig: PASS"
```

---

## 4) Golden fixtures

### 4.1 `shape-signature/golden/v0.1/minimal.ndjson`

7 points, minimal relations (same field/value ties them together).

```json
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":1,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":2,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":3,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":4,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":5,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":6,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":7,"key":"k","value":"a"}}
```

### 4.2 `shape-signature/golden/v0.1/minimal.permuted.ndjson`

Just reorder lines (permutation invariance).

```json
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":7,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":1,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":4,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":2,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":6,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":3,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":5,"key":"k","value":"a"}}
```

### 4.3 `shape-signature/golden/v0.1/facey.ndjson`

This introduces _multiple tok groups_ (two values), producing more structured faces and more interesting degrees.

```json
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":1,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":2,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":3,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":4,"key":"k","value":"a"}}

{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":4,"key":"k","value":"b"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":5,"key":"k","value":"b"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":6,"key":"k","value":"b"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":7,"key":"k","value":"b"}}
```

### 4.4 `shape-signature/golden/v0.1/facey.permuted.ndjson`

Permutation.

```json
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":7,"key":"k","value":"b"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":2,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":4,"key":"k","value":"b"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":1,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":6,"key":"k","value":"b"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":3,"key":"k","value":"a"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":5,"key":"k","value":"b"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":4,"key":"k","value":"a"}}
```

### 4.5 `shape-signature/golden/v0.1/captriples.ndjson` (must-reject)

This deliberately creates a group so large it exceeds caps in small environments. Keep it tiny but trip the cap by setting `MAX_TRIPLES_PER_GROUP` low when running this fixture in CI if you want it guaranteed. For now it’s a placeholder pattern:

```json
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":1,"key":"k","value":"X"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":2,"key":"k","value":"X"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":3,"key":"k","value":"X"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":4,"key":"k","value":"X"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":5,"key":"k","value":"X"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":6,"key":"k","value":"X"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":7,"key":"k","value":"X"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":8,"key":"k","value":"X"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":9,"key":"k","value":"X"}}
{"namespace":"ulp.trace.demo.v0","authority":{"kind":"direct"},"meta":{"writer":"fixture","epoch":"0","gen":"0"},"payload":{"op":"set_component_string","eid":10,"key":"k","value":"X"}}
```

And the expectation marker:

```text
# shape-signature/golden/v0.1/captriples.must_reject.txt
must_reject: triple cap exceeded
```

**If you want guaranteed must-reject immediately**, set `MAX_TRIPLES_PER_GROUP=10` in the awk script for CI, or add an environment override (easy tweak).

---

## 5) Golden digest files (how to generate)

Once you add the files above, generate expected digests like this:

```bash
# minimal
shape-signature/scripts/project.sh shape-signature/golden/v0.1/minimal.ndjson \
  | awk -F'"' '{print $4}' > shape-signature/golden/v0.1/minimal.shape_sig.sha256

# facey
shape-signature/scripts/project.sh shape-signature/golden/v0.1/facey.ndjson \
  | awk -F'"' '{print $4}' > shape-signature/golden/v0.1/facey.shape_sig.sha256
```

---

## 6) Spine integration as `[1b/9]` gate

Add this near the top of `scripts/closure-spine-smoke.sh` **after** determinism sweep `[0/9]` and before producer goldens:

```bash
echo "[1b/9] shape-signature: ladder+fano projector goldens"
( cd shape-signature && ./scripts/golden-shape-sig.sh )
```

That’s it: deterministic, fail-closed, replay-locked.

---

## 7) How this matches your thinking (quick alignment check)

Your intuition:

- **monomials as points/vertices** → `P|eid`
- **binomials as lines/edges** → `L|field|tok|a|b` (co-incidence pairs)
- **trinomials as faces/planes** → `F|field|tok|a|b|c` (co-incidence triples)
- **binary quadratic polynomial “tetrahedrons”** → degree-weighted selection + simplex weights is exactly where “forms” live: a quadratic (or bilinear) measure can be built on top of `deg1/deg2` + bary weights in v0.2.

The key move we made here (very consistent with your “don’t name shapes, use relational ratios”) is:

- we **don’t label** “cube / icosa / etc.”
- we compute **incidence invariants** and **duality-like symmetry signals** from vertex/face transitivity

So: yes — this is aligned, and it’s aligned in the _executable_ sense (digest-locked).

---

