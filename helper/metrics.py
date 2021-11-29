import numpy as np


class Accumulator(object):
    def __init__(self, **kwargs):
        self.values = kwargs
        self.counter = {k: 0 for k, v in kwargs.items()}
        for k, v in self.values.items():
            if not isinstance(v, (float, int, list)):
                raise TypeError(f"The Accumulator does not support "
                                f"`{type(v)}`. Supported types: "
                                f"[float, int, list]")

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(self.values[k], list):
                self.values[k].append(v)
            else:
                self.values[k] = self.values[k] + v
            self.counter[k] += 1

    def reset(self):
        for k in self.values.keys():
            if isinstance(self.values[k], list):
                self.values[k] = []
            else:
                self.values[k] = 0
            self.counter[k] = 0

    def sum(self, key, axis=None):
        if isinstance(key, str):
            if isinstance(self.values[key], list):
                return np.array(self.values[key]).sum(axis)
            else:
                return self.values[key]
        else:
            return [self.sum(k, axis) for k in key]

    def mean(self, key, axis=None, dic=False):
        if isinstance(key, str):
            if isinstance(self.values[key], list):
                return np.array(self.values[key]).mean(axis)
            else:
                return self.values[key] / self.counter[key]
        elif isinstance(key, (list, tuple)):
            if dic:
                return {k: self.mean(k, axis) for k in key}
            return [self.mean(k, axis) for k in key]
        else:
            TypeError(f"`key` must be a str/list/tuple, got {type(key)}")

    def std(self, key, axis=None, dic=False):
        if isinstance(key, str):
            if isinstance(self.values[key], list):
                return np.array(self.values[key]).std(axis)
            else:
                raise RuntimeError("`std` is not supported for (int, float). "
                                   "Use list instead.")
        elif isinstance(key, (list, tuple)):
            if dic:
                return {k: self.std(k, axis) for k in key}
            return [self.std(k, axis) for k in key]
        else:
            TypeError(f"`key` must be a str/list/tuple, got {type(key)}")
