# Day 20 of Advent of Code 2023
from __future__ import annotations

import math
import timeit
from aoc.helpers import *


class Module:
    def __init__(self, name: str):
        self.name: str = name
        self.sources: list[Module] = []
        self.destinations: list[Module] = []
        self.low_pulse_count: int = 0
        self.high_pulse_count: int = 0
        self.low_pulse_received: bool = False
        pass

    def add_sources(self, sources: list[Module]):
        self.sources.extend(sources)

    def add_destinations(self, destinations: list[Module]):
        self.destinations.extend(destinations)

    def increase_pulse_count(self, pulse) -> None:
        if pulse:
            self.high_pulse_count += len(self.destinations)
        else:
            self.low_pulse_count += len(self.destinations)

    def handle(self, pulse: bool, sender: Module | None) -> callable(None):
        if not pulse:
            self.low_pulse_received = True
        self.increase_pulse_count(False)
        return lambda: (dest.handle(False, self) for dest in self.destinations)


class FlipFlop(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.state: bool = False

    def handle(self, pulse: bool, sender: Module | None) -> callable(None):
        if not pulse:
            self.state = not self.state
            self.increase_pulse_count(self.state)
            return lambda: (dest.handle(self.state, self) for dest in self.destinations)
        return lambda: ()


class Conjunction(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.__source_vals: dict[Module, bool] = dict()

    def add_sources(self, sources: list[Module]):
        super().add_sources(sources)
        self.__source_vals.update({source: False for source in sources})

    def handle(self, pulse: bool, sender: Module | None) -> callable(None):
        self.__source_vals[sender] = pulse
        send_pulse = not all(self.__source_vals.values())
        self.increase_pulse_count(send_pulse)
        return lambda: (dest.handle(send_pulse, self) for dest in self.destinations)


def generate_modules(inputs: list[str]) -> (Module, dict[str, Module]):
    modules: dict[str, Module] = dict()
    dest_to_set: dict[Module, list[str]] = dict()
    sources_to_set: dict[str, list[Module]] = dict()
    broadcaster = []

    for module in inputs:
        source, destinations = module.split(' -> ')
        destinations = destinations.split(', ')
        module_type = source[0]

        if module_type == '%':
            new_module = FlipFlop(source[1:])
        elif module_type == '&':
            new_module = Conjunction(source[1:])
        else:
            new_module = Module(source)
            broadcaster.append(new_module)

        dest_to_set[new_module] = destinations
        for dest in destinations:
            if dest not in sources_to_set:
                sources_to_set[dest] = []
            sources_to_set[dest].append(new_module)

        modules[new_module.name] = new_module

    for module, destinations in dest_to_set.items():
        for dest in destinations:
            if dest not in modules:
                modules[dest] = Module(dest)
            module.add_destinations([modules[dest]])
    for name, sources in sources_to_set.items():
        modules[name].add_sources(sources)

    return broadcaster[0], modules


def main():
    inputs = get_input("\n", example=False)

    broadcaster, modules = generate_modules(inputs)

    runs = 1000
    for i in range(runs):
        queue = [broadcaster.handle(False, None)]
        while len(queue) > 0:
            action = queue.pop(0)
            queue.extend(action())

    total_low_pulses = sum([module.low_pulse_count for module in modules.values()])
    total_low_pulses += runs
    total_high_pulses = sum([module.high_pulse_count for module in modules.values()])
    print(f"{total_low_pulses=}, {total_high_pulses=}")
    print(f"Part 1: {total_low_pulses * total_high_pulses}")

    broadcaster, modules = generate_modules(inputs)

    loop_nums: dict[Module, int] = dict()

    runs = 0
    while not modules['rx'].low_pulse_received:
        runs += 1
        queue = [broadcaster.handle(False, None)]
        while len(queue) > 0:
            action = queue.pop(0)
            queue.extend(action())
        for source in modules['qb'].sources:
            if source not in loop_nums and source.high_pulse_count > 0:
                print(f"{source.name=}, {source.high_pulse_count=}, {runs=}")
                loop_nums[source] = runs
        if all([source in loop_nums for source in modules['qb'].sources]):
            break
        if runs % 10000 == 0:
            print(f"{runs=}, qb={modules['qb'].low_pulse_count}, {loop_nums=}", end="\r")

    print(f"Part 2: {math.lcm(*loop_nums.values())}")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print(f"Time taken: {timeit.default_timer()-start}s")
