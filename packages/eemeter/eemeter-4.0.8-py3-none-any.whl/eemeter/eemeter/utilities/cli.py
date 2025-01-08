#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   Copyright 2014-2024 OpenEEmeter contributors

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""
import json

import click
import importlib.resources

from eemeter.eemeter.models.daily.data import DailyBaselineData
from eemeter.eemeter.models.daily.model import DailyModel
from eemeter.eemeter.utilities.io import meter_data_from_csv, temperature_data_from_csv


@click.group()
def cli():
    """Example usage


    Save output::


        Use CalTRACK methods on sample data:

        \b
            $ eemeter caltrack --sample=il-electricity-cdd-hdd-daily

        Save output:

        \b
            $ eemeter caltrack --sample=il-electricity-cdd-only-billing_monthly --output-file=/path/to/output.json

        Load custom data (see sample files for example format):

        \b
            $ eemeter caltrack --meter-file=/path/to/meter/data.csv --temperature-file=/path/to/temperature/data.csv

        Do not fit CDD models (intended for gas data):

        \b
            $ eemeter caltrack --sample=il-gas-hdd-only-billing_monthly --no-fit-cdd
    """
    pass  # pragma: no cover


def _get_data(
    sample,
    meter_file,
    temperature_file,
):
    if sample is not None:
        with importlib.resources.files("eemeter.eemeter.samples").joinpath(
            "metadata.json"
        ).open("rb") as f:
            metadata = json.loads(f.read().decode("utf-8"))
        if sample in metadata:
            click.echo("Loading sample: {}".format(sample))
            meter_file = importlib.resources.files("eemeter.eemeter.samples").joinpath(
                metadata[sample]["meter_data_filename"]
            )
            temperature_file = importlib.resources.files(
                "eemeter.eemeter.samples"
            ).joinpath(metadata[sample]["temperature_filename"])
        else:
            raise click.ClickException(
                "Sample not found. Try one of these?\n{}".format(
                    "\n".join([" - {}".format(key) for key in sorted(metadata.keys())])
                )
            )

    if meter_file is not None:
        gzipped = meter_file.name.endswith(".gz")
        meter_data = meter_data_from_csv(meter_file, gzipped=gzipped)
    else:
        raise click.ClickException("Meter data not specified.")

    if temperature_file is not None:
        gzipped = temperature_file.name.endswith(".gz")
        temperature_data = temperature_data_from_csv(
            temperature_file, gzipped=gzipped, freq="hourly"
        )
    else:
        raise click.ClickException("Temperature data not specified.")

    is_electricity_data = "elec" in sample if sample else False
    data = DailyBaselineData.from_series(
        meter_data, temperature_data, is_electricity_data=is_electricity_data
    )
    return data


@cli.command()
@click.option("--sample", default=None, type=str)
@click.option("--meter-file", default=None, type=click.File("rb"))
@click.option("--temperature-file", default=None, type=click.File("rb"))
@click.option("--output-file", default=None, type=click.File("wb"))
def caltrack(sample, meter_file, temperature_file, output_file):
    data = _get_data(
        sample,
        meter_file,
        temperature_file,
    )
    model_results = DailyModel().fit(data, ignore_disqualification=True)
    json_str = json.dumps(model_results.to_dict(), indent=2)

    if output_file is None:
        click.echo(json_str)
    else:
        output_file.write(json_str.encode("utf-8"))
        click.echo("Output written: {}".format(output_file.name))
