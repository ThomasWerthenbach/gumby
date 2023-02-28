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
            for j in range(100):
                s += total_accuracies[j][i]
            average.append(s / 100)

        with open("accuracies.csv", "w") as sum_id_file:
            for avg in average:
                sum_id_file.write(f"{avg}\n")

    def run(self):
        self.aggregate_peer_accuracies()


# cd to the output directory
os.chdir(os.environ['OUTPUT_DIR'])

parser = AccuracyStatisticsParser(sys.argv[1])
parser.run()
