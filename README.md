<!---
  This file is part of Inspire-Magpie.
  Copyright (c) 2016 CERN

  Inspire-Magpie is a free software; you can redistribute it and/or modify it
  under the terms of the MIT License; see LICENSE file for
  more details.
-->

# Inspire-Magpie

A wrapper around [magpie](https://github.com/inspirehep/magpie) for Inspire that provides trained models and functions to learn from the High Energy Physics corpus.

# Installation

```
$ git clone https://github.com/inspirehep/inspire-magpie.git
$ cd inspire-magpie
$ pip install .
```

# Dependencies
 - [Flask](http://flask.pocoo.org/)
 - [magpie](https://github.com/inspirehep/magpie) (and all that comes with it)

# Usage
There exists a UI and REST API based on [Flask](http://flask.pocoo.org/) that you can run with:

```shell
$ python wsgi.py
```

Access the UI on http://localhost:5051 and the REST interface under http://localhost:5051/api.

## REST Example

```shell
$ curl -i -X POST -H 'Content-Type: application/json' -d '{"corpus": "keywords", "positive": ["lhc"]}' http://localhost:5051/api/word2vec
```

For the training, you can use two functions that the [API](https://github.com/inspirehep/inspire-magpie/blob/master/inspire_magpie/api.py) provides: `train()` and `batch_train()`. The latter performs out-of-core training, but both of them take the same parameters:
```
$ from inspire_magpie.api import batch_train
$ batch_train('/path/to/the/training/set', test_dir='if/you/have/a/test/set', nn='cnn', nb_epochs=5, batch_size=64, persist=True, no_of_labels=10000, verbose=1)
```
 - `test_dir` - is the path to the test set (optional)
 - `nn` - defines the NN model to use for training. Currently supported: `cnn` and `rnn`
 - `nb_epochs` - how many times should we feed the training set to the NN
 - `batch_size` - size of the batch with which the training occurs
 - `persist` - whether to save to disk the final model after training (in the log directory)
 - `no_of_labels` - number of labels to train the model on. It defines whether we want to train keyword extraction (10k labels), experiment prediction (500 labels) or category assignment (14 labels).
 - `verbose` - the same values as in Keras. 1 is the most verbose with a progress bar

Other configuration variables might be found in the [config file](https://github.com/inspirehep/inspire-magpie/blob/master/inspire_magpie/config.py).
