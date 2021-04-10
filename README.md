# VOCGO

VOCGO is a simple tool for VOC dataset that can help to analyze and process the dataset, and it has a intresting chinese name - [窝酷狗].

VOCGO uses [poetry](https://python-poetry.org/) to build the package and manage the dependece.

## python 

```
>=python3.6.7
```

## Installing

### pip

```shell
pip install cocogo
```

### poetry

```shell
# clone the Repository
git clone https://github.com/smslit/cocogo.git
# install
cd cocogo && poetry install
```

## Development

execute the follow command after installing poetry:

```shell
# only install the depedence
poetry install --no-root
```

## Usage

```shell
➜ vocgo --help     
Usage: vocgo [OPTIONS] COMMAND [ARGS]...

  This is a simple tool for VOC dataset, it can help you analyze and process
  the dataset, its chinese name is 「窝酷狗」，more details to
  https://github.com/smslit/vocgo

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

Commands:
  generate  generate the train files for model training and evaluating
  list      analyze the dataset and display the statistics
  version   display the version info
```

### list

The subcommand can analyze the specified VOC dataset and display the statistics data.

For example:

```shell
vocgo list ./
```

<img src="https://pichome-1254392422.cos.ap-chengdu.myqcloud.com/uPic/list-20210410170643.png" width="420px">

### split

This subcommad can help to split the dataset and generate the data files(train.txt valid.txt label_list.txt) based on anns and imgs data. It will display the spliting details!

We can specify some labels to filter the necessary data, and specify a diretory to export training files.

For example:

```shell
vocgo split --labels=mask,no_mask --ratio=0.9 ./
```

<img src="https://pichome-1254392422.cos.ap-chengdu.myqcloud.com/uPic/split-20210410170657.png" width="640px">