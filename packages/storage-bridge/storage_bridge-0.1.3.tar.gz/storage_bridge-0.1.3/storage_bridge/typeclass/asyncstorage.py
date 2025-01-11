from abc import ABC, abstractmethod

class AsyncStorage(ABC):
    @abstractmethod
    async def async_list_files(self):
        # Implementation to list files from storage
        pass

    @abstractmethod
    async def async_download(self, source, destination):
        # Implementation to download a file asynchronously
        pass

