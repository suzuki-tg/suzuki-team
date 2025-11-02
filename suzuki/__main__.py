"""Entry point. Checks for user and starts main script"""

# ©️ Suzuki Team, 2023-2024
# This file is a part of Suzuki Userbot
# 🌐 https://github.com/suzuki-team/Suzuki
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import getpass
import os
import subprocess
import sys

from ._internal import restart

if (
    getpass.getuser() == "root"
    and "--root" not in " ".join(sys.argv)
    and all(trigger not in os.environ for trigger in {"DOCKER", "GOORM"})
):
    print("🚫" * 15)
    print("You attempted to run Suzuki on behalf of root user")
    print("Please, create a new user and restart script")
    print("If this action was intentional, pass --root argument instead")
    print("🚫" * 15)
    print()
    print("Type force_insecure to ignore this warning")
    if input("> ").lower() != "force_insecure":
        sys.exit(1)


def deps():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "-q",
            "--disable-pip-version-check",
            "--no-warn-script-location",
            "-r",
            "requirements.txt",
        ],
        check=True,
    )


if sys.version_info < (3, 8, 0):
    print("🚫 Error: you must use at least Python version 3.8.0")
elif __package__ != "suzuki":  # In case they did python __main__.py
    print("🚫 Error: you cannot run this as a script; you must execute as a package")
else:
    try:
        import suzuki_tl
    except Exception:
        pass
    else:
        try:
            import suzuki_tl  # noqa: F811

            if tuple(map(int, suzuki_tl.__version__.split("."))) < (2, 0, 4):
                raise ImportError

            import suzuki_pyro

            if tuple(map(int, suzuki_pyro.__version__.split("."))) < (2, 0, 103):
                raise ImportError
        except ImportError:
            print("🔄 Installing dependencies...")
            deps()
            restart()

    try:
        from . import log

        log.init()

        from . import main
    except ImportError as e:
        print(f"{str(e)}\n🔄 Attempting dependencies installation... Just wait ⏱")
        deps()
        restart()

    if "SUZUKI_DO_NOT_RESTART" in os.environ:
        del os.environ["SUZUKI_DO_NOT_RESTART"]

    main.suzuki.main()  # Execute main function