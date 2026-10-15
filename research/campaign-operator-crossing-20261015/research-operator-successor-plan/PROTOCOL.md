# Support-crossing operator protocol: prospective, not released
15 October 2026. Planning only. Base: denghanjie/drone-swarm-aerodynamics-public,
commit 827350b7d9ea517c5f1e471672aaca4ad6a4c26e.

## 1. Question and fixed scope
Compare ZOH (Z), linear (L), quadratic (Q), restricted cliff (C). Does ONE
variant remove a linear ACCURACY advantage? Equal samples are not equal cost.
Planning only: no model/experiment/install/publish, speedup/novelty/physics claim.

World/body +z up; identity attitudes. Source (0, 0, 0.5) m; receiver (x(t), 0, 0),
x(t)=0.22-0.12 cos(2 pi (t+phi)/0.5), t in [0, 0.5] s. Both m=0.027 kg;
g=9.81; a=0.028 m; source hover scale; receiver nominal thrust mg/4 per rotor.
Preserve order (a,a),(-a,a),(-a,-a),(a,-a), original kernel/taper/load closure.
Four ordered (H,phi) cases, seconds: (0.00125, 0),(0.00125, 0.000625),
(0.005, 0),(0.005, 0.0025). No tuning/replacements.
D=2 sqrt(2)a; downstream=0.5; b=0.07668(0.5+5.817D).
Fade onset 2b=0.1473303289873278 m; edge 3b=0.22099549348099173 m.
Neighbor distance <3 m. All rotors start in core, leave/re-enter support.
No near-field/axial/wall crossing. Taper is C1, not a jump. Y symmetry
duplicates two histories: roll zero, pitch informative. Retain all four.

## 2. Causal supply and cliff rules
At t_k=kH, u_k is the scheduled four-rotor truth sample. Per-rotor predictors
receive only samples, integer clock, own history. No negative-time/periodic
samples, dense truth, geometry, resets, extra refreshes or support masks.
Scoring data stay inaccessible.
Use integer ticks: alpha=(n-k*R)/R, R=16 or 64, exact endpoints 0/1.
Binary64 order:
d1=u_k-u_(k-1); d2=(u_k-2*u_(k-1))+u_(k-2);
L=u_k+alpha*d1; Q=L+((alpha*(alpha+1))*0.5)*d2.
No algebraic rewrite/fused operations. Delivered=max(0,raw); record -0 as +0.
Z holds always. L holds at k=0, then linear. Q holds at k=0, linear at k=1,
quadratic from k=2. C has that same startup; interval k=2 is ungated Q.

For every C interval k>=2, retain a separately computed RAW shadow s=Q_k(1),
even when delivering hold. Never use delivered fallback/clamped shadow as s.
At t_(k+1), first score old delivered alpha=1, THEN reveal u_(k+1).
N=abs(u_(k+1)-s); B=abs(u_(k+1)-u_k); eps=1e-12 m/s.
- B<=eps and N<=eps: Q next interval (zero/zero category).
- B<=eps<N: hold next interval (positive/zero category).
- B>eps: hold exactly when N>0.9*B; equality selects Q.
No hysteresis/reset. First gate k=3. Terminal residuals are diagnostic only.
JSON encodes degeneracy categories, not infinities.

[CHOPtrey primary v2](https://arxiv.org/html/1610.09261v2) reread.
§4.3 covers interpolation; §5.2/Table 1 uses contextual polynomial/history
families; §5.3/Eqs.11–13 compares prior endpoint residuals, selects six
possible weights and applies a cliff threshold (0.9 illustrated).
Single-Q/shadow/startup/degeneracy/clamp choices are our adaptations,
NOT full CHOPtrey or a stability guarantee.

## 3. Reference and one-sided timing
Common grid: n=0..6400, t_n=n/12800 s; refresh indices multiples of 16 or 64.
Original A.fields(sum-rotor) on the two prescribed states supplies truth.
Count source-zero work separately. No event-triggered calls. Original
A.effectiveThrust/F.wrench retain arithmetic, stopping rule and 12-loop cap.
All truth/delivered values must be finite/nonnegative.
At n=0 score initialization. Refreshes score incoming alpha=1 BEFORE new
truth. These are primary values. Also score outgoing alpha=0 at interior
refreshes (must equal new sample), never terminal. Maxima use both sides;
sums/counts primary only. Tag sides.
Crosscheck cached original truth with existing exact-aero.cjs at
n=0,200,..., 6400: 33 nodes/case, including source zeros. Tolerance 1e-12 m/s +1e-12 times larger magnitude. Mismatch stops.
Check nominal/load identities and side invariants.

## 4. Metrics and event admission
W=mg=0.26487 N; Wa=0.00741636 N m (a, not sqrt(2)a).
eU=max_r abs(u_hat_r-u_r) [m/s]; eF=norm2(F_hat-F)/W;
eM=hypot(Mx_hat-Mx,My_hat-My)/(Wa).
F=(0, 0,sum thrust); Mx=sum(y_r thrust_r); My=-sum(x_r thrust_r).
Yaw remains nominal, excluded from accuracy. Report roll separately;
abs(Mx)/(Wa)>1e-12 in truth/any method stops the symmetry check.
Secondary: raw-inflow error/minimum, raw<0 and raw<-1e-12 counts, clamp
maximum/sum. Never feed negative inflow to loads or divide by zero truth.
Outside support is original geometry r>=3b. Leakage: maximum delivered
inflow, count of rotor/grid slots >1e-12 m/s, and
I_leak=delta*sum_(n=1..6400)[sum_r 1_outside*u_hat_r/4], delta=1/12800.
I_U,I_F,I_M=delta*sum_(n=1..6400)e_j(t_n). Right-node DISCRETE scores use incoming refreshes, not certified continuous
integrals. Outgoing has zero extra weight.

For each x offset dx and kappa in {2, 3}, define
xe=sqrt((kappa*b)^2-a^2)-dx;
tau_out=acos((0.22-xe)/0.12)/(4*pi)-phi;
tau_in=0.5-acos((0.22-xe)/0.12)/(4*pi)-phi.
Retain dense bracketing indices and verify geometric signs. Each rotor must
have fade-out, support-out, support-in, fade-in, all strictly inside run:
16 rotor-events/case, 64 total (32 support-edge events). Assign each to
right-closed (t_k,t_(k+1)]; within 1e-12 s of a clock boundary assign incoming.
Label tolerance never changes truth/predictions.
Disjoint primary strata: startup (incoming intervals k=0, 1 plus n=0),
crossing (remaining intervals containing ANY rotor fade/support event),
interior (remainder). Preserve event-type flags/rotor masks; also report each
event type, with overlaps disclosed. Loads use the union across rotors.
Invalid events/geometry, nonfinites or ambiguity stop; no residual-selected
windows/search.

Accuracy-max tie floors: fixed absolute 1e-10 in each metric's units.
Leakage max floor 1e-10 m/s; leakage-integral floor 5e-11 m; counts exact.
Floors classify only; no data changes or below-floor percentage claims.

## 5. Fixed-variant decision
Coarse even-index 3201-grid uses 2*delta and identical sides; report decision
maxima/leak only. Fine grid:global scores; strata/event maxima and shared
counts only (no stratum integrals). No new fields or between-grid guarantee.
Reject a special linear accuracy advantage only if ONE candidate Q or C:
- weakly dominates L in all three maxima in ALL four cases on BOTH grids
  (candidate-linear<=metric floor);
- strictly improves beyond the floor in the SAME case/metric on both grids;
- has no worse leakage maximum/count/integral in every case on both grids.
Evaluate Q/C separately; never mix winners across cases/grids. Any qualifying
variant establishes sampled accuracy dominance even if the other reverses.
If NONE passes and ANY candidate-vs-L accuracy/leakage grid ranking reverses
beyond floors (counts exact), report SAMPLING_UNRESOLVED; otherwise
NO_FIXED_VARIANT_DOMINANCE. Retain per-variant reversals/all strata/ZOH.
Near-floor ties remain ties.

## 6. Work counts and bounded attempt
25,604 reference times =102,416 receiver rotor slots. Original two-body
fields visits 204,832 directed rotor/source slots including source zeros.
Each method gets 1,004 scheduled vectors/4,016 rotor slots, initial/terminal
included, reused from truth. Dense reference is offline work.
Four-method primary outputs: 409,664 scalars; interior outgoing:
996*4*4=15,936; total 425,600. Invoke supply even at initialization, including
64 exact initial scalar outputs. Reference+delivered load calls: 528,016
before additional explicit load checks. C raw shadows: 3,968 scalars;
next-interval gate decisions: 3,952; terminal residual diagnostics: 16.
Exact crosschecks add 132 evaluator calls/1,056 directed rotor slots.
Total receiver kernel opportunities <=102,944; total directed slots 205,888.
Cap actual far-field kernel evaluations, both original W.normalizedWake and
exact-aero's inline kernel, at 110,000. Count fields, guards, skipped zeros,
actual kernels and crosschecks separately; receiver slots are not total work.
Count evaluations by degree, coefficients/history, shadows, gates, clamps,
loads/zero returns, wrench reductions, scoring/geometry/hashes. Exact solver calls/zero returns plus the labeled<=12 Newton-iterations per
nonzero call bound suffice; actual-loop instrumentation is optional. No FLOPs claim.
Record wall/CPU/phase times, without a speedup claim from shared truth.

One prospective attempt: 20 s outer wall including checks/final flush,
reserving 2 s for termination/failure recording. No retry or parameter search.
Time/kernel/schema/byte/finite-value failure stops, preserving partial
records. Source/code hashes, schema, review, byte census and hash-bound release
remain prerequisites; no longer run/retry is authorized.

## 7. Retention and 180,000-byte feasibility
Carry 199,751,910 B despite workspace loss; cap 200,000,000 B,remaining 248,090.
All new copies count; 250 MB unapproved. 180,000 B leaves 68,090 B headroom.
PRIMARY ceilings(B):source 20,997;protocol 12,000;driver/supervisor 16,000;
review 4,000;evidence/failure 30,000;viewer 3,000;manifest 4,003. Total 90,000.
Sources:original four 13,341 +exact-aero 7,465 +source 191 B; predictor read-only.

Stream summaries and binary64 witnesses, not dense histories (truth alone
is 819,328 B). Reserve 4,000 B of evidence for first failure/bounded raw logs;
normal schema <=26,000 B, proven before release. Retain:
- all 64 unique event-bracket nodes:truth[4],raw[4 methods][4 rotors]; clamp
  reconstructs exactly as max(0,raw);
- all 48 fine-grid case/method/metric worst witnesses;
- worst leakage and minimum raw per case/method;
- first gate fallback/recovery per case/rotor, k>=3; absent flagged.
Fixed widths, no outcome-dependent size savings: 64 event rows *168 B,
80 metric/leak/minraw rows *88 B, 32 gate rows *80 B =20,352 B. Metric rows:
Metric indices:uint32(case,n,method,side), then truth4/raw4/metric float64.
Gate indices:uint32(case,k,rotor,flags), then 8 doubles(old3,new,shadow,N,B,0.9B).
Event words:uint32(packed,n),then truth4/raw16 doubles. Packed bits 0–1 case;
2–10 interval k<=399;11–26 mask;27 side(0 lower,1 upper);28–31 zero.
Mask bit 4*type+rotor;types fade-out/support-out/support-in/fade-in,rotors 0..3.
Add 64 B header +5,584 B binary summaries/counters/status =26,000 B.
Freeze layout; viewer decodes binary, no duplicate JSON.
Ties: earliest time, incoming before outgoing, then lowest rotor.
Hash truth/prediction/load/shadow-gate/geometry:
case order, increasing time, incoming before outgoing, method Z/L/Q/C,
rotor 0..3; explicit record tags, uint32 integers, binary64 little-endian.
Freeze schema/hash versions/source hashes. Hashes do not prove dense maxima.
Keep all generated evidence; no deletions. Fix/review the 17-component failure
schema before writer reuse.

Archive ALL new records; omit ONLY six unchanged public sources (20,997 B),
kept locally; manifest pins paths/blob hashes.
ZIP_STORED:<=32 entries,total UTF-8 name bytes<=1,250,no extras/comments/Zip64.
Payload<=90,000-20,997=69,003; overhead 76*32+2*1,250+22=4,954; total 73,957 B
<75,000 reserve. Plus 15,000 receipts/Git checks =180,000 B, no compression
assumption. No deleted evidence/staging copies. Overlay requires pinned
source AND vendor checkout, not standalone.
Viewer<=3KB: Three.js source/receiver/rotors/support rings, case selector,
saved witnesses, protocol/results links. Label prescribed/unvalidated/sampled;
no fabricated flight/interpolated prediction.
Reuse sibling research/campaign-public-support-factorial/demo/vendor/
three.module.js and three.core.js plus existing license; no copied assets.
Readable metrics if WebGL fails; publication needs separate authorization.

## 8. Blockers
Still required: code/review, field-layout proof, failure handling, counters,
actual byte census, hash-bound release; verify logical ledger, sources, viewer
and publication permission. Charge all versions/copies. Failed ceiling means
stop before running; 250MB increase unnecessary IF 180KB fits, otherwise ask.
Full CHOPtrey, event-exposed own-state Boids, physics and matched-error
runtime/scaling remain open. Publication is not guaranteed.
