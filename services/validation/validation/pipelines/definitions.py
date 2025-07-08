"""Dagster definitions for validation pipeline."""

from dagster import Definitions, load_assets_from_modules

from . import assets
from .jobs import all_jobs, all_schedules, all_sensors
from .resources import database_resource, expectation_resource

# Load all assets from the assets module
all_assets = load_assets_from_modules([assets])

# Create the definitions object
defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
    sensors=all_sensors,
    resources={
        "database": database_resource,
        "expectations": expectation_resource,
    },
)