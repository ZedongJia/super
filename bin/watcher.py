from bin.stream import Path, File
from bin.vdom import Node


class Watcher:
    r'''
    watch the file 
    
    if it has changed, notify it
    '''
    WatcherList: list = []
    NotifyList: list = []
    
    def __init__(self, path: Path, file: File):
        r'''
        @param path Path Object
        @param file File Object
        '''
        self._path = path
        self._file = file

    def watch(self):
        r'''
        watch the file
        '''
        if self._path.isModified():
            Watcher.UpdateList.append(self)

    def notify(self):
        r'''
        notify the file
        '''
        pass
    
    @staticmethod
    def watchAll():
        r'''
        watch all files
        '''
        for watcher in Watcher.WatcherList:
            watcher.watch()
            
    @staticmethod
    def notifyAll():
        r'''
        invoke the notify method of all watchers
        '''
        for watcher in Watcher.NotifyList:
            watcher.notify()