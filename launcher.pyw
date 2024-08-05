# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
import sys
import os
import subprocess
import shutil
import CurrOS

if getattr(sys, "frozen", False):
    py_packed = True
    app_dir = os.path.dirname(sys.executable)
else:
    py_packed = False
    app_dir = os.path.dirname(__file__)
os.chdir(app_dir)
if len(sys.argv) == 1:
    subprocess.Popen(["AnyWhere"] if py_packed else ["pythonw", "AnyWhere.py"])
    sys.exit(0)


operation_type, arg = sys.argv[1].split(":")[1].split("/", maxsplit=1)
if operation_type == "install":
    shutil.move(
        os.path.join(os.environ["TEMP"], "AnyWhere", arg),
        os.path.join(CurrOS.appdata_path, "n0", "AnyWhere", arg),
    )
elif operation_type == "check":
    pass  # TODO:Not Developed Yet
elif operation_type == "dismiss":
    os.remove(os.path.join(os.environ["TEMP"], "anywhere", arg))
elif operation_type == "mute":
    pass  # TODO:mute
