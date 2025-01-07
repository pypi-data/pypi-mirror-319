from abc import abstractmethod
from typing import List

from efootprint.abstract_modeling_classes.contextual_modeling_object_attribute import ContextualModelingObjectAttribute
from efootprint.abstract_modeling_classes.explainable_objects import ExplainableQuantity, \
    EmptyExplainableObject
from efootprint.abstract_modeling_classes.modeling_object import ModelingObject
from efootprint.core.hardware.hardware_base_classes import InfraHardware
from efootprint.abstract_modeling_classes.source_objects import SourceValue, SOURCE_VALUE_DEFAULT_NAME
from efootprint.constants.units import u
from efootprint.core.hardware.storage import Storage


class Server(InfraHardware):
    def __init__(self, name: str, carbon_footprint_fabrication: SourceValue, power: SourceValue,
                 lifespan: SourceValue, idle_power: SourceValue, ram: SourceValue, cpu_cores: SourceValue,
                 power_usage_effectiveness: SourceValue, average_carbon_intensity: SourceValue,
                 server_utilization_rate: SourceValue, base_ram_consumption: SourceValue,
                 base_cpu_consumption: SourceValue, storage: Storage):
        super().__init__(name, carbon_footprint_fabrication, power, lifespan)
        self.hour_by_hour_cpu_need = EmptyExplainableObject()
        self.hour_by_hour_ram_need = EmptyExplainableObject()
        self.available_cpu_per_instance = EmptyExplainableObject()
        self.available_ram_per_instance = EmptyExplainableObject()
        self.server_utilization_rate = EmptyExplainableObject()
        self.raw_nb_of_instances = EmptyExplainableObject()
        self.nb_of_instances = EmptyExplainableObject()
        self.idle_power = idle_power.set_label(f"Idle power of {self.name}")
        self.ram = ram.set_label(f"RAM of {self.name}")
        self.cpu_cores = cpu_cores.set_label(f"Nb cpus cores of {self.name}")
        if not power_usage_effectiveness.value.check("[]"):
            raise ValueError(
                "Value of variable 'power_usage_effectiveness' does not have appropriate [] dimensionality")
        self.power_usage_effectiveness = power_usage_effectiveness.set_label(f"PUE of {self.name}")
        if not average_carbon_intensity.value.check("[time]**2 / [length]**2"):
            raise ValueError(
                "Variable 'average_carbon_intensity' does not have mass over energy "
                "('[time]**2 / [length]**2') dimensionality"
            )
        self.average_carbon_intensity = average_carbon_intensity
        if self.average_carbon_intensity.label == SOURCE_VALUE_DEFAULT_NAME:
            self.average_carbon_intensity.set_label(f"Average carbon intensity of {self.name} electricity")
        self.server_utilization_rate = server_utilization_rate.set_label(f"{self.name} utilization rate")
        if not base_ram_consumption.value.check("[]"):
            raise ValueError("variable 'base_ram_consumption' does not have byte dimensionality")
        if not base_cpu_consumption.value.check("[cpu]"):
            raise ValueError("variable 'base_cpu_consumption' does not have core dimensionality")
        self.base_ram_consumption = base_ram_consumption.set_label(f"Base RAM consumption of {self.name}")
        self.base_cpu_consumption = base_cpu_consumption.set_label(f"Base CPU consumption of {self.name}")
        self.storage = ContextualModelingObjectAttribute(storage)

    @property
    def calculated_attributes(self):
        return ["hour_by_hour_cpu_need", "hour_by_hour_ram_need", "available_ram_per_instance",
                "available_cpu_per_instance", "raw_nb_of_instances", "nb_of_instances",
                "instances_fabrication_footprint", "instances_energy", "energy_footprint"]

    @property
    def resources_unit_dict(self):
        return {"ram": "GB", "cpu": "core"}

    @property
    def jobs(self):
        return self.modeling_obj_containers

    @property
    def modeling_objects_whose_attributes_depend_directly_on_me(self) -> List[ModelingObject]:
        return [self.storage]

    def compute_hour_by_hour_resource_need(self, resource):
        resource_unit = u(self.resources_unit_dict[resource])
        hour_by_hour_resource_needs = EmptyExplainableObject()
        for job in self.jobs:
            hour_by_hour_resource_needs += (
                job.hourly_avg_occurrences_across_usage_patterns * getattr(job, f"{resource}_needed"))

        return hour_by_hour_resource_needs.to(resource_unit).set_label(f"{self.name} hour by hour {resource} need")

    def update_hour_by_hour_cpu_need(self):
        self.hour_by_hour_cpu_need = self.compute_hour_by_hour_resource_need("cpu")

    def update_hour_by_hour_ram_need(self):
        self.hour_by_hour_ram_need = self.compute_hour_by_hour_resource_need("ram")

    def update_available_ram_per_instance(self):
        available_ram_per_instance = self.ram * self.server_utilization_rate
        available_ram_per_instance -= self.base_ram_consumption
        if available_ram_per_instance.value < 0 * u.B:
            raise ValueError(
                f"server has available capacity of {(self.ram * self.server_utilization_rate).value} "
                f" but is asked {self.base_ram_consumption.value}")

        self.available_ram_per_instance = available_ram_per_instance.set_label(
            f"Available RAM per {self.name} instance")

    def update_available_cpu_per_instance(self):
        available_cpu_per_instance = self.cpu_cores * self.server_utilization_rate
        available_cpu_per_instance -= self.base_cpu_consumption
        if available_cpu_per_instance.value < 0:
            raise ValueError(
                f"server has available capacity of {(self.cpu_cores * self.server_utilization_rate).value} "
                f" but is asked {self.base_cpu_consumption.value}")

        self.available_cpu_per_instance = available_cpu_per_instance.set_label(
            f"Available CPU per {self.name} instance")

    def update_raw_nb_of_instances(self):
        nb_of_servers_based_on_ram_alone = (
                self.hour_by_hour_ram_need / self.available_ram_per_instance).to(u.dimensionless).set_label(
            f"Raw nb of {self.name} instances based on RAM alone")
        nb_of_servers_based_on_cpu_alone = (
                self.hour_by_hour_cpu_need / self.available_cpu_per_instance).to(u.dimensionless).set_label(
            f"Raw nb of {self.name} instances based on CPU alone")

        nb_of_servers_raw = nb_of_servers_based_on_ram_alone.np_compared_with(nb_of_servers_based_on_cpu_alone, "max")

        hour_by_hour_raw_nb_of_instances = nb_of_servers_raw.set_label(
            f"Hourly raw number of {self.name} instances")

        self.raw_nb_of_instances = hour_by_hour_raw_nb_of_instances

    def update_instances_energy(self):
        energy_spent_by_one_idle_instance_over_one_hour = (
                self.idle_power * self.power_usage_effectiveness * ExplainableQuantity(1 * u.hour, "one hour"))
        extra_energy_spent_by_one_fully_active_instance_over_one_hour = (
                (self.power - self.idle_power) * self.power_usage_effectiveness
                * ExplainableQuantity(1 * u.hour, "one hour"))

        server_power = (
                energy_spent_by_one_idle_instance_over_one_hour * self.nb_of_instances
                + extra_energy_spent_by_one_fully_active_instance_over_one_hour * self.raw_nb_of_instances)

        self.instances_energy = server_power.to(u.kWh).set_label(
            f"Hourly energy consumed by {self.name} instances")

    @abstractmethod
    def update_nb_of_instances(self):
        pass
