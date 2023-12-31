from tfn.tools.jobs import CrossValidate


class TestCrossValidation:
    def test_cartesian_ts_cross_validated(self, run_config, builder_config):
        loader_config = {
            "loader_type": "ts_loader",
            "splitting": 5,
            "load_kwargs": {"output_distance_matrix": True},
        }
        job = CrossValidate(
            {
                "name": "test",
                "run_config": dict(**run_config, metrics=["cumulative_loss"]),
                "loader_config": loader_config,
                "builder_config": dict(
                    **builder_config,
                    builder_type="cartesian_builder",
                    prediction_type="vectors",
                    output_type="distance_matrix"
                ),
            }
        )
        job.run()
