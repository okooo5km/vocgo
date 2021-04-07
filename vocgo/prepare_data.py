#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : prepare_data.py
@desc          : Generate the train files for model training and evaluating 
@dateTime      : 2021/04/07 15:45:39
@author        : 5km
@contact       : 5km@smslit.cn
"""

import os
import os.path as osp
from enum import Enum
from random import shuffle
from typing import Dict, List

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


def prepare_train_valid_data(data_dir, train_ratio) -> Dict[str, int]:
    img_dir = osp.join(data_dir, "imgs")

    imgs = os.listdir(img_dir)
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
         ratio: float = typer.Option(default=1.0, help=RATIO_HELP)):
    count = list_stat(directory=directory)
    labels = list(count["cls"].keys())

    # generate train.txt、 valid.txt
    count = prepare_train_valid_data(directory, ratio)
    # generate label_list
    prepare_lable_list(directory, labels)

    tip_info = "\n"
    tip_info += tip_info_for_dict({
        "voc dir": directory,
        "labels": ", ".join(labels),
        "ratio": ratio,
    }, key_width=10)
    tip_info += tip_info_for_dict(count, key_width=10)
    typer.echo(tip_info)
    typer.secho("Generate train.txt valid.txt label_list.txt successfully!",
                fg=typer.colors.BRIGHT_BLUE)


if __name__ == "__main__":
    data_dir = "/data/tianye/paddle/PaddleDetection/dataset/bank"
    train_ratio = 1.0
    labels = ['customer', 'security', 'teller']

    # 创建train.txt、valid.txt
    prepare_train_valid_data(data_dir, train_ratio)

    # 创建label_list
    prepare_lable_list(data_dir, labels)
