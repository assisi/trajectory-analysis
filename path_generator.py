#!/usr/bin/env python
"""
Module for displaying/saving all bee paths found in the given csv file.

Input:
    <path_to_csv_file> [<output_directory>]

Example:
    python ~/ASSISIbf/example_file.csv
    python ~/ASSISIbf/example_file.csv ./tmp/output_dir
"""
from argparse import ArgumentParser

from core.csv_loader import CSVLoader
from core.output import Output


def main(csv_file, out_folder):
    bees = CSVLoader.load_from_csv(csv_file)

    Output.dump_bees_to_folder(bees, out_folder)
    # Output.show_bee_path(bees['bee_2'])


if __name__ == '__main__':
    parser = ArgumentParser(prog=__file__[:-3], description=__doc__)

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s v0.5'
    )

    parser.add_argument('ctrax_res', help='file with results of ctrax tracking')
    parser.add_argument('dir', nargs='?', help='output folder',
                        default='attempts/tmp')

    args = parser.parse_args()
    main(args.ctrax_res, args.dir)
