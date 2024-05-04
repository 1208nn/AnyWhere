# pylint: disable=missing-module-docstring,missing-function-docstring,missing-class-docstring
import sys
import os
import shutil
import CurrOS

operation_type, arg = sys.argv[1].split(":")[1].split("/", maxsplit=1)
if operation_type == "install":
    shutil.move(
        os.path.join(os.environ["TEMP"], "AnyWhere", arg),
        os.path.join(CurrOS.appdata_path, "n0", "AnyWhere", arg),
    )
elif operation_type == "check":
    pass  # Not Developed Yet
elif operation_type == "decline":
    os.remove(os.path.join(os.environ["TEMP"], "anywhere", arg))
