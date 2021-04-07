#!/usr/bin/env python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : main.py
@desc          : This is a simple tool for VOC dataset, 
                 it can help you analyze and process the dataset, 
                 its chinese name is 「窝酷狗」
@dateTime      : 2021/04/06 17:28:05
@author        : 5km
@contact       : 5km@smslit.cn
"""
import typer

from .consts import __description__
from . import version, list_stat, prepare_data

app = typer.Typer(help=__description__)

app.command("version", help="display the version info")(version.main)
app.command("list", help="analyze the dataset and display the statistics")(
    list_stat.main)
app.command("generate", help="generate the train files for model training and evaluating")(
    prepare_data.main)
