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
from . import version, list_stat, prepare_data, rename_labels, remove_labels, normalize

app = typer.Typer(help=__description__)

app.command("version", help="Display the version info")(version.main)
app.command("list", help="Analyze the dataset and display the statistics")(
    list_stat.main)
app.command("split", help="Split the dataset and generate the train files for model training and evaluating")(
    prepare_data.main)
app.command("rename", help="Rename the specified labels")(rename_labels.main)
app.command("remove", help="Remove the specified labels")(remove_labels.main)
app.command("normalize", help="Calculate the normalization parameters")(
    normalize.main)
