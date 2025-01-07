## scez – single cell, easy mode
[![package](https://github.com/abearab/scez/actions/workflows/main.yml/badge.svg)](https://github.com/abearab/scez/actions/workflows/main.yml)
[![PyPI version](https://badge.fury.io/py/scez.svg)](https://badge.fury.io/py/scez)
[![Downloads](https://static.pepy.tech/badge/scez)](https://pepy.tech/project/scez)
[![Downloads](https://static.pepy.tech/badge/scez/month)](https://pepy.tech/project/scez)


### Description
There are many tools available for single-cell RNA-seq analysis, but they often require a lot of understanding of the underlying algorithms, reading of documentation, and setting up analysis environments. This takes time and effort, and can be a barrier to entry for many projects. [Single-Cell Best Practices](https://github.com/theislab/single-cell-best-practices) is a great resource for learning about the best practices for single-cell analysis. `scez` aims to provide functionalities for single-cell analysis through definitions of analysis "tasks" and implementation of these "best practices" in a user-friendly way.

This is more a personal effort to streamline my own analysis workflows, but I hope it can be useful to others as well.


### Installation
Make sure you have mamba installed in your base environment. If not, install it with:
```bash
conda install mamba -n base -c conda-forge
```
Then, create a new conda environment with the provided `environment.yml` file and activate it. This will install all necessary dependencies for scez.
```bash
conda env create -f https://raw.githubusercontent.com/abearab/scez/main/environment.yml

conda activate scez
```
Finally, install scez with:

```bash
pip install scez
```

___
Or, if you want to install the latest version from the repository:
```bash
pip install git+https://github.com/abearab/scez.git
```
