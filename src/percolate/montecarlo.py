import argparse
import matplotlib.pyplot as plt
import numpy as np
import random

from .grid import PercolationGrid

MAX_GRIDS_RENDERED = 16

class MonteCarloRunner(object):
    @staticmethod
    def run(num_runs: int, params: dict, seed: int, draw:bool = True):
        random.seed(seed)
        if draw:
            nrows = int(np.minimum(np.ceil(np.sqrt(num_runs)), np.sqrt(MAX_GRIDS_RENDERED)))
            ncols = int(np.minimum(np.ceil(num_runs / nrows), np.sqrt(MAX_GRIDS_RENDERED)))
            fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12,8), gridspec_kw={'hspace':0.5})

        result = []
        for i in range(num_runs):
            grid = PercolationGrid(**params)
            if draw and i < MAX_GRIDS_RENDERED:
                grid.draw_grid(axes[i // ncols][i % ncols])
            result.append(grid.percolates)
    
        if draw:
            if (nrows * ncols) < MAX_GRIDS_RENDERED:
                for i in range(num_runs, (nrows * ncols)):
                    fig.delaxes(axes.flatten()[i])
            plt.show()

        return sum(result) / num_runs

    @staticmethod
    def plot_runs(var: str, num_runs:int, params: dict, seed: int, bounds: list):
        """Plot the percolation percentage against a param with a specified bound"""
        xs = np.linspace(float(bounds[0]), float(bounds[1]), num=100)
        ys = []

        for x in xs:
            y = MonteCarloRunner.run(
                    num_runs=num_runs,
                    seed=seed,
                    draw=False,
                    params = {
                        **params,
                        var : x
                    }
                )
            ys.append(y)

        _, ax = plt.subplots()
        ax.scatter(xs, ys)

        plt.show()

def parse_args():
    parser = argparse.ArgumentParser(description="Run a percolation monte carlo")
    parser.add_argument("-n", "--num-runs", type=int, default=10)
    parser.add_argument("-y", "--height", type=int)
    parser.add_argument("-x", "--length", type=int)
    parser.add_argument("-s", "--seed", type=int)
    parser.add_argument("-d", "--draw", action="store_true")
    parser.add_argument("-v", "--vacancy-percentage", type=float)
    parser.add_argument("--plot-runs", action="store_true")
    parser.add_argument("--variable", type=str)
    parser.add_argument("--bounds", type=str)

    return parser.parse_args()
    
def main():
    args = parse_args()
    
    params = {
        "length": args.length,
        "height": args.height,
        "vacancy_percentage": args.vacancy_percentage,
    }
    if args.plot_runs:
        MonteCarloRunner.plot_runs(
            var=args.variable,
            num_runs=args.num_runs,
            params=params,
            seed=args.seed,
            bounds=args.bounds.split(","),
        )
        return

    MonteCarloRunner.run(
        num_runs=args.num_runs,
        seed=args.seed,
        draw=args.draw,
        params=params,
    )
