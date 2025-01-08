from typing import List

import pandas as pd

from efootprint.abstract_modeling_classes.source_objects import SourceValue, Source
from efootprint.core.hardware.servers.server_base_class import Server
from efootprint.core.hardware.storage import Storage
from efootprint.core.usage.job import Job, JobTypes
from efootprint.builders.usage.job_ecobenchmark.ecobenchmark_data_analysis import ECOBENCHMARK_DATA, \
    ECOBENCHMARK_RESULTS_LINK, default_request_duration
from efootprint.constants.units import u

ECOBENCHMARK_DF = pd.read_csv(ECOBENCHMARK_DATA)
ecobenchmark_source = Source(
    "e-footprint analysis of Boavizta’s Ecobenchmark data", ECOBENCHMARK_RESULTS_LINK)


def ecobenchmark_job(
        name: str, server: Server, data_upload: SourceValue, data_download: SourceValue,
        data_stored: SourceValue, technology: str, implementation_details: str = "default", job_type=JobTypes.UNDEFINED,
        description: str = ""):
    filter_df = ECOBENCHMARK_DF[
        (ECOBENCHMARK_DF['service'] == technology) & (ECOBENCHMARK_DF['use_case'] == implementation_details)]

    if len(filter_df) == 0:
        raise ValueError(f"The input technology ({technology}) doesn’t belong to the list of supported technologies: "
                         f"{get_ecobenchmark_technologies()}")
    else:
        tech_row = filter_df.iloc[0]

    cpu_needed = SourceValue(tech_row['avg_cpu_core_per_request'] * u.core, ecobenchmark_source)
    ram_needed = SourceValue(tech_row['avg_ram_per_request_in_MB'] * u.MB, ecobenchmark_source)

    return Job(
        name, server, data_upload, data_download, data_stored, request_duration=default_request_duration(),
        cpu_needed=cpu_needed, ram_needed=ram_needed, job_type=job_type, description=description)


def get_ecobenchmark_technologies() -> List[str]:
    return list(ECOBENCHMARK_DF["service"].unique())


if __name__ == "__main__":
    print(get_ecobenchmark_technologies())
