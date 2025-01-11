import os
import asyncio
from storage_bridge.typeclass.asyncstorage import AsyncStorage

class AsyncLocalStorage(AsyncStorage):
    def __init__(self, base_path: str = "./storage"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    async def async_upload(self, source_path: str, destination_path: str) -> None:
        dest = os.path.join(self.base_path, destination_path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        await asyncio.to_thread(os.rename, source_path, dest)
        print(f"Uploaded to local storage: {dest}")

    async def async_download(self, source_path: str, destination_path: str) -> str:
        src = os.path.join(self.base_path, source_path)
        await asyncio.to_thread(os.rename, src, destination_path)
        print(f"Downloaded from local storage: {src}")
        return destination_path

    async def async_list_files(self) -> list:
        return await asyncio.to_thread(os.listdir, self.base_path)

