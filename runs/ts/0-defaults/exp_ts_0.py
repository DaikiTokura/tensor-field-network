from tfn.tools.jobs import SingleModel

job = SingleModel(exp_config={
    'name': 'DEFAULT TS MODEL ON TS DATASET',
    'notes': 'Train on only distance matrix',
    'run_config': {'epochs': 200, 'loss': 'mae', 'optimizer_kwargs': {
        'learning_rate': 0.1}},
    'builder_config': {'builder_type': 'ts_builder', 'output_type': 'both', 'num_layers': (2, 2, 2),
                       'si_units': 64},
    'loader_config': {'loader_type': 'ts_loader', 'splitting': '70:25:5', 'load_kwargs': {
        'output_distance_matrix': True, 'use_complexes': False, 'output_type': 'both'
    }}
})
job.run()
