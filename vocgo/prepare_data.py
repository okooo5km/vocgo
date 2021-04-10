#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : prepare_data.py
@desc          : Split the dataset and generate the train files 
                 for model training and evaluating 
@dateTime      : 2021/04/07 15:45:39
@author        : 5km
@contact       : 5km@smslit.cn
"""

import os
import shutil
import os.path as osp
from typing import Dict
from random import shuffle

import typer

from .utilities import VocCallback, tip_info_for_dict
from .list_stat import ARGUMENT_HELP, list_stat

RATIO_HELP = "The distribution ratio of model training and evaluating"
LABEL_SORT_HELP = "The sort type for class label"


def save_datapath_to_txt(imgs, save_file):
    if osp.exists(save_file):
        os.remove(save_file)
    with open(save_file, "w") as f:
        for img in imgs:
            ann = osp.splitext(img)[0] + ".xml"
            line = f"./imgs/{img} ./anns/{ann}\n"
            f.write(line)


def prepare_train_valid_data(data_dir, imgs, train_ratio) -> Dict[str, int]:
    img_n = len(imgs)
    train_n = int(img_n*train_ratio)

    shuffle(imgs)

    save_datapath_to_txt(imgs[0:train_n], osp.join(data_dir, "train.txt"))
    save_datapath_to_txt(imgs[train_n:img_n], osp.join(data_dir, "valid.txt"))

    return {
        "train": train_n,
        "valid": img_n - train_n
    }


def prepare_lable_list(data_dir, labels):
    with open(osp.join(data_dir, "label_list.txt"), "w") as f:
        for label in labels:
            f.write(f"{label}\n")


def main(directory: str = typer.Argument(default="./",
                                         callback=VocCallback.check_dir_valid,
                                         help=ARGUMENT_HELP),
         ratio: float = typer.Option(default=1.0, help=RATIO_HELP),
         labels: str = typer.Option(None, help="The label to learn", ),
         export_dir: str = typer.Option(None, help="The exporting dir path of the training files")):

    directory = os.path.abspath(directory)
    if not export_dir:
        export_dir = typer.prompt(
            "\nPlease specify a exporting directory name")
    export_dir_path = os.path.join(directory, export_dir)
    imgs_path = os.path.join(directory, "imgs")

    # confirm to create the export directory
    if os.path.exists(export_dir_path):
        typer.secho(f"\nThe directory 「{export_dir}」 exists!",
                    fg=typer.colors.BRIGHT_YELLOW)
        override = typer.confirm("\nDo you overide it?")
        if not override:
            export_dir = typer.prompt(
                "\nPlease specify a exporting directory name")
            export_dir_path = os.path.join(directory, export_dir)
        else:
            shutil.rmtree(export_dir_path)
    os.makedirs(export_dir_path)

    # link the imgs directory
    imgs_export_path = os.path.join(export_dir_path, "imgs")
    anns_export_path = os.path.join(export_dir_path, "anns")
    link_imgs_command = f"ln -s {imgs_path} {imgs_export_path}"
    os.system(link_imgs_command)
    os.makedirs(anns_export_path, exist_ok=True)

    if "," in labels:
        label = labels.split(",")
    else:
        label = [labels]

    info = list_stat(directory=directory,
                     filter_labels=label,
                     anns_path=anns_export_path)

    labels = sorted(list(info["cls"].keys()))

    # generate train.txt、 valid.txt
    count = prepare_train_valid_data(export_dir_path,
                                     info["valid_imgs"],
                                     ratio)
    # generate label_list
    prepare_lable_list(export_dir_path, labels)

    tip_info = "\n"
    tip_info += tip_info_for_dict({
        "voc dir": os.path.relpath(export_dir_path),
        "train file": os.path.relpath(os.path.join(export_dir_path, "train.txt")),
        "valid file": os.path.relpath(os.path.join(export_dir_path, "valid.txt")),
        "label list": os.path.relpath(os.path.join(export_dir_path, "label_list.txt")),
        "train labels": ", ".join(labels),
        "ratio": ratio,
    }, key_width=15)
    tip_info += tip_info_for_dict(count, key_width=15)
    tip_info += typer.style("\nSplit the dataset and export files to ",
                            fg=typer.colors.BRIGHT_BLACK)
    tip_info += typer.style(f"{export_dir_path}",
                            fg=typer.colors.BRIGHT_GREEN, bold=True)
    tip_info += typer.style(" successfully!", fg=typer.colors.BRIGHT_BLACK)
    typer.echo(tip_info)
