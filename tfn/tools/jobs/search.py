import numpy as np
from sklearn.model_selection import ParameterGrid

from . import KerasJob


class GridSearch(KerasJob):
    def __init__(
        self, job: KerasJob, grid: dict, total_models: int = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.job = job
        self.grid = ParameterGrid(grid)
        self.total_models = total_models or np.inf

    def _main(self, run, fitable=None, dataloader_config=None, fitable_config=None):
        for i, config in enumerate(self.grid):
            if i >= self.total_models:  # Stop when hitting max models
                print(
                    f"## Max model count of {self.total_models} exceeded, ending search ##"
                )
                break
            print(f"### Performing Grid searh on model {i} ###")
            print(f"Config set (not showing defaults): {config}")
            [
                config.setdefault(k, v)
                for k, v in self.job.exp_config["builder_config"].items()
            ]
            self.job._new_model_path(i)
            try:
                self.job._main(run, fitable_config=config)
                print(f"# Completed search on model {i} #\n")
            except Exception as e:
                print(
                    f"Encountered exception in search, skipping configuration...\n Error "
                    f"message: {e}"
                )
                pass
