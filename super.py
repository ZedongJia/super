import argparse

from bin.runner import Builder

parser = argparse.ArgumentParser()

parser.add_argument('choice')

args = parser.parse_args()

if args.choice == 'build':
    Builder.build()
