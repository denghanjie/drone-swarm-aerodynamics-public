# Prospective B/C equality condition

Desk observation before direct-load outcomes. No execution, target-value read, source change, mask change, or schedule change.

For one fixed candidate row x>0, let t=[tL,tU] enclose the retained defect x^3+x*s_kept. Let o=[oL,oU] enclose x times the omitted contraction, with 0<=oL<=oU. The implemented exact rational arithmetic gives:

- B defect: [tL+oL,tU+oU].
- C defect: [tL,tU+oU].

Thus B/C share U=tU+oU; C changes only the lower endpoint. With tL>0,

    kB=max(1,U,1/(tL+oL))
    kC=max(1,U,1/tL).

If tL*U>=1, then tL<=U implies U>=1, and both inverse terms are <=U. Consequently kB=kC=U. This condition is sufficient, not necessary: oL=0 already gives identical defects and factors even when the condition fails.

If the retained defect is the exact point 1, then tL=tU=1, U=1+oU>=1, and the condition automatically holds. Hence an exact solution of the retained model with exact retained contraction yields the same B/C local factor, despite C discarding a nonzero omitted lower contribution. This is a statement about the root-defect certificate, not equality of their contraction intervals.

If the sufficient condition holds for every row, all local factors agree, so their global maxima K agree. The raw corollary roots [x/(kK),min(1,x*kK)] agree, as do the subsequent outward192 roots, signed load boxes, error intervals, and tier decisions. A condition on just one row does not establish its final root equality unless the global K values also agree. Conversely, outward quantization can erase a small difference, so equal emitted roots do not prove all local factors were equal.

Exact solution of a retained mathematical model does not by itself make a computed retained interval the point 1. Finite coefficient/y enclosures can straddle the true value; the proposal also uses native force weights, coefficient midpoints, finite iterations, and native arithmetic, whereas certification uses exact weights and outward y. These distinctions can affect whether the sufficient condition holds. They do not establish that it will fail or that C will differ on any planned state.

Implication for interpretation: C isolates whether discarding the omitted lower bound changes this particular k/K certificate. It need not add slack even when its contraction interval is strictly wider. A B/C equality outcome would therefore not show that upper-only omission has no uncertainty; it would show that the certificate's maximum is insensitive to that added lower-end uncertainty for the evaluated candidate. A B-pass/C-not-certified branch remains logically possible outside the equality condition. No outcome is predicted, and the fixed A/B/C diagnostic remains unchanged.
