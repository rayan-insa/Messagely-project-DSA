from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_engine
from app.database import Base, get_db
from app.models.conversation import Conversation
from app.models.user import User
from app.models.message import Message
from app.models.groupchat import GroupChat
from sqlalchemy.future import select
import logging
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("/db_test")
async def db_test():
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT DATABASE();"))
            return {"database": result.scalar()}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error connecting to the database: {str(e)}"
        )


@router.get("/reset_db")
async def reset_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(
            text(
                "DROP TABLE IF EXISTS messages, conversations, group_members, groupchats, users CASCADE"
            )
        )
        await db.execute(text("DROP TABLE IF EXISTS alembic_version"))
        await db.commit()

        # Recreate tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        return {"message": "Database reset successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error resetting the database: {str(e)}"
        )


@router.get("/add_test_data")
async def add_test_data(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(
            text(
                "DROP TABLE IF EXISTS messages, conversations, group_members, groupchats, users CASCADE"
            )
        )
        await db.execute(text("DROP TABLE IF EXISTS alembic_version"))
        await db.commit()

        # Recreate tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        # Create users
        user1 = User(username="user1", email="user1@example.com")
        user2 = User(username="user2", email="user2@example.com")
        user3 = User(username="user3", email="user3@example.com")
        user4 = User(username="user4", email="user4@example.com")
        user5 = User(username="user5", email="user5@example.com")
        user6 = User(username="user6", email="user6@example.com")
        user7 = User(username="user7", email="user7@example.com")
        user8 = User(username="user8", email="user8@example.com")
        user9 = User(username="user9", email="user9@example.com")

        db.add_all([user1, user2, user3, user4, user5, user6, user7, user8, user9])
        await db.commit()

        await db.refresh(user1)
        await db.refresh(user2)
        await db.refresh(user3)
        await db.refresh(user4)
        await db.refresh(user5)
        await db.refresh(user6)
        await db.refresh(user7)
        await db.refresh(user8)
        await db.refresh(user9)

        # Create conversations
        conversation1 = Conversation(
            name="conv 1", user1_id=user1.id, user2_id=user2.id
        )
        conversation2 = Conversation(
            name="conv 2", user1_id=user3.id, user2_id=user4.id
        )

        db.add_all([conversation1, conversation2])
        await db.commit()

        await db.refresh(conversation1)
        await db.refresh(conversation2)

        await db.refresh(user1)
        await db.refresh(user2)
        await db.refresh(user3)
        await db.refresh(user4)

        # Create messages for conversations
        messages = [
            Message(
                conversation=conversation1,
                sender_id=user1.id,
                content="Hello from user1 to user2",
            ),
            Message(
                conversation=conversation1,
                sender_id=user2.id,
                content="Hello from user2 to user1",
            ),
            Message(
                conversation=conversation2,
                sender_id=user3.id,
                content="Hello from user3 to user4",
            ),
            Message(
                conversation=conversation2,
                sender_id=user4.id,
                content="Hello from user4 to user3",
            ),
        ]

        db.add_all(messages)
        await db.commit()

        await db.refresh(user1)
        await db.refresh(user2)
        await db.refresh(user3)
        await db.refresh(user4)

        # Create groupchats
        groupchat1 = GroupChat(name="Group Chat 1", admin_id=user1.id)
        groupchat2 = GroupChat(name="Group Chat 2", admin_id=user2.id)
        groupchat1.members.append(user1)
        groupchat1.members.append(user2)
        groupchat1.members.append(user3)

        db.add_all([groupchat1, groupchat2])
        await db.commit()

        await db.refresh(groupchat1)
        await db.refresh(groupchat2)

        await db.refresh(user1)
        await db.refresh(user2)
        await db.refresh(user3)
        await db.refresh(user4)

        # Create messages for groupchats
        group_messages = [
            Message(
                groupchat=groupchat1,
                sender_id=user1.id,
                content="Hello from user1 to groupchat1",
            ),
            Message(
                groupchat=groupchat1,
                sender_id=user2.id,
                content="Hello from user2 to groupchat1",
            ),
            Message(
                groupchat=groupchat2,
                sender_id=user3.id,
                content="Hello from user3 to groupchat2",
            ),
            Message(
                groupchat=groupchat2,
                sender_id=user4.id,
                content="Hello from user4 to groupchat2",
            ),
        ]
        db.add_all(group_messages)
        await db.commit()

        return {"message": "Test data added successfully"}
    except Exception as e:
        print(f"Error adding test data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding test data: {str(e)}")
