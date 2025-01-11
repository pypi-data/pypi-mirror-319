import argparse

from . import difference


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("fileA")
    parser.add_argument("fileB")
    parser.add_argument("--colors", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--values", action=argparse.BooleanOptionalAction, default=True)
    ns = parser.parse_args(args)
    kwargs = vars(ns)
    msg = difference.files(**kwargs)
    print(msg)
