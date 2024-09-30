from database.models import async_session
from database.models import User
from sqlalchemy import select, update


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper


@connection
async def set_user(session, user_id):
    user = await session.scalar(select(User).where(User.user_id == user_id))

    if not user:
        session.add(User(user_id=user_id))
        await session.commit()
        return False
    else:
        return user


@connection
async def update_user(session, user_id, tg_name, age, question2, question3, question4, question5):
    await session.execute(update(User).where(User.user_id == user_id).values(tg_name=tg_name, age=age,
                                                                             question2=question2, question3=question3,
                                                                             question4=question4, question5=question5))
    await session.commit()


