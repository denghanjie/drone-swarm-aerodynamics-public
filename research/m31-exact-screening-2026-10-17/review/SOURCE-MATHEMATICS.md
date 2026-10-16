# Source-only mathematical review of exact screening

**No unresolved mathematical or assembly blocker was found in the reviewed source snapshot.** The prepared-pair adaptation preserves the inherited scalar calculation, the extracted proposal/load certificate arithmetic is unchanged, and the exact box/tree implementation realizes the five reviewed conservative predicates. This is a source review, not a numerical qualification or execution authorization. The independent checker, frozen protocol, supervision and publication remain separate obligations.

## Reviewed boundary and resolved integration issue

The primary review covers `source/pair-prepared.cjs`, `source/loads.cjs`, `source/boxes.cjs`, `source/tree.cjs` and the subsequently authored `source/methods.cjs`. `SOURCE-MATHEMATICS-READING.json` records exact source hashes and reading scopes. The preserved pair and coupled snapshots match the inherited hashes recorded in the initial review. The coupled source, previously read only through line 52, has now been read in full through its preserved copy. No additional inherited semantic file was needed; the count remains 5 of 16.

The initial load-helper inspection exposed an interface risk: `loads.cjs:21` accepts stable-ID pair endpoints, while query `i` and entry `j` are original input indices. This is resolved by `methods.cjs:50-51`: it first sorts the indexed outcomes in original receiver/rotor/source order, then converts both endpoints to stable IDs before either canonical witness selection or `L.certify`. The certificate's own row IDs correctly remain stable IDs. The adopted contract now documents this conversion.

## Prepared scalar kernel and common certificate

The text diff against `prefreeze/inherited-pair.cjs` changes the query interface, removes repeated preparation/self handling, and replaces repeated dyadic decoding with supplied exact prepared operands. It preserves the center component/norm guard, neighbor zero, rotor/down guards, upstream/down-cut zeros, radial guard, near rejection/outside zero, width/radial cutoff, projection, active coefficient arithmetic and cap/normalizer refusal order. In particular, projection is still too late to hide near rejection. All five active intervals are still computed internally; compact assembly retains the coefficient only after positive classification.

`methods.cjs:6-12` establishes the moved preconditions: each method separately prepares every raw drone, preserves all preparation records, rejects the first invalid preparation before any tree/pair work, then decodes centers, axes, actual prepared rotor points and forces into exact rationals. Its scan calls the prepared helper only for nonself pairs and valid rotor indices. The solver validates nonempty/maximum scene size, unique bounded integer IDs and state length before invoking either method. Thus removing preparation and self branches from the helper does not remove those obligations from the complete method.

The diff against `prefreeze/inherited-coupled.cjs` shows that `loads.cjs` extracts the shared arithmetic and changes only its entry wrapper and compact coefficient field access. The text beginning at force/weight construction through candidate iteration, root bisection, defect factors, root boxes, rotor/collective/world-force/world-moment loads, normalized error bounds, exact tolerance comparison and certificate exception handling is unchanged. The interval, rational and adapter helpers are byte-identical to their previous-package counterparts by a metadata-only comparison. This establishes source preservation, not accuracy by shared-method agreement; independent reference/certificate validation is still required.

## Boxes, global proof and tree

`boxes.cjs` uses natural exact rational intervals. Subtraction exchanges opposite endpoints; multiplication takes all four endpoint products; division is restricted to a positive exact scalar. Coordinate interval minima/maxima of absolute value give conservative lower/upper squared norms. Bounds contain current prepared values, with no native-rounded box or unit-axis shortcut.

`tree.cjs:4-8` bounds all prepared center, source-axis and receiver-point operands, forms `d`, `h=d dot axis` and the actual residual `e=d-h*axis`, and evaluates all five global magnitude checks. Dependence loss can force fallback but cannot prove a false guard bound. `methods.cjs:15-18` builds the tree only after the completed global proof returns true; a false return selects complete scan. Administrative exceptions propagate rather than silently becoming a fallback, rejection or zero. Retention and naming of a failed stage must be checked at the supervisor boundary.

Tree construction uses the largest exact center span, x/y/z ties, coordinate then numeric stable-ID order, and the floor midpoint. Nodes receive IDs before their left and right recursive children; their ranges therefore form disjoint complete partitions of the leaf-order permutation. Leaves preserve incoming recursive order, including an unsplit root, as now explicitly adopted. The caller's validated unique IDs and nonempty scene make every internal split nonempty and terminating.

The zero-rule comparisons match the reviewed strictness exactly: neighbor lower bound `>=neighbor^2`; upstream upper `<=0`; down-cut lower `>=downCut`; near-outside upper `<minDown*D` and radial lower `>=nearRad^2`; radial lower `>=minDown*D`, positive width lower, and radial lower `>=radCut^2*widthUpper^2`. Their fixed test order and incremented test counts agree. Natural residual bounds preserve actual near-unit axes, and no projection predicate was added.

## Assembly, precedence and accounting

The traversal tests each node, emits a zero terminal and stops descending when a predicate succeeds, or recurses left then right and ultimately scans leaf members. Nonself membership is used both in zero-terminal counts and scalar scans. Self-only terminals may cover an empty set. Leaf entries are ordered by original input-source index. With the exact tree construction, these operations produce a disjoint complete source partition; the scalar-plus-pruned count equality is a useful check but remains insufficient evidence on its own for an independent checker.

Traversal continues after scalar rejection or unresolved outcomes. All nonzero outcomes, including positive classifications whose coefficient lower endpoint could be zero, remain in accounting. After assembly, the complete original-order sort precedes rejection, unresolved, positive-ordering and positive-term-budget decisions. Stable-ID conversion preserves that sequence. The descending exact center-height/stable-ID rank test matches the inherited ordering restriction. Shared solve/certificate arithmetic is called only after these checks.

The counters distinguish preparation, global proof, tree creation, visited nodes/rules, pruned nonself pairs and actual scalar outcomes. A false global proof incurs its proof count and the full scan, without an earlier tree. Global invalidity preserves only preparation calls. These are selected work counts; they do not establish wall-clock speedup or total-cost savings.

## Scope limits

Only source/text reading, textual comparison, metadata hashing and structural JSON inventory were performed. No scientific module was imported, no model case or earlier suite was evaluated, no numerical probe or external operation occurred, and no agent was created. The structural scene inventory confirms 18 records, 312 drone records, maximum 64 and 46,744 logical nonself rotor pairs per method; expected classes and boundary descriptions remain prospective declarations.

This review does not cover a not-yet-qualified independent checker, control effectiveness, final serializer/supervisor implementation, runtime/resource behavior, physical accuracy or the original 5,000-drone objective. Any change to the reviewed source hashes needs a corresponding source delta review before relying on this disposition.
