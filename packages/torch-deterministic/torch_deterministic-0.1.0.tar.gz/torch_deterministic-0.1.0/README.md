Torch Deterministic
===================

[![Last release](https://img.shields.io/pypi/v/torch_deterministic.svg)](https://pypi.python.org/pypi/torch_deterministic)
[![Python version](https://img.shields.io/pypi/pyversions/torch_deterministic.svg)](https://pypi.python.org/pypi/torch_deterministic)
[![Documentation](https://img.shields.io/readthedocs/torch_deterministic.svg)](https://torch-deterministic.readthedocs.io/en/latest/)
[![Test status](https://img.shields.io/github/actions/workflow/status/kalekundert/torch_deterministic/test.yml?branch=master)](https://github.com/kalekundert/torch_deterministic/actions)
[![Test coverage](https://img.shields.io/codecov/c/github/kalekundert/torch_deterministic)](https://app.codecov.io/github/kalekundert/torch_deterministic)
[![Last commit](https://img.shields.io/github/last-commit/kalekundert/torch_deterministic?logo=github)](https://github.com/kalekundert/torch_deterministic)

*Torch Deterministic* is a library for making PyTorch datasets with 
deterministic and easily reproducible augmentations.  More specifically, this 
library is meant to facilitate the following paradigm:

- None of the global PyTorch pseudorandom number generators (PRNGs) are used.
- Every time the dataset is indexed, a new PRNG is seeded with that index 
  number.  This PRNG is used for all randomness needed to make the data point 
  in question.



