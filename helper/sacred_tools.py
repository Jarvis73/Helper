import shutil
from pathlib import Path

from sacred.config.custom_containers import ReadOnlyDict
from sacred.observers import FileStorageObserver


class MapConfig(ReadOnlyDict):
    """
    A wrapper for dict. This wrapper allow users to access dict value by `dot`
    operation. For example, you can access `cfg["split"]` by `cfg.split`, which
    makes the code more clear. Notice that the result object is a
    sacred.config.custom_containers.ReadOnlyDict, which is a read-only dict for
    preserving the configuration.

    Parameters
    ----------
    obj: ReadOnlyDict
        Configuration dict.
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, obj, **kwargs):
        new_dict = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, dict):
                    new_dict[k] = MapConfig(v)
                else:
                    new_dict[k] = v
        else:
            raise TypeError(f"`obj` must be a dict, got {type(obj)}")
        super(MapConfig, self).__init__(new_dict, **kwargs)


def recover_backup_names(_run):
    if _run.observers:
        for obs in _run.observers:
            if isinstance(obs, FileStorageObserver):
                for source_file, _ in _run.experiment_info['sources']:
                    Path(f'{obs.dir}/source/{source_file}').parent.mkdir(parents=True, exist_ok=True)
                    obs.save_file(source_file, f'source/{source_file}')
                shutil.rmtree(f'{obs.basedir}/_sources')
                break
