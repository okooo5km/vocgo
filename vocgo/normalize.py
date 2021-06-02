#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : normalize.py
@desc          :
@dateTime      : 2021/06/02 10:40:46
@author        : 5km
@contact       : 5km@smslit.cn
"""

import os
import threading
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

import cv2
import typer
import numpy as np

from .utilities import VocCallback
from vocgo.list_stat import ARGUMENT_HELP


class NormalizationMethod(str, Enum):
    z_score = "Z-score"


lock = threading.Lock()


class ZScore():

    image_Rmean = []
    image_Gmean = []
    image_Bmean = []

    image_R_std = []
    image_G_std = []
    image_B_std = []

    @classmethod
    def compute_mean(cls, img_path, progress):
        img = cv2.imread(img_path)
        per_image_Bmean = np.mean(img[:, :, 0] / 255.0)
        per_image_Gmean = np.mean(img[:, :, 1] / 255.0)
        per_image_Rmean = np.mean(img[:, :, 2] / 255.0)

        per_image_B_std = np.std(img[:, :, 0] / 255.0)
        per_image_G_std = np.std(img[:, :, 1] / 255.0)
        per_image_R_std = np.std(img[:, :, 2] / 255.0)

        lock.acquire()
        cls.image_Rmean.append(per_image_Rmean)
        cls.image_Gmean.append(per_image_Gmean)
        cls.image_Bmean.append(per_image_Bmean)

        cls.image_R_std.append(per_image_R_std)
        cls.image_G_std.append(per_image_G_std)
        cls.image_B_std.append(per_image_B_std)
        progress.update(1)
        lock.release()


def main(directory: str = typer.Argument(default="./",
                                         callback=VocCallback.check_dir_valid,
                                         help=ARGUMENT_HELP),
         method: NormalizationMethod = typer.Option(
             NormalizationMethod.z_score, help="Normalization method")
         ):
    typer.secho(f"\nChecking the directory {directory} ...\n",
                fg=typer.colors.BRIGHT_BLACK)

    valid_dfiles = []
    names = os.listdir(directory)
    for name in names:
        if not name.endswith(".txt"):
            continue
        path = os.path.join(directory, name)
        if os.path.isdir(path):
            continue
        with open(path, "r") as f:
            line = f.readline().strip()
            file_paths = line.split(" ")
            if len(file_paths) != 2:
                continue
            if os.path.splitext(file_paths[0])[1].lower() != ".jpg" \
                    or os.path.splitext(file_paths[1])[1].lower() != ".xml":
                continue
        valid_dfiles.append(name)
        typer.secho(f"  {len(valid_dfiles)}. {name}",
                    fg=typer.colors.BRIGHT_GREEN)

    if len(valid_dfiles) == 0:
        typer.secho("Have no valid dataset file!",
                    fg=typer.colors.BRIGHT_YELLOW)
        return
    choices = [i + 1 for i in range(len(valid_dfiles))]
    prompt_tip = typer.style(f"\nPlease choose the dataset file, give a num from {choices}",
                             fg=typer.colors.BRIGHT_YELLOW)
    file_no = typer.prompt(prompt_tip, type=int)
    while file_no not in choices:
        file_no = typer.prompt(prompt_tip, type=int)

    typer.secho("\nCalculating the normalization parameters with Z-Score ...\n",
                fg=typer.colors.BRIGHT_BLACK)

    dataset_file = os.path.join(directory, valid_dfiles[file_no - 1])
    image_paths = []
    with open(dataset_file, "r") as f:
        for line in f:
            file_paths = line.split(" ")
            image_path = os.path.join(directory, file_paths[0])
            image_paths.append(image_path.replace("./", ""))
    processbar_args = {
        "length": len(image_paths),
        "fill_char": "█",
        "label": "",
        "empty_char": ""
    }

    with typer.progressbar(**processbar_args) as progress:
        with ThreadPoolExecutor(max_workers=40) as t:
            for img_path in image_paths:
                t.submit(ZScore.compute_mean, img_path, progress)

    R_mean = np.mean(ZScore.image_Rmean)
    G_mean = np.mean(ZScore.image_Gmean)
    B_mean = np.mean(ZScore.image_Bmean)

    R_std = np.std(ZScore.image_R_std)
    G_std = np.std(ZScore.image_G_std)
    B_std = np.std(ZScore.image_B_std)

    tips = typer.style("\nNormalization Parameters as follows\n",
                       fg=typer.colors.BRIGHT_YELLOW)
    result = f"  - mean: [{R_mean:.4f}, {G_mean:.4f}, {B_mean:.4f}]\n"
    result += f"  - std: [{R_std:.4f}, {G_std:.4f}, {B_std:.4f}]"
    tips += typer.style(result,
                        fg=typer.colors.BRIGHT_BLUE,
                        bold=True)
    typer.echo(tips)
