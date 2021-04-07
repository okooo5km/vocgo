#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : list_stat.py
@desc          : Analyze the dataset and display the statistics
@dateTime      : 2021/04/06 17:38:25
@author        : 5km
@contact       : 5km@smslit.cn
"""

import os
from typing import Dict, Any
import xml.etree.ElementTree as ET

import typer

from .utilities import VocCallback, ANN_DIR_NAME, IMAGE_DIR_NAME, tip_info_for_dict

ARGUMENT_HELP = "The directory of VOC dataset containing two dirs(imgs and anns)"


def list_stat(directory: str) -> Dict[str, Any]:
    """analyze the VOC dataset

    Args:
        directory (str): the directory of VOC dataset

    Returns:
        Dict[str, Any]: the statistics data
    """
    anns_dir = os.path.join(directory, ANN_DIR_NAME)
    imgs_dir = os.path.join(directory, IMAGE_DIR_NAME)
    count = {
        "no_danger": 0,
        "danger": 0,
        "no_xml": [],
        "cls": {}
    }

    img_names = os.listdir(imgs_dir)
    tip_info = typer.style(
        "\nAnalyzing the directory(", fg=typer.colors.BRIGHT_BLACK)
    tip_info += typer.style(f"{directory}",
                            fg=typer.colors.BRIGHT_YELLOW)
    tip_info += typer.style(")...\n", fg=typer.colors.BRIGHT_BLACK)
    typer.echo(tip_info)
    processbar_args = {
        "length": len(img_names),
        "fill_char": "█",
        "label": "",
        "empty_char": ""
    }
    with typer.progressbar(**processbar_args) as progress:
        for img_name in img_names:
            ann_name = f"{os.path.splitext(img_name)[0]}.xml"
            ann_path = os.path.join(anns_dir, ann_name)
            if not os.path.exists(ann_path):
                count["no_xml"].append(img_name)
                continue
            xml_tree = ET.parse(ann_path)
            xml_root = xml_tree.getroot()
            if xml_root.find("object"):
                count["danger"] += 1
                for obj in xml_root.iter("object"):
                    obj_cls = obj.find("name").text
                    if obj_cls not in count["cls"]:
                        count["cls"][obj_cls] = 0
                    count["cls"][obj_cls] += 1
            else:
                count["no_danger"] += 1
            progress.update(1)

    return count


def main(directory: str = typer.Argument(default="./",
                                         callback=VocCallback.check_dir_valid,
                                         help=ARGUMENT_HELP)):
    count = list_stat(directory=directory)
    typer.echo()
    tip_info = typer.style("1. includes ", fg=typer.colors.BRIGHT_BLUE)
    tip_info += typer.style(f"{len(count['cls'])}",
                            fg=typer.colors.BRIGHT_GREEN, bold=True)
    tip_info += typer.style(" classes，the statistics of them as follows：\n\n",
                            fg=typer.colors.BRIGHT_BLUE)

    tip_info += tip_info_for_dict(count["cls"], key_width=20)
    tip_info += typer.style(f"\n2. the statistics of images as follows：\n\n",
                            fg=typer.colors.BRIGHT_BLUE)
    tip_info += tip_info_for_dict(count, only_int=True, key_width=20)
    typer.echo(tip_info)