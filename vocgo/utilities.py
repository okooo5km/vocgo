#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : utilities.py
@desc          : Usual methods
@dateTime      : 2021/04/07 13:30:26
@author        : 5km
@contact       : 5km@smslit.cn
"""

import os
import shutil
from typing import Dict, Any

import typer

ANN_DIR_NAME = "anns"
IMAGE_DIR_NAME = "imgs"


class VocCallback:

    @staticmethod
    def check_dir_valid(value: str):
        """check the directory of VOC dataset
        """
        if not os.path.exists(value):
            raise typer.BadParameter(f"{value} NOT EXIST!")
        if os.path.isfile(value):
            raise typer.BadParameter(
                f"{value} is a file，please specify a valid directory!")
        return value


def tip_info_for_dict(dict_data: Dict[str, Any], key_width: int = 20, only_int=False) -> str:
    """produce the echo tip info for dict data

    Args:
        dict_data (dict): dict data
        key_width (int): the key display character width
        only_int (bool): only display the item(the value is int instance) 

    Returns:
        [str]: the tip info string
    """
    tip_info = ""
    for key, value in dict_data.items():
        if (not isinstance(value, int)) and only_int:
            continue
        tip_info += typer.style(f"{key:>{key_width}}",
                                fg=typer.colors.BRIGHT_YELLOW, bold=True)
        tip_info += typer.style(" : ", fg=typer.colors.BRIGHT_BLACK)
        tip_info += typer.style(f"{value}\n",
                                fg=typer.colors.BRIGHT_GREEN, bold=True)
    return tip_info


def check_and_make_dir(root_path,
                       dir_name,
                       promp_str: str = "\nPlease input another one") -> str:
    # confirm to create the export directory
    path = os.path.join(root_path, dir_name)
    if os.path.exists(path):
        typer.secho(f"\nThe directory 「{path}」 exists!",
                    fg=typer.colors.BRIGHT_YELLOW)
        override = typer.confirm("\nDo you overide it?")
        if not override:
            export_dir = typer.prompt(promp_str)
            path = os.path.join(root_path, export_dir)
        else:
            shutil.rmtree(path)
    os.makedirs(path)

    return path
