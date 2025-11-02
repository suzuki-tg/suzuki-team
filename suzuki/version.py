"""Represents current userbot version"""
# ©️ Suzuki Team, 2025
# This file is a part of Suzuki Userbot
# 🌐 https://github.com/suzuki-team/Suzuki
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

__version__ = (1, 0, 0)

import os

import git

try:
    branch = git.Repo(
        path=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ).active_branch.name
except Exception:
    branch = "master"