# Static challenge of the prospective transport protocol

Disposition: **protocol scope cleared for preparation after two clarifications.** No invocation has been reviewed as ready to launch, and no worker or verifier was executed for this challenge.

Reviewed document: `research/m31-transport-diagnostic-2026-10-16/PROTOCOL.md`, prospective text with one 3,840-byte synthetic payload, one 60-second diagnostic allowance, and one later 30-second saved-evidence review.

The protocol keeps the new question distinct from the closed scientific attempts. It fixes the synthetic bytes and relevant transport semantics; excludes GPU calls, scientific imports, old outputs, retries and automatic numerical continuation; requires browser/server observations before fetch; separates persistence from acknowledgement; documents that heap-backed bytes cannot reproduce GPU-mapped backing storage; and preserves the old failure, failed review, physical gaps, and launch cutoff. Its source freeze, publication, independent verification, resource caps and later bounded saved-only review are explicit.

The following two requests were made and then verified as addressed in the revised protocol:

1. Replace “Exactly one new worker/browser lifecycle” with “Exactly one diagnostic worker invocation and at most one browser lifecycle.” An invocation consumed by source admission or instrumentation failure may stop before browser creation; it must be preserved as failure rather than forced into a success-shaped lifecycle schema.
2. State decision-table precedence: missing or truncated instrumentation, an unavailable required observer, cap breach, or incomplete lifecycle makes the overall diagnostic incomplete/inconclusive. Narrower raw facts may still be reported, but absence of a POST or an event cannot support a negative observation from an incomplete trace. The success row already requires complete instrumentation and lifecycle; the same coverage rule should explicitly govern failure-boundary interpretations.

These clarifications do not enlarge the allocation or authorize a retry. Draft implementation must still be independently challenged for actual enforcement, capture completeness, source/evidence binding, ownership, privacy, and terminal behavior. The later verifier must use explicit producer/consumer projections, permit early failure, and retain an unsuccessful diagnostic as distinct from an inconsistent saved record.

Static byte inspection also confirms that the new `payload.bin` is 3,840 bytes with SHA-256 `b92773fc3edb949a8a0d6e4a2f60ef2020ee2bd5bf6f8299c1448142a6cd3404`, matching the new fixture descriptor. No payload was sent and no scientific computation was performed.
