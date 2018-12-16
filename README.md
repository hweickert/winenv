Extracts the current windows environment.
Useful for starting new processes independent of the current session environment.


# Usage
```python
import subprocess
import winenv

env = winenv.get_desktopenv()
subprocess.call('cmd.exe', env=env)
```

# Functionality
- `winenv.get_sysenv()`
  Extracts the system-level environment.

- `winenv.get_userenv()`
  Extracts the user-level environment.

- `winenv.get_desktopenv()`
  Extracts the combined system- and user-level environment.
