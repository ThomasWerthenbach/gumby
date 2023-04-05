#!/usr/bin/env python3
import json
import logging
import os
import sys

import pandas as pd

from gumby.statsparser import StatisticsParser


class AccuracyStatisticsParser(StatisticsParser):
    """
    Simply read all the id.txt files created by instances and sum up the numbers inside them.
    """

    def aggregate_peer_accuracies(self):

        filename = os.path.join(os.path.dirname(__file__), sys.argv[2])
        with open(filename) as f:
            settings = json.loads("".join([x.strip() for x in f.readlines()]))

        total_accuracies = list()

        for i in range(settings['peers_per_host']):
            for _, filename, _ in self.yield_files(f'accuracy_{i}.csv'):
                total_accuracies.append(list(pd.read_csv(filename)[f'accuracy_{i}']))

        average = list()
        for i in range(min(list(map(lambda x: len(x), total_accuracies)))):
            s = 0
            for j in range(len(total_accuracies)):
                s += total_accuracies[j][i]
            average.append(s / len(total_accuracies))

        with open("accuracies.csv", "w") as sum_id_file:
            for avg in average:
                sum_id_file.write(f"{avg}\n")

    def aggregate_peer_attack_rates(self):
        filename = os.path.join(os.path.dirname(__file__), sys.argv[2])
        with open(filename) as f:
            settings = json.loads("".join([x.strip() for x in f.readlines()]))

        total_attack_rates = list()

        for i in range(settings['peers_per_host']):
            for _, filename, _ in self.yield_files(f'attack_rate_{i}.csv'):
                total_attack_rates.append(list(pd.read_csv(filename)[f'attack_rate_{i}']))

        average = list()
        for i in range(min(list(map(lambda x: len(x), total_attack_rates)))):
            s = 0
            for j in range(len(total_attack_rates)):
                s += total_attack_rates[j][i]
            average.append(s / len(total_attack_rates))

        with open("attack_rate.csv", "w") as sum_id_file:
            for avg in average:
                sum_id_file.write(f"{avg}\n")

    def aggregate_peer_round_times(self):
        filename = os.path.join(os.path.dirname(__file__), sys.argv[2])
        with open(filename) as f:
            settings = json.loads("".join([x.strip() for x in f.readlines()]))

        total_round_times = list()

        for i in range(settings['peers_per_host']):
            for _, filename, _ in self.yield_files(f'attack_rate_{i}.csv'):
                total_round_times.append(list(pd.read_csv(filename)['time']))

        average = list()
        for i in range(min(list(map(lambda x: len(x), total_round_times)))):
            s = 0
            for j in range(len(total_round_times)):
                s += total_round_times[j][i]
            average.append(s / len(total_round_times))

        if len(average) > 0:
            first = average[0]
            for i in range(len(average)):
                average[i] -= first

        with open("round_times.csv", "w") as sum_id_file:
            for avg in average:
                sum_id_file.write(f"{avg}\n")


    def run(self):
        self.aggregate_peer_accuracies()
        self.aggregate_peer_attack_rates()
        self.aggregate_peer_round_times()


# cd to the output directory
os.chdir(os.environ['OUTPUT_DIR'])

parser = AccuracyStatisticsParser(sys.argv[1])
parser.run()
