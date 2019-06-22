import sys
import os
import json


class line_loader:
    def __init__(self, path):
        with open(path, 'r', encoding="utf-8_sig") as f:
            self.lines = json.load(f)

    def search(self, key):
        return self.lines[key]


def main():
    loader = line_loader('line.json')

    print(loader.search('sake'))


if __name__ == '__main__':
    main()
