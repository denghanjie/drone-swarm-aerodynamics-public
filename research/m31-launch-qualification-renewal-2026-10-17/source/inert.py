"""Fixed harmless child. No research imports, subprocesses or network."""
import json
import sys
import time
from pathlib import Path
case, directory = sys.argv[1:]
if case == 'child-timeout':
    time.sleep(3)
elif case == 'child-exit7':
    sys.exit(7)
else:
    with (Path(directory) / 'inert-output.json').open('x') as f:
        json.dump({'inert': True, 'case': case}, f)
