from orm import NoMatch

from models.models import *

def update(main):
    async def wrapper_update(*args):
        try:
            user_id = (args[0]).from_user.id
            user = await AuthUser.objects.get(username=user_id)
            await user.update(last_login=dt.now())
            return await main(args)
        except NoMatch:
            return await main(args)
    return wrapper_update