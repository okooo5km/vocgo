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


def list_stat(directory: str,
              filter_labels=None,
              anns_export_path: str = None,
              anns_dir_name: str = ANN_DIR_NAME,
              imgs_dir_name: str = IMAGE_DIR_NAME) -> Dict[str, Any]:
    """analyze the VOC dataset

    Args:
        directory (str): the directory of VOC dataset
        filter_labels (iterable obj): the necessary labels
        export_path (str): anns target path

    Returns:
        Dict[str, Any]: the statistics data
    """

    if filter_labels:
        if not anns_export_path:
            raise Exception(
                "Need to specify anns directory path if you specify the filter_labels!")
        if not os.path.exists(anns_export_path):
            raise Exception(
                "The anns path to export annotation file does not exist!")

    anns_dir_path = os.path.join(directory, anns_dir_name)
    imgs_dir_path = os.path.join(directory, imgs_dir_name)
    info = {
        "no_danger": 0,
        "danger": 0,
        "no_xml": [],
        "cls": {},
        "valid_imgs": []
    }

    img_names = os.listdir(imgs_dir_path)
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
        if filter_labels or anns_export_path:
            for img_name in img_names:
                dangerous = False
                ann_name = f"{os.path.splitext(img_name)[0]}.xml"
                ann_path = os.path.join(anns_dir_path, ann_name)
                if not os.path.exists(ann_path):
                    info["no_xml"].append(img_name)
                    continue
                xml_tree = ET.parse(ann_path)
                xml_root = xml_tree.getroot()
                to_remove = []
                if xml_root.find("object"):
                    for obj in xml_root.iter("object"):
                        obj_cls = obj.find("name").text
                        if filter_labels and (obj_cls not in filter_labels):
                            to_remove.append(obj)
                            continue
                        dangerous = True
                        if obj_cls not in info["cls"]:
                            info["cls"][obj_cls] = 0
                        info["cls"][obj_cls] += 1
                if dangerous:
                    info["danger"] += 1
                    info["valid_imgs"].append(img_name)
                    ann_export_path = os.path.join(anns_export_path, ann_name)
                    for obj in to_remove:
                        xml_root.remove(obj)
                    xml_tree.write(ann_export_path)
                else:
                    info["no_danger"] += 1
                progress.update(1)
        else:
            for img_name in img_names:
                ann_name = f"{os.path.splitext(img_name)[0]}.xml"
                ann_path = os.path.join(anns_dir_path, ann_name)
                if not os.path.exists(ann_path):
                    info["no_xml"].append(img_name)
                    continue
                xml_tree = ET.parse(ann_path)
                xml_root = xml_tree.getroot()
                if xml_root.find("object"):
                    info["danger"] += 1
                    for obj in xml_root.iter("object"):
                        obj_cls = obj.find("name").text
                        if obj_cls not in info["cls"]:
                            info["cls"][obj_cls] = 0
                        info["cls"][obj_cls] += 1
                else:
                    info["no_danger"] += 1
                progress.update(1)
    return info


def main(directory: str = typer.Argument(default="./",
                                         callback=VocCallback.check_dir_valid,
                                         help=ARGUMENT_HELP),
         anns_dir: str = typer.Option("anns", help="the annotations directory"),
         imgs_dir: str = typer.Option("imgs", help="the images directory")):
    count = list_stat(directory=directory,
                      anns_dir_name=anns_dir,
                      imgs_dir_name=imgs_dir)
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
