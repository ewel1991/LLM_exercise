# system_info.py
import os
import platform
import sys
import subprocess
from datetime import datetime


def _run(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=isinstance(cmd, str),
            stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:
        return ""


def get_system_info():
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",

        "os": {
            "name": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "arch": platform.machine(),
        },

        "python": {
            "version": sys.version.split()[0],
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        },

        "cpu": {
            "cores_logical": os.cpu_count() or 0,
            "brand": (
                _run("grep -m1 'model name' /proc/cpuinfo | cut -d: -f2")
                or _run(["sysctl", "-n", "machdep.cpu.brand_string"])
                or _run(
                    'powershell -NoProfile -Command '
                    '"(Get-CimInstance Win32_Processor).Name"'
                )
            ).strip(),
        },
    }
