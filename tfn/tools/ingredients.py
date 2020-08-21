import os

from sacred import Ingredient

from .builders import (
    EnergyBuilder,
    ForceBuilder,
    CartesianBuilder,
    SiameseBuilder,
    ClassifierBuilder,
)
from .loaders import ISO17DataLoader, QM9DataDataLoader, TSLoader, SN2Loader
from .loggers import SacredMetricLogger
from .radials import get_radial_factory


# ===== Dataset Ingredient(s) ===== #
data_ingredient = Ingredient("data_loader")


@data_ingredient.capture
def get_data_loader(
    loader_type: str = "qm9_loader", **kwargs,
):
    """
    :param loader_type: str. Defaults to 'qm9_loader'. Used to specify which loader type is
        being used. Supported identifiers: 'qm9_loader', 'iso17_loader', iso17_force_loader',
            'ts_loader'
    :param kwargs: kwargs passed directly to Loader classes
    :return: DataLoader object specified by `loader_type`
    """
    data_dir = os.environ["DATADIR"]
    qm9_path = data_dir + "/QM9_data_original.hdf5"
    iso17_path = data_dir + "/iso17.hdf5"
    ts_path = data_dir + "/ts.hdf5"
    sn2_path = data_dir + "/sn2_reactions.npz"
    if loader_type == "qm9_loader":
        return QM9DataDataLoader(path=qm9_path, **kwargs)
    elif loader_type == "iso17_loader":
        return ISO17DataLoader(path=iso17_path, **kwargs)
    elif loader_type == "ts_loader":
        return TSLoader(path=ts_path, **kwargs)
    elif loader_type == "sn2_loader":
        return SN2Loader(path=sn2_path, **kwargs)
    else:
        raise ValueError(
            "arg `loader_type` had value: {} which is not supported. "
            "Check ingredient docs for supported strings "
            "identifiers".format(loader_type)
        )


# ===== Builder Ingredient(s) ===== #
builder_ingredient = Ingredient("model_builder")


@builder_ingredient.capture
def get_builder(
    builder_type: str = "energy_builder", **kwargs,
):
    """

    :param builder_type: str. Defaults to 'energy_builder'. Possible values include:
        'energy_builder', 'force_builder', 'ts_builder'.
    :param kwargs: kwargs passed directly to Builder classes
    :return: Builder object specified by 'builder_type'
    """
    kwargs["radial_factory"] = get_radial_factory(
        kwargs.get("radial_factory", "multi_dense"), kwargs.get("radial_kwargs", None)
    )
    if builder_type == "energy_builder":
        return EnergyBuilder(**kwargs)
    elif builder_type == "force_builder":
        return ForceBuilder(**kwargs)
    elif builder_type == "cartesian_builder":
        return CartesianBuilder(**kwargs)
    elif builder_type == "siamese_builder":
        return SiameseBuilder(**kwargs)
    elif builder_type == "classifier_builder":
        return ClassifierBuilder(**kwargs)
    else:
        raise ValueError(
            "arg `builder_type` had value: {} which is not supported. Check "
            "ingredient docs for supported string identifiers".format(builder_type)
        )


# ===== Logger Ingredient(s) ===== #
logger_ingredient = Ingredient("metric_logger")
get_logger = logger_ingredient.capture(SacredMetricLogger)
