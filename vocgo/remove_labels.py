#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : remove_labels.py
@desc          : 
@dateTime      : 2021/05/28 14:52:36
@author        : 5km
@contact       : 5km@smslit.cn
"""

import os
import typer
import xml.etree.ElementTree as ET

from vocgo.list_stat import ARGUMENT_HELP
from .utilities import VocCallback, check_and_make_dir

LABELS_PROMP_TIP = "\n1. Which labels do you want to remove?"\
    "(You can use subcommand - list - to check labels!)\n"\
    "Need comma between labels [e.g. person,bike,kite]"


def main(directory: str = typer.Argument(default="./",
                                         callback=VocCallback.check_dir_valid,
                                         help=ARGUMENT_HELP),
         anns_dir: str = typer.Option("anns", help="the annotations directory"),
         imgs_dir: str = typer.Option("imgs", help="the images directory")
         ):
    labels_str: str = typer.prompt(LABELS_PROMP_TIP).replace(" ", "")
    labels_to_merge = labels_str.split(",")

    anns_export_dir: str = typer.prompt(
        "\n2. Which directory to export the new annotation files into"
    ).replace(" ", "")

    anns_path = os.path.join(directory, anns_dir)
    imgs_path = os.path.join(directory, imgs_dir)

    anns_export_path = check_and_make_dir(root_path=directory,
                                          dir_name=anns_export_dir)

    image_names = os.listdir(imgs_path)

    typer.secho(f"\nRemoving {labels_str} ...",
                fg=typer.colors.BRIGHT_BLACK)

    processbar_args = {
        "length": len(image_names),
        "fill_char": "█",
        "label": "",
        "empty_char": ""
    }

    with typer.progressbar(**processbar_args) as progress:
        for image_name in image_names:
            progress.update(1)
            ann_name = f"{os.path.splitext(image_name)[0]}.xml"
            ann_path = os.path.join(anns_path, ann_name)
            ann_export_path = os.path.join(anns_export_path, ann_name)
            if not os.path.exists(ann_path):
                continue
            xml_tree = ET.parse(ann_path)
            xml_root = xml_tree.getroot()
            if not xml_root.find("object"):
                continue
            objs_to_rm = []
            for obj in xml_root.iter("object"):
                obj_name = obj.find("name")
                if obj_name.text in labels_to_merge:
                    objs_to_rm.append(obj)
            try:
                [xml_root.remove(obj) for obj in objs_to_rm]
            except Exception as e:
                typer.secho("Remove the objs error",
                            fg=typer.colors.BRIGHT_RED)
            if xml_root.find("object"):
                xml_tree.write(ann_export_path)

    typer.secho(f"\nDone",
                fg=typer.colors.BRIGHT_BLACK)
