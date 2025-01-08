from dataclasses import dataclass


class ReadonlyDict:
    def __init__(self, entries):
        self.records = dict(entries)

    def __getitem__(self, key):
        value = self.records[key]
        if (value == None):
            print("{} is not present at your config file, program exit")
            exit(1)
        return value

    def __str__(self):
        return self.records.__str__()

    def __len__(self):
        return self.records.__len__()
