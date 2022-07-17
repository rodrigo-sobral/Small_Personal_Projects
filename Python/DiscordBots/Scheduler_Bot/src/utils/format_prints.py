from typing import List
from discord import User

def printUserTag(user: User):
	return f'<@!{str(user.id)}>'

def printUsersTag(users: List[User]):
	return ' '.join([printUserTag(user) for user in users])

def printUsersName(users: List[User]):
	return ' '.join([user.name for user in users])
