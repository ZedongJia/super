from bin.stream import Stream, FileHash

class Dev:
    @staticmethod
    def dev():
        pass
    

class Builder:
    @staticmethod
    def build(randomSlots: dict[str, str] = {}, paramsSlots: dict[str, str] = {}):
        fileHash = FileHash(Stream.scanFiles()['.html'])
        Stream.loadFiles(fileHash.FILES, randomSlots, paramsSlots)
        Stream.writeFiles()
