class DatabaseInterface:
    async def connect(self) -> None:
        raise NotImplementedError()

    async def disconnect(self) -> None:
        raise NotImplementedError()

    async def acquire_pool(self):
        raise NotImplementedError()

    def connection_pool(self):
        raise NotImplementedError()
