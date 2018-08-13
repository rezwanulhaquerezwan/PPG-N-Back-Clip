# -*- coding: utf-8 -*-

import os
import json
import pickle
import csv
from io import open


def make_dirs_for_file(pathname):
    try:
        os.makedirs(os.path.dirname(pathname))
    except:
        pass


def exist(pathname, overwrite=False, display_info=True):
    def __path_type(pathname):
        if os.path.isfile(pathname):
            return 'File'
        if os.path.isdir(pathname):
            return 'Directory'
        if os.path.islink(pathname):
            return 'Symbolic Link'
        if os.path.ismount(pathname):
            return 'Mount Point'
        return 'Path'
    if os.path.exists(pathname):
        if overwrite:
            if display_info:
                print('%s: %s exists. Overwrite.' % (__path_type(pathname), pathname))
            os.remove(pathname)
            return False
        else:
            if display_info:
                print('%s: %s exists.' % (__path_type(pathname), pathname))
            return True
    else:
        if display_info:
            print('%s: %s does not exist.' % (__path_type(pathname), pathname))
        return False


def load_text(pathname, display_info=True):
    if exist(pathname=pathname, display_info=display_info):
        with open(pathname, 'rt', newline='') as f:
            return [line.strip() for line in f.readlines()]


def load_json(pathname, display_info=True):
    if exist(pathname=pathname, display_info=display_info):
        with open(pathname, 'rt', newline='') as f:
            return json.load(f)


def dump_json(data, pathname, overwrite=False, display_info=True):
    make_dirs_for_file(pathname)
    if not exist(pathname=pathname, overwrite=overwrite, display_info=display_info):
        if display_info:
            print('Write to file: %s' % pathname)
        with open(pathname, 'wt', newline='') as f:
            json.dump(data, f)


def load_model(pathname, display_info=True):
    if exist(pathname=pathname, display_info=display_info):
        with open(pathname, 'rb') as f:
            return pickle.load(f)


def dump_model(model, pathname, overwrite=False, display_info=True):
    make_dirs_for_file(pathname)
    if not exist(pathname=pathname, overwrite=overwrite, display_info=display_info):
        if display_info:
            print('Write to file: %s' % pathname)
        with open(pathname, 'wb') as f:
            pickle.dump(model, f)


def export_csv(data, fieldnames, pathname, overwrite=False, display_info=True):
    make_dirs_for_file(pathname)
    if not exist(pathname=pathname, overwrite=overwrite, display_info=display_info):
        if display_info:
            print('Write to file: %s' % pathname)
        with open(pathname, 'wt', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            for row in data:
                writer.writerow(row)


def parse_iso_time_string(timestamp):
    import dateutil.parser
    from dateutil import tz
    return dateutil.parser.parse(timestamp).astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)


def get_change_ratio(data, baseline):
    def __get_change_ratio(value, baseline):
        return (value - baseline) / baseline
    if isinstance(baseline, list):
        import numpy as np
        baseline = np.mean(baseline, axis=0)
        return [__get_change_ratio(value=value, baseline=baseline).tolist() for value in data]
    return __get_change_ratio(value=data, baseline=baseline)


def set_matplotlib_backend(backend=None):
    import matplotlib
    if matplotlib.get_backend() == 'MacOSX':
        matplotlib.use('TkAgg')
    if backend:
        matplotlib.use(backend)


def plot(args, backend=None):
    set_matplotlib_backend(backend=backend)
    import matplotlib.pyplot as plt
    plt.plot(*args)
    plt.show()


def semilogy(args, backend=None):
    set_matplotlib_backend(backend=backend)
    import matplotlib.pyplot as plt
    plt.semilogy(*args)
    plt.show()