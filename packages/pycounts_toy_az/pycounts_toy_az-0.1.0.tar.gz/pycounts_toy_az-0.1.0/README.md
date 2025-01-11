# pycounts_toy_az

A toy package for counting words in a text file. DSCI524 individual assignment

## Installation

```bash
$ pip install pycounts_toy_az
```

## Usage

`pycounts_toy_az` can be used to count words in a text file and plot results
as follows:

```python
from pycounts_toy_az.pycounts import count_words
from pycounts_toy_az.plotting import plot_words
import matplotlib.pyplot as plt

file_path = "test.txt"  # path to your file
counts = count_words(file_path)
fig = plot_words(counts, n=10)
plt.show()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pycounts_toy_az` was created by Alix Zhou. It is licensed under the terms of the MIT license.

## Credits

`pycounts_toy_az` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
