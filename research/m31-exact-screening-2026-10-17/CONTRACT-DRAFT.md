# Proposed compact exact-screening wire contract and adopted semantics

This source-only declaration resolves initial independent-review questions; numerical execution still requires final review, frozen/published source and remote verification. Initial DESIGN-DRAFT and reviews remain unchanged.

## Common data

Document fields: schema, specId, runtime, sourceSha256, constants, records. Each of18 records has id,input,methods. Input is {drones:[{id,state:17binary64 hex words}]} in declared order. Methods are exactly complete then hierarchy, each run afresh from that same input; each record is {name,prepared,assembly,result,solve,certificate}. Prepared records and result/solve/certificate retain the prior complete-group schema and mathematical semantics. There are no allowed stress exceptions in this suite. The18 scenes and46,744 planned pairs per method (93,488 total) are literal declarations; expected classes are prospective hypotheses, not oracle inputs.

The two methods must agree exactly on prepared records, model status/branch/canonical witness, ordered positive coefficient records, native candidate bits and entire common certificate/load payload. This strict within-scene comparison isolates screening; it does not require native invariance across different input permutations. Each method is also independently checked against the actual full model; agreement between two methods alone proves nothing.

## Assembly and zero accounting

Assembly fields: mode,globalGuard,tree,queries,work. Modes: complete, hierarchy, fallback, global-preparation. Complete has null globalGuard/tree. Hierarchy first performs global guard proof; if it fails, mode=fallback, tree=null and the entire scalar scan runs. Tree building occurs only AFTER a successful global proof. Global invalidity retains all prepared records, emits no queries, null guard/tree, mode=global-preparation, and stops both methods before scientific pair/tree work.

GlobalGuard is {passed,checks:{centerComponent,centerNorm,rotorComponent,down,radial}}, with all five exact-box checks evaluated and true iff each bound passes. It is independently recomputed. A failed proof is not a model rejection; the fallback decides the model outcome.

Tree is {permutation:[stableID],nodes:[node]} with node={id,start,end,left,right,center,axis}. Nodes are preorder; [start,end) indexes the leaf-order permutation. Leaf children are null. Internal children partition the parent range; leaf capacity8; largest exact center-span split, x/y/z ties, exact coordinate then stableID ordering, floor(n/2) split. Center/axis are3pairs of canonical rational endpoints {n,d}, not native-rounded bounding values. All boxes are independently reconstructed. Left child traversal precedes right.

Queries appear exactly in input receiver order then rotor0..3. Query fields are {i,r,terminals}. Complete and fallback use exactly one terminal {kind:'scan',entries,zeroCount}, implicitly covering all input source IDs except receiverID. Hierarchy uses deterministic depth-first terminals: either {kind:'zero',node,rule,count} or {kind:'leaf',node,entries,zeroCount}. A zero terminal covers node membership minus receiverID, even if self belongs to the proved node. The predicate may conservatively include self; self is never a counted source. Rule is a zero-PROOF label; member pairs need not share the scalar branch name.

For scan/leaf terminals, entries contain every NONZERO singleton outcome as {j,result} in input-source order. All other eligible source members are explicitly claimed zeros. Positive result is {status:'positive',branch:'active',coefficient:{l,u}} (fixed96 interval). Rejected/unresolved result is {status,branch}. Internal scalar arithmetic still computes all five prior intervals; only coefficient is required by this compact common interface. The independent oracle must prove domain/caps and coefficient containment. Every implicit zero singleton is independently checked; zeroCount alone is never evidence of zero. Full source partition is disjoint and exhaustive, including empty self-only terminal sets when applicable.

No traversal stops after a refusal. After complete assembly, sort EVERY evaluated nonzero outcome by input receiver/rotor/input-source order before choosing first rejection, first unresolved, first ordering violation, then actual-positive-term resource failure. Omitted sets are proved zero, so this preserves canonical precedence. Only after whole-model admission construct identical ordered positive rows and shared candidate/certificate arithmetic.

## Work counters

Work fields: preparationCalls,globalProofs,treeNodes,nodeVisits,nodeRuleTests,zeroNodes,zeroPairs,leafVisits,scalarPairs,scalarZeroPairs,positiveTerms,rejectedPairs,unresolvedPairs. PreparationCalls counts N calls to the inherited adapter's self-pair preparation (both methods pay the same duplicated internal preparation); it is not a claim of N underlying rotations. GlobalProofs is0 for complete/global invalid and1 for hierarchy/fallback after successful preparation. TreeNodes is0 outside hierarchy. NodeVisits includes every traversed node. NodeRuleTests counts each tested predicate in fixed neighbor/upstream/down-cut/near-outside/radial order until a success or all5fail. LeafVisits counts emitted hierarchy leaf terminals only. ScalarPairs counts actual shared prepared-pair calls. ScalarZeroPairs counts their zero results. zeroNodes/zeroPairs count pruned terminals and nonself members, separately from scalar zeros. Nonzero counters count all scalar outcomes, even in refused scenes. In globally invalid scenes, all counters except preparationCalls are zero.

All counters must reconcile to source partitions and independently recomputed deterministic traversal. They measure selected algorithmic work, not total arithmetic, build comparisons or time; no wall-clock speedup or total-cost savings follows. The fallback pays globalProofs and full scalar scan; no tree was built before a failed proof under this declared recipe.

## Budget still to finalize

Fixed scene count18, maximum64, total312 drone records and46,744 logical nonself pairs per method. Compact zero output avoids repeated zero intervals. Before source freeze, the protocol reviewer and checker author must settle per-field/schema bounds and aggregate output feasibility for kernel JSON+journal, checker evidence/controls and supervision logs;64MiB remains draft and may change prospectively before execution. The proposed300s kernel/600s checker deadlines likewise remain draft until source supervision and total-output accounting are reviewed. No numerical probe is authorized to estimate these budgets.

## Prospective clarifications before implementation freeze

Leaf members retain the incoming recursive order, including a root of at most8 members. Query i and entry j are original input indices. Prepared records, tree permutation, solver/load IDs and canonical refusal witness i/j use stable IDs. Assembly explicitly converts all indexed nonzero outcomes to stable-ID pairs before canonical refusal selection and shared certification.

An administrative exception in exact-box construction, tree creation or serialization fails the stage explicitly and is retained. It is not model rejection and never silently triggers fallback. Only a completed global proof returning false chooses full-scan fallback.

Adopted static budget:384MiB aggregate, with kernel JSON<=128MiB, journal<=128MiB, checker<=96MiB, logs/attempt metadata<=16MiB and two64KiB supervision reports. Kernel/checker wall limits300/600s, guardians310/610s, sampled process-group RSS1GiB. Compact kernel serializer caps each nonzero entry384B, certificate row1KiB, per-drone load96KiB, tree node8KiB, fixed96 integer string108characters, canonical load rational integer string4096characters and tree numerator310/denominator324characters. Refuse oversize output explicitly; never truncate. Compact JSON is used. No numerical probe was used for this budget choice.
