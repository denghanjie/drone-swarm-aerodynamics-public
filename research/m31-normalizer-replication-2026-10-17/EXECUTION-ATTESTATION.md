# Actual dispatch and recorded lifecycle

The parent invoked source/supervise.py kernel once and then source/supervise.py checker once. Both tools explicitly used sandbox_permissions=require_escalated. Both command environments set RESEARCH_EXECUTION_CONTEXT=tool-require-escalated, selected the pinned Node binary, used the pinned Python with-I-B, and supplied the same initially empty private raw-log directory outside Git. Source HEAD remained08ed31c184f88f95217dca689d3727c44c75e8c4through both stages.

Kernel tool session49311ended exit0, reporting success and closure. Checker tool session1730ended exit1, reporting closure with child-exit as the first failure. The saved report shows all numerical gates passed and the speed gate failed; this expected negative decision is not recast as a positive overall result. No retry occurred. The kernel consumed84.276048s and checker44.404171s according to their bounded supervision records.

This document is the parent's dispatch attestation. The independent checker validates saved context fields and lifecycle evidence; it cannot independently inspect the historical tool dispatch or detect the OS sandbox. Runtime/source identities and source publication are separately pinned. No other research benchmark or browserQAoverlapped the measured kernel. Background desktop activity was not eliminated or assigned a causal role.

Before freeze, git diff --check reported only space-only context lines within archived .patch/.diff review files. Runtime source passed its separate whitespace/syntax check. Those archival diff bytes are preserved.
