from bin.stream import Stream, FileTree

class Dev:
    @staticmethod
    def dev():
        pass
    

class Builder:
    @staticmethod
    def build():
        tree = FileTree(Stream.scanFiles())
        Stream.writeFiles(tree.FILES)
