from fastapi import FastAPI
from prisma import Prisma

app = FastAPI()
prisma = Prisma()


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.get("/")
def index():
    return {"message": "Hello, World"}


# add a new message
@app.post("/message")
async def add_message(message: str):
    return await prisma.message.create(data={"text": message})


@app.get("/message")
async def get_messages(take: int = 10, offset: int = 0):
    print(take, offset)
    message_count = await prisma.message.count()
    messages = await prisma.message.find_many(take, offset, order={"createdAt": "desc"})
    return {"message_count": message_count, "messages": messages}


@app.get("/message/{id}")
async def get_message(id: str):
    return await prisma.message.find_unique(where={"id": id})
