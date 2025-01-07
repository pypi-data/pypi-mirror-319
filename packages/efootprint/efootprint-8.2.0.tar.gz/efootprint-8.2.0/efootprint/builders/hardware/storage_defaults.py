from efootprint.constants.sources import Sources
from efootprint.abstract_modeling_classes.source_objects import SourceValue
from efootprint.constants.units import u
from efootprint.core.hardware.storage import Storage


def default_ssd(name="Default SSD storage", **kwargs):
    output_args = {
        "carbon_footprint_fabrication": SourceValue(160 * u.kg, Sources.STORAGE_EMBODIED_CARBON_STUDY),
        "power": SourceValue(1.3 * u.W, Sources.STORAGE_EMBODIED_CARBON_STUDY),
        "lifespan": SourceValue(6 * u.years, Sources.HYPOTHESIS),
        "idle_power": SourceValue(0 * u.W, Sources.HYPOTHESIS),
        "storage_capacity": SourceValue(1 * u.TB, Sources.STORAGE_EMBODIED_CARBON_STUDY),
        "data_replication_factor": SourceValue(3 * u.dimensionless, Sources.HYPOTHESIS),
        "base_storage_need": SourceValue(0 * u.TB, Sources.HYPOTHESIS),
        "data_storage_duration": SourceValue(5 * u.year, Sources.HYPOTHESIS)
    }

    output_args.update(kwargs)

    return Storage(name, **output_args)


def default_hdd(name="Default HDD storage", **kwargs):
    output_args = {
        "carbon_footprint_fabrication": SourceValue(20 * u.kg, Sources.STORAGE_EMBODIED_CARBON_STUDY),
        "power": SourceValue(4.2 * u.W, Sources.STORAGE_EMBODIED_CARBON_STUDY),
        "lifespan": SourceValue(4 * u.years, Sources.HYPOTHESIS),
        "idle_power": SourceValue(0 * u.W, Sources.HYPOTHESIS),
        "storage_capacity": SourceValue(1 * u.TB, Sources.STORAGE_EMBODIED_CARBON_STUDY),
        "data_replication_factor": SourceValue(3 * u.dimensionless, Sources.HYPOTHESIS),
        "base_storage_need": SourceValue(0 * u.TB, Sources.HYPOTHESIS),
        "data_storage_duration": SourceValue(5 * u.year, Sources.HYPOTHESIS)
    }

    output_args.update(kwargs)

    return Storage(name, **output_args)
