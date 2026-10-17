# Saved-record viewer QA

Prospective UI-only check after the scientific attempt has closed. Flow: load the saved qualification → select branches/endpoints/stages/forces → verify rendered saved positions and load arrows, status and controls. No scientific imports, rerun, reference evaluation, integration or numerical-accuracy claim.

Browser plugin/skill is not available; use the existing pinned Playwright and Chrome installation. One fresh owned Chrome profile, one browser launch, at most five pages, 90-second process budget including cleanup, 16 MiB public QA output. Sources and scientific results are hashed before/after. The existing server 8876 remains unchanged.

Check desktop and mobile, title/content/console, all 18 endpoint selections and 64 stage selections, force/state association, play/pause, orbit/reset, and missing/corrupt-result initial-only behavior. Rendering floats are compared to saved positions with 2e-6 m display tolerance; this is only a GPU display check. Force arrow endpoints use the labelled 2 m/N display scale. Screenshots support layout review. Partial/failed outputs must never be replaced with invented success. No scientific result fixtures are created.

Parent may repair UI bugs and run a separately recorded QA attempt; immutable science remains untouched. The scientific run's single-attempt rule is unchanged.
