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
        file_dirs = os.listdir(value)
        if ANN_DIR_NAME not in file_dirs or IMAGE_DIR_NAME not in file_dirs:
            msg = typer.style(f"The DIRECTORY {value} does not containes {ANN_DIR_NAME} or {IMAGE_DIR_NAME}",
                              fg=typer.colors.BRIGHT_RED)
            raise typer.BadParameter(msg)
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
