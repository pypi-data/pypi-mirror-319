from typing import List

from efootprint.abstract_modeling_classes.explainable_objects import EmptyExplainableObject
from efootprint.abstract_modeling_classes.modeling_object import ModelingObject
from efootprint.abstract_modeling_classes.source_objects import SourceValue
from efootprint.constants.units import u


class Network(ModelingObject):
    def __init__(self, name: str, bandwidth_energy_intensity: SourceValue):
        super().__init__(name)
        self.energy_footprint = EmptyExplainableObject()
        if not bandwidth_energy_intensity.value.check("[energy]/[]"):
            raise ValueError(
                "Value of variable 'bandwidth_energy_intensity' does not have the appropriate "
                "'energy/data transfer' dimensionality")
        self.bandwidth_energy_intensity = bandwidth_energy_intensity.set_label(
            f"bandwith energy intensity of {self.name}")

    @property
    def calculated_attributes(self):
        return ["energy_footprint"]

    @property
    def modeling_objects_whose_attributes_depend_directly_on_me(self) -> List:
        return []

    @property
    def usage_patterns(self):
        return self.modeling_obj_containers

    @property
    def systems(self) -> List:
        return list(set(sum([up.systems for up in self.usage_patterns], start=[])))

    @property
    def jobs(self):
        return list(set(sum([up.jobs for up in self.usage_patterns], start=[])))

    def update_energy_footprint(self):
        hourly_data_transferred_per_up = {up: EmptyExplainableObject() for up in self.usage_patterns}
        for job in self.jobs:
            job_ups_in_network_ups = [up for up in job.usage_patterns if up in self.usage_patterns]
            for up in job_ups_in_network_ups:
                hourly_data_transferred_per_up[up] += job.hourly_data_upload_per_usage_pattern[up]
                hourly_data_transferred_per_up[up] += job.hourly_data_download_per_usage_pattern[up]

        energy_footprint = EmptyExplainableObject()
        for up in self.usage_patterns:
            up_network_consumption = (
                        self.bandwidth_energy_intensity * hourly_data_transferred_per_up[up]).to(u.kWh).set_label(
                f"{up.name} network energy consumption")

            energy_footprint += up_network_consumption * up.country.average_carbon_intensity

        self.energy_footprint = energy_footprint.to(u.kg).set_label(f"Hourly {self.name} energy footprint")
