from tfn.tools.jobs import GridSearch
from tfn.tools.jobs.config_defaults import default_grid_search

job = GridSearch(
    total_models=100,
    exp_config={
        'name': 'TS architecture grid search',
        'notes': 'Testing all 96 models of default grid search',
        'run_config': {'epochs': 20},
        'loader_config': {'loader_type': 'ts_loader'},
        'builder_config': {'builder_type': 'ts_builder'},
        'grid_config': default_grid_search
    }
)
job.run()
