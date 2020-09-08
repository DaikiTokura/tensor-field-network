from pathlib import Path
from tfn.tools.jobs import GridSearch, CrossValidate
from tfn.tools.jobs.config_defaults import default_grid_search


job = GridSearch(
    job=CrossValidate(
        exp_config={
            "name": f"{Path(__file__).parent}",
            "notes": "192 models total",
            "seed": 1,
            "run_config": {"epochs": 300, "test": False, "fit_verbosity": 0},
            "loader_config": {
                "loader_type": "ts_loader",
                "splitting": 5,
                "load_kwargs": {"remove_noise": True},
            },
            "builder_config": {
                "builder_type": "cartesian_builder",
                "prediction_type": "cartesians",
                "output_type": "cartesians",
            },
            "lr_config": {
                "min_delta": 0.01,
                "patience": 30,
                "cooldown": 20,
                "verbosity": 0,
            },
        }
    ),
    grid=default_grid_search,
)
job.run()
