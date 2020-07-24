from tensorflow.keras.models import load_model

from tfn.tools.jobs import SingleModel


class TestScalarModels:
    def test_defaults(self, run_config, builder_config):
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'builder_config': builder_config
        })
        job.run()

    def test_sum_atoms(self, run_config, builder_config):
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'builder_config': dict(**builder_config, sum_atoms='cosine')
        })
        job.run()

    def test_cosine_basis(self, run_config, builder_config):
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'builder_config': dict(**builder_config, basis_type='cosine')
        })
        job.run()

    def test_single_dense_radial(self, run_config, builder_config):
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'builder_config': dict(**builder_config, **{
                'embedding_units': 32,
                'model_num_layers': (3, 3, 3),
                'si_units': 32,
                'radial_factory': 'single_dense',
                'radial_kwargs': {
                    'num_layers': 1,
                    'units': 64,
                    'activation': 'ssp',
                    'kernel_lambda': 0.01,
                    'bias_lambda': 0.01},
                'sum_atoms': True})
        })
        job.run()

    def test_multi_conv_radial(self, run_config, builder_config):
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'builder_config': dict(**builder_config, radial_factory='multi_conv')
        })
        job.run()

    def test_single_conv_radial(self, run_config, builder_config):
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'builder_config': dict(**builder_config, radial_factory='single_conv')
        })
        job.run()

    def test_default_loads_graphly(self, run_config, builder_config, model):
        run_config['run_eagerly'] = False
        builder_config['dynamic'] = False
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'builder_config': builder_config
        })
        job.run()
        model = load_model(model)
        assert True

    def test_default_loads_eagerly(self, run_config, builder_config, model):
        run_config['run_eagerly'] = True
        builder_config['dynamic'] = True
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'builder_config': builder_config
        })
        job.run()
        model = load_model(model)
        assert True


class TestDualModels:
    def test_defaults(self, run_config, builder_config):
        loader_config = {'loader_type': 'iso17_loader'}
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'loader_config': loader_config,
            'builder_config': dict(**builder_config, builder_type='force_builder')
        })
        job.run()

    def test_sn2(self, run_config, builder_config):
        loader_config = {'loader_type': 'sn2_loader'}
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'loader_config': loader_config,
            'builder_config': dict(**builder_config, builder_type='force_builder')
        })
        job.run()


class TestVectorModels:
    def test_ts_job(self, run_config, builder_config):
        loader_config = {'loader_type': 'ts_loader', 'load_kwargs': {
            'output_distance_matrix': True, 'use_complexes': False
        }}
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'loader_config': loader_config,
            'builder_config': dict(**builder_config, builder_type='ts_builder')
        })
        job.run()


class TestClassifiers:
    def test_siamese_network(self, run_config, builder_config):
        loader_config = {'loader_type': 'ts_loader', 'load_kwargs': {'output_type': 'siamese'}}
        job = SingleModel({
            'name': 'test',
            'run_config': run_config,
            'loader_config': loader_config,
            'builder_config': dict(**builder_config, builder_type='siamese_builder')
        })
        job.run()
