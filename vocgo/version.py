#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : version.py
@desc          : display the version info
@dateTime      : 2021/04/06 17:32:47
@author        : 5km
@contact       : 5km@smslit.cn
"""

import typer
from .consts import __version__


def main():
    typer.echo()
    typer.secho(f"  v{__version__}", fg=typer.colors.BRIGHT_YELLOW, bold=True)
