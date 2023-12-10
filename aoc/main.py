#!/usr/bin/python3

# Advent of code day generator + input downloader
# Heavily inspired by https://github.com/Jessseee/AdventOfCode

import os
import click
import dotenv
import requests
from datetime import datetime
from dotenv import dotenv_values
from importlib.resources import as_file, files


def download_input(day_dir, year, day, session_id):
    with requests.get(
            f"https://adventofcode.com/{year}/day/{day}/input",
            cookies={'session': session_id}) as response:
        if response.ok:
            with open(f"{day_dir}/input.txt", "w+") as f:
                f.write(response.text.rstrip("\n"))
            with open(f"{day_dir}/example.txt", "w+") as f:
                f.write(" ")


def init_day(year, day, session_id):
    day_dir = f"{year}/day_{day:02d}"
    if os.path.exists(day_dir):
        print("Day already exists")
        return
    else:
        os.makedirs(day_dir, exist_ok=True)

        input_file = f"{day_dir}/input.txt"
        example_input_file = f"{day_dir}/example.txt"
        if os.path.exists(input_file):
            print(f"Input file already at {input_file}")
        else:
            download_input(day_dir, year, day, session_id)

        puzzle_file = f"{day_dir}/day_{day:02d}.py"
        if os.path.exists(puzzle_file):
            print(f"Solution file already at {puzzle_file}")
        else:
            template_file = files("aoc").joinpath("day_template.py")
            with as_file(template_file) as file:
                data = file.open('r').read().replace("<YEAR>", str(year)).replace("<DAY>", str(day))
            with open(puzzle_file, "w") as file:
                file.write(data)
        os.system(f"pycharm {input_file}")
        os.system(f"pycharm {example_input_file}")
        os.system(f"pycharm {puzzle_file}")
        print(f"Let's get started on day {day} of AdventofCode {year}!")


@click.group()
def cli():
    pass


@cli.command()
@click.option("--date", type=click.DateTime(formats=["%Y-%d", "%Y%d"]), default=datetime.today())
def init(date: datetime):
    session_id = dotenv_values()['SESSION_ID']
    print(session_id)
    if date is not None:
        if int(date.year) < 2015:
            print("There was no AdventOfCode before 2015 :(")
        elif not 1 <= date.day <= 25:
            print("Advent of code runs from 1 Dec until 25 Dec.")
        else:
            init_day(date.year, date.day, session_id)

    else:
        # Get current time in UTC
        init_time = datetime.utcnow()
        release_time = datetime.utcnow().replace(hour=5, minute=0, second=0)
        year, day = str(init_time.year), str(init_time.day)

        # Check if it is December yet
        if init_time.month != 12:
            print("It is not December! If you want to initiate a previous year please provide a date.")
            exit()

        # Check if it is after midnight EST/UTC-5 (=05:00 UTC)
        if init_time.hour > 5:
            init_day(year, day, session_id)
        else:
            print("There is no new puzzle yet! you have to wait until midnight EST/UTC-5.")
