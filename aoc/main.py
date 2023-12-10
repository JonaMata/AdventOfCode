#!/usr/bin/python3
# Advent of code day generator + input downloader
# Heavily inspired by https://github.com/Jessseee/AdventOfCode

import os

import click
from click import echo, style, secho
import requests
from datetime import datetime
from dotenv import dotenv_values
from importlib.resources import as_file, files

logo = (
style(("          .---_\n"
"         / / /\|\n"
"       / / | \ "), fg='red')+style("*\n", fg='yellow')+
style("      /  /  \ \\         ", fg='red')+style("Advent\n", fg='green')+
style("     / /  / \  \        ", fg='red')+style("of Code\n", fg='green')+
style(("   ./~~~~~~~~~~~\.\n"
"  ( .\",^. -\". '.~ )     "), fg='white')+style("Tool by\n", fg='green')+
style("   '~~~~~~~~~~~~~'      ", fg='white')+style("Jonathan Matarazzi\n", fg='green'))


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
        secho("Day already exists", fg='red')
        return
    else:
        os.makedirs(day_dir, exist_ok=True)

        input_file = f"{day_dir}/input.txt"
        example_input_file = f"{day_dir}/example.txt"
        if os.path.exists(input_file):
            secho(f"Input file already at {input_file}", fg='red')
        else:
            download_input(day_dir, year, day, session_id)

        puzzle_file = f"{day_dir}/day_{day:02d}.py"
        if os.path.exists(puzzle_file):
            secho(f"Solution file already at {puzzle_file}", fg='red')
        else:
            template_file = files("aoc").joinpath("day_template.py")
            with as_file(template_file) as file:
                data = file.open('r').read().replace("<YEAR>", str(year)).replace("<DAY>", str(day))
            with open(puzzle_file, "w") as file:
                file.write(data)
        os.system(f"pycharm {input_file}")
        os.system(f"pycharm {example_input_file}")
        os.system(f"pycharm {puzzle_file}")
        secho(f"Let's get started on day {day} of AdventofCode {year}!", fg='green')


@click.group()
def cli():
    click.clear()
    secho(logo)


@cli.command()
@click.option("--date", type=click.DateTime(formats=["%Y-%d", "%Y%d"]), default=datetime.today())
def init(date: datetime):
    session_id = dotenv_values()['SESSION_ID']
    if date is not None:
        if int(date.year) < 2015:
            secho("There was no AdventOfCode before 2015 :(", fg='red')
        elif not 1 <= date.day <= 25:
            secho("Advent of code runs from 1 Dec until 25 Dec.", fg='red')
        else:
            init_day(date.year, date.day, session_id)

    else:
        # Get current time in UTC
        init_time = datetime.utcnow()
        release_time = datetime.utcnow().replace(hour=5, minute=0, second=0)
        year, day = str(init_time.year), str(init_time.day)

        # Check if it is December yet
        if init_time.month != 12:
            secho("It is not December! If you want to initiate a previous year please provide a date.", fg='red')
            exit()

        # Check if it is after midnight EST/UTC-5 (=05:00 UTC)
        if init_time.hour > 5:
            init_day(year, day, session_id)
        else:
            secho("There is no new puzzle yet! you have to wait until midnight EST/UTC-5.", fg='red')


@cli.command()
@click.argument('day', type=click.INT)
@click.option('--year', type=click.INT, default=datetime.today().year)
def run(year: int, day: int):
    day_dir = f"{year}/day_{day:02d}"
    file_path = f"day_{day:02d}.py"
    if os.path.exists(f"{day_dir}/{file_path}"):
        os.system(f"(cd {day_dir} && python {file_path})")
    else:
        secho(f"No files found for {year} day {day}", fg='red')
