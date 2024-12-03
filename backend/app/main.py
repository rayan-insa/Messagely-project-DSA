from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import Base, engine, get_db
from app.models.user import User
from app.models.message import Message
from app.models.groupchat import GroupChat
from app.models.conversation import Conversation

app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/db_test")
async def db_test():
    async with engine.begin() as conn:
        result = await conn.execute("SELECT DATABASE();")
        return {"database": result.scalar()}
    
@app.get("/add_test_data")
async def add_test_data(db: AsyncSession = Depends(get_db)):
    try:
        # Create some sample conversations
        conversation1 = Conversation(name="General Chat")
        conversation2 = Conversation(name="Private Chat with Alice")

        # Add conversations to the session and commit
        db.add_all([conversation1, conversation2])
        await db.commit()
        return {"message": "Test data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding test data: {str(e)}")

@app.get("/conversations")
async def get_conversations(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Conversation))
        conversations = result.scalars().all()  # Get all conversations as a list
        return conversations  # Return the conversations to the frontend
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching conversations")
    
@app.get("/print_conversations")
async def print_conversations(db: AsyncSession = Depends(get_db)):
    try:
        # Fetch all conversations from the database
        result = await db.execute(select(Conversation))
        conversations = result.scalars().all()

        # Print conversations to the console
        for conversation in conversations:
            print(f"Conversation ID: {conversation.id}, Name: {conversation.name}")

        return {"message": "Conversations printed in the backend console"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")