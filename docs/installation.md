# Installation

## Stable release

To install montecarlo, run this command in your terminal:

```sh
uv add montecarlo
```

Or if you prefer to use `pip`:

```sh
pip install montecarlo
```

## From source

The source files for montecarlo can be downloaded from the [Github repo](https://github.com/aaron/montecarlo).

You can either clone the public repository:

```sh
git clone https://github.com/aaron/montecarlo
```

Or download the [tarball](https://github.com/aaron/montecarlo/tarball/main):

```sh
curl -OJL https://github.com/aaron/montecarlo/tarball/main
```

Once you have a copy of the source, you can install it with:

```sh
cd montecarlo
uv sync
```
You will need an environment with the following packages: 
*Python 3.11
*NumPy
*MatPlotLib
Once you have these packages installed, you can install montecarlo in the same environment using 
```sh 
pip install -e.
```
from the top-level montecarlo/directory 


