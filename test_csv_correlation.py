#!/usr/bin/env python
"""
Module for testing correlation between two csv files. The implementation tests
the difference in x_px, y_px, and angle parameters for the same video file.

Input:
    <path_to_ctrax_csv> <path_to_graz_csv>

Example:
    python test_csv_correlation.py ~/ctrax.csv ~/Downloads/Ger09-069.csv
"""
import os
from argparse import ArgumentParser

from core.csv_loader import CSVLoader
from core.graz_csv_loader import GrazCsvLoader
from core.parameters_correlation import ParametersCorrelation


def main(ctrax_cvs, graz_cvs, save_dir):

    # make a directory to save files if it doesn't exist
    if save_dir:
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

    # load parameters from csv files
    graz_params = GrazCsvLoader.load_from_csv(graz_cvs)
    bee = CSVLoader.load_from_csv(ctrax_cvs, 1)

    best_ofst_sol = ParametersCorrelation.run(graz_params, bee['bee_0'], save_dir)


if __name__ == '__main__':
    parser = ArgumentParser(prog=__file__[:-3], description=__doc__)

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s v0.5'
    )

    parser.add_argument('ctrax_res', help='file with results of ctrax tracking')
    parser.add_argument('graz_res', help='file with parameters from Graz')
    parser.add_argument('-s', '--save', action="store", dest='out', default=False)

    args = parser.parse_args()

    main(args.ctrax_res, args.graz_res, args.out)

