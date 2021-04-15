#!/usr/bin/env python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@fileName      : main.py
@desc          : VOCGO is a simple tool for VOC dataset 
                 that can help to analyze and process the dataset, 
                 and it has a intresting chinese name - [窝酷狗].
@dateTime      : 2021/04/06 17:28:05
@author        : 5km
@contact       : 5km@smslit.cn
"""
import typer

from .consts import __description__
from . import version, list_stat, prepare_data, merge_labels

app = typer.Typer(help=__description__)

app.command("version", help="Display the version info")(version.main)
app.command("list", help="Analyze the dataset and display the statistics")(
    list_stat.main)
app.command("split", help="Split the dataset and generate the train files for model training and evaluating")(
    prepare_data.main)
app.command("merge", help="Merge the specified labels")(merge_labels.main)
