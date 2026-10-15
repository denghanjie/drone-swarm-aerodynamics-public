# Static launcher accounting correction

Before any reviewer invocation, coordinator static review required the 16 MiB output ledger to include copied archive inputs as newly emitted bytes. `launcher.py` now counts every regular archive file (including exact checker, input index, invocation, arguments, preparation, launcher, stdout, stderr and runtime), plus the generated review JSON and both permanent locks. Runtime is included once through archive traversal. `outputBytesBeforeRuntime` therefore covers the full emitted prefix, with the existing 8 KiB final-runtime reserve.

No checker, scientific data, numerical gate, input index, argument or prospective invocation manifest changed. The checker and launcher remain unexecuted; no typed scientific arrays were decoded. This note records only a static bookkeeping correction. The original review preparation remains pinned by the unchanged invocation manifest.
