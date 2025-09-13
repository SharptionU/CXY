class BaseService:

    def __init__(self, model, col):
        self.model = model
        self.col = col

    async def get_by_id(self, id):
        pass

    async def get_by_name(self):
        pass

    async def list(self, q):
        pass

    async def create(self, data):
        ...

    async def update(self, id, data):
        pass

    async def delete(self, id):
        pass
