import argparse

from bin.runner import Builder



class Super:
    def __init__(self) -> None:
        self.randomSlots = {}
        self.paramsSlots = {}
    
    def super(self) -> None:
        parser = argparse.ArgumentParser()

        parser.add_argument('--choice', type=str,  default='debug')

        args = parser.parse_args()

        if args.choice == 'debug':
            Builder.build(self.randomSlots, self.paramsSlots)

        elif args.choice == 'build':
            Builder.build(self.randomSlots, self.paramsSlots)
    
    def registRandomSlots(self, registDict: dict[str, str]):
        for _k, _v in registDict.items():
            self.randomSlots[_k] = _v
    
    def registParamsSlots(self, registDict: dict[str, str]):
        for _k, _v in registDict.items():
            self.paramsSlots[_k] = _v