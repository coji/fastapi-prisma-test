from fastapi import FastAPI
from prisma import Prisma

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello, World"}


# add a new message
@app.post("/message")
async def add_message(message: str):
    prisma = Prisma()
    await prisma.connect()
    result = await prisma.message.create(data={"text": message})
    await prisma.disconnect()
    return result


@app.get("/message")
async def get_messages(take: int = 10, offset: int = 0):
    print(take, offset)
    prisma = Prisma()
    await prisma.connect()
    message_count = await prisma.message.count()
    messages = await prisma.message.find_many(take, offset, order={"createdAt": "desc"})
    await prisma.disconnect()
    return {"message_count": message_count, "messages": messages}


@app.get("/message/{id}")
async def get_message(id: str):
    prisma = Prisma()
    await prisma.connect()
    result = await prisma.message.find_unique(where={"id": id})
    await prisma.disconnect()
    return result
