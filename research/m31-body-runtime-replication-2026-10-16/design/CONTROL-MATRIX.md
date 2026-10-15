# Fixed control matrix v1

Source only. `buildControls` is an explicit scientific-envelope operation, not import-time work. It produces all raw fixtures once, before GPU dispatch. Original f64 control operands and packed u32 packets are both retained. No adaptive additions, reruns, value search or replacement.

All pair fixtures have receiver position zero, rotor offset `(.028,.028,0)`, source and receiver axes +z, receiver ID0/source ID1, unless stated. P00 uses source ID0. For displacement d, source position is `offset+d`, using original binary64 addition then one f32 packing. Constants are original for R, exact decoded packed for Q/GPU.

| ID | Fixed original definition | Terminal symbol | GPU validity | R/Q validity |
|---|---|---:|---:|---:|
| P00 | Self ID and identical node | 1 | 17 | 1 |
| P01 | Source center `(3,0,0)` | 1 | 17 | 17 |
| P02 | Source center `(nextDown32(3),0,0)` | 2 | 19 | 19 |
| P03 | d=`(.4,0,0)` | 2 | 19 | 19 |
| P04 | d=`(.4,0,-.25)` | 2 | 19 | 19 |
| P05 | d=`(0,0,2.5)` | 3 | 19 | 19 |
| P06 | d=`(0,0,2.75)` | 3 | 19 | 19 |
| P07 | d=`(0,0,D)` | 4, expected domain rejection | 22 | 22 |
| P08 | d=`(.25,0,D)` | 5 | 23 | 23 |
| P09 | d=`(.75,0,.6)` | 6 | 23 | 23 |
| P10 | d=`(0,0,.6)` | 8 | 31 | 31 |
| P11 | d=`(.02,0,2.25)` | 8 | 31 | 31 |
| P12 | d=`(.2,0,.6)` | 8 | 31 | 31 |
| P13 | d=`(.5,0,2.25)` | 8 | 31 | 31 |
| P14 | d=`(0,0,.6)`, receiver axis +x; explicit low-level tilt bypass | 7 | 31 | 31 |

P15 passes P14's prepared node to full admission and must reject `BodyContractError: Global tilt admission`. P14 does not describe an admitted main scene. Pair positive symbols require positive terms; all valid zero classes require +0. No separate pointwise numerical accuracy gate is invented.

Root controls are IDs0..143: 16 original nominal definitions crossed with nine inflow definitions, ID=`9*nominalIndex+inflowIndex`. Let d=`2^-149`, n=`2^-126`, m=`n-d/2`, fmax=`((2.25*.027)*9.81)/4` with exactly that grouping.

| Nominal index | Original binary64 nominal |
|---:|---|
| 0 | +0 |
| 1 | 2^-1074 |
| 2 | 2^-151 |
| 3 | 2^-150 |
| 4 | nextUp64(2^-150) |
| 5 | d |
| 6 | n-d |
| 7 | m |
| 8 | nextDown64(m) |
| 9 | n |
| 10 | n+d |
| 11 | 2^-32 |
| 12 | 2^-16 |
| 13 | fmax/64 |
| 14 | fmax/2 |
| 15 | fmax |

For each nominal, if its packed word is normal positive, compute the **input-construction** value `vstar=RN32(sqrt(RN32(nPacked/RN32(RN32(2*rhoPacked)*areaPacked))))` once. Otherwise use exactly1. This is an explicitly charged host approximation, not an expected device sqrt result. Inflow indices0..8 are `[+0,d,n,1/4,4,2^20,nextDown32(vstar),vstar,nextUp32(vstar)]`. Keep duplicate values as distinct fixtures. Branch acceptance uses saved actual GPU vi/U; branch identities are not predicted from the host sqrt.

ID144 is `(nominal=-0,U=1/4)`; ID145 is `(nominal=fmax/2,U=-0)`. Nominal-zero canonicalization takes precedence. Controls use the same raw-input H solve and main direct rotor/H residual gates. R/Q/H references run once per scalar each (438 attempts, at most42048 bisection iterations); GPU positive branches perform exactly12 updates (at most1752). No controls repeat four equivalent rotor solves.

The 12 additional host admission/record controls must raise the exact named `BodyContractError`; unrelated exceptions, including deadline/work-cap/TypeError, are rethrown as terminal failures:

| ID | Input | Required message |
|---|---|---|
| A00 | Original nominal -2^-149 | Original nominal |
| A01 | Original nominal nextUp64(fmax) | Original nominal |
| A02 | Original quaternion component NaN | Original finite17 |
| A03 | Original position component +Infinity | Original finite17 |
| A04 | Zero quaternion | Original quaternion norm |
| A05 | Original position x=129 | Original position |
| A06 | Decoded packed pad1 | Nonzero prepared pad |
| A07 | State length16 | Original finite17 |
| A08 | Source ID2 with N2 | Pair identifiers |
| A09 | Synthetic term nextUp32(128) | Term limit |
| A10 | Synthetic sum nextUp32(2^20) | Sum limit |
| A11 | Unwritten required GPU output header | Unwritten header |

The16 decoder controls supply each literal symbol0..15 to the shared policy-class decoder: symbols1..3 map to classes0..2,5..7 to4..6,8/9 to7;0,4,10..15 reject. They are decoding controls, not manufactured profile observations. The main assessment itself enforces every N² required slot and exact positive counts.

No GPU body-injection controls or claim of GPU body-invalidity coverage is added. Every main body output is covered by direct original-R gates, and its f64 recomposition from saved operands is diagnostic only.
