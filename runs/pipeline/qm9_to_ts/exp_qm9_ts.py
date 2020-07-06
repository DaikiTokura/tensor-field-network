from tfn.tools.jobs import Pipeline


job = Pipeline({
    'run_config': {
        'name': 'tl0 - QM9 Energy to ISO17 Energy/Force predictor',
        'notes': 'Not freezing layers, defaults for both models'
    },
    'pipeline_config': {
        'configs': [
            {  # QM9 config
                'builder_config': {
                    'builder_type': 'energy_builder'
                },
                'loader_config': {
                    'loader_type': 'qm9_loader'
                }
            },
            {  # TS config
                'builder_config': {
                    'builder_type': 'ts_builder'
                },
                'loader_config': {
                    'loader_type': 'ts_loader',
                    'splitting': '90:10',
                    'load_kwargs': {
                        'output_distance_matrix': True, 'use_complexes': False
                    }
                }
            }
        ]
    }
})
job.run()
