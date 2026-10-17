# Browser calculation completed; supervisor stage failed

Source commit: e6f99b140c70887fa0ed05c14574221eb5db12da. The single authorized browser invocation ran on 2026-10-17. All twelve target calls and fixed controls were saved; the controller records complete=true, no errors, Chrome closed and source/input preservation. The child returned zero. The outer supervisor then recorded PermissionError (EPERM), cleanupError=true and exitCode=1 during its group-cleanup path. Its overall browser stage is **failed**. Do not relabel or rerun it.

The originally conditional checker was not launched; its completion prerequisite was not met. That original allocation is now closed without checker execution. Raw browser records are available but not yet numerically qualified. Do not promote internal complete=true into an overall run pass.

A subsequent read-only elevated process inspection found neither of the two recorded guardian/child PIDs. This does not prove all descendants were gone or the exact cause of EPERM. A separate postrun hash check found all 306 source pins unchanged and verified the browser journal hash, record count, sequence and equality of saved target records with the final browser JSON. These postrun checks do not retroactively satisfy the interrupted original supervisor.

The next proposed operation is a separately frozen saved-record audit, with no browser replay or replacement targets. Its numerical findings would apply to the existing returned words only and retain the operational failure. See the separate m31-native-saved-audit-2026-10-17 package.
