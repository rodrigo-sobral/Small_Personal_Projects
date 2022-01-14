'''
    __author__ = "Rodrigo Sobral"
    __copyright__ = "Copyright 2021, Rodrigo Sobral"
    __credits__ = ["Rodrigo Sobral"]
    __license__ = "MIT"
    __version__ = "1.0.1"
    __maintainer__ = "Rodrigo Sobral"
    __email__ = "rodrigosobral@sapo.pt"
    __status__ = "Beta"
'''

import discord, datetime
from dotenv import load_dotenv
from keep_alive import keep_alive
from db_manage import insertNewMessage, message_db, getMostRecentMessageTime, logSentMessage
from os import getenv
from threading import Thread
from time import sleep


def defineBotIntents():
    intents = discord.Intents.default()
    intents.members = True
    return intents
client = discord.Client(command_prefix='!', intents=defineBotIntents(), help_command='!sch help')
wait_flag= False

#   ================================================================================


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(command: discord.Message):
    if command.author.bot: return
    #   Ask for help showing all the commands available
    if command.content=='!sch help':
        await command.channel.send(':clipboard: Here\'s a list of the current commands:\n`!sch <message> <target?> | <hours> <date?>`\n\nExample: ```!sch Have a good dinner John and Harry! @John @Harry | 20:21 19/07/2021\nor\n!sch Good morning guys! | 08:00```\n')

    #   Schedule a message to be sent
    elif command.content.startswith('!sch'):
        command.content= command.content[4:]
		
        tagged_users=[]
        if command.content.find('<@!')==-1 or command.mention_everyone: [tagged_users.append(member) for member in command.channel.members if not member.bot]
        else: [tagged_users.append(member) for member in command.mentions if not member.bot]
        
        #   Get Deliver Time from message
        if command.content.count('|')!=1: 
            return await command.channel.send(':warning: Invalid command format.\nExample: ```!sch Have a good dinner John and Harry! @John @Harry | 20:21 19/07/2021```\n')
        
        inputed_date= command.content[command.content.find(' | ')+3:]
        #   If the date is not given, use the current date
        deliver_date= getHoursAndDate(inputed_date)
        if not deliver_date: deliver_date=getOnlyHours(inputed_date)
        if not deliver_date: 
            return await command.channel.send(':warning: Invalid deliver time format.\nExample: ```!sch Have a good dinner John and Harry! @John @Harry | 20:21 19/07/2021```\n')
        del inputed_date

        #   Get Attachments from message
        attachments= await getAttachmentsFromMessage(command.attachments)

        #   Clear date and hours from message
        command.content= clearString(command.content[:command.content.find(' | ')])
        if not command.content and len(attachments)==0: return await command.channel.send(':warning: You must send any type of information (text or files)\n')
        message_container= {
            'channel_name': command.channel.name,
            'sender': command.author,
            'receivers': tagged_users,
            'content': command.content,
            'deliver_date': deliver_date,
            'attachments': attachments
        }
        
        #   Stores the new message to the queue
        try: insertNewMessage(message_container)
        except Exception as e: return await command.channel.send(str(e))
        
        return await command.channel.send(':white_check_mark: Your message \'{}\' (containing {} attachments) will be sent to{} at '.format(message_container['content'], len(attachments), printUsersTag(message_container['receivers'])) + deliver_date.strftime("%H:%M:%S, %d/%m/%Y"))

#   Event triggered by TrackTime to send direct messages to the tagged users
@client.event
async def on_sendDMs():
    global wait_flag
    for receiver in message_db[0]['receivers']:
        await receiver.send('{} sent you a message (with {} attachments): {}'.format(printUserTag(message_db[0]['sender']), len(message_db[0]['attachments']), message_db[0]['content']))
        [await receiver.send(file=attachment) for attachment in message_db[0]['attachments']]
    registMessage(message_db[0])
    message_db.pop(0)
    wait_flag= False


#   ================================================================================

#   Clear all the not necessary spaces until the string is cleared or empty
def clearString(string: str):
    id_index= string.find('<@!')
    if id_index!=-1: string= string[:id_index]
    while string and string[0].isspace(): string= string[1:]
    while string and string[-1].isspace(): string= string[:-1]
    return string

#   When the command only indicates hours (the date is, by default, today's date)
def getOnlyHours(inputed_date:str):
    today= datetime.datetime.now()
    try: hour= datetime.datetime.strptime(inputed_date, '%H:%M:%S')
    except:
        try: hour= datetime.datetime.strptime(inputed_date, '%H:%M')
        except: return None
    return today.replace(hour=hour.hour, minute=hour.minute, second=hour.second, microsecond=0)

#   When the command indicates hours and a date to the message be delivered
def getHoursAndDate(inpute_date: str):
    if inpute_date.find(' ')==-1: return None
    try: date= datetime.datetime.strptime(inpute_date, '%H:%M:%S %d/%m/%Y')
    except:
        try: date= datetime.datetime.strptime(inpute_date, '%H:%M %d/%m/%Y')
        except: return None
    return date

#   Get the list of attachments from the command and returns a list of discord.Files
async def getAttachmentsFromMessage(attachments_list: list) -> discord.File:
    if len(attachments_list)==0: return []
    files= []
    for attachment in attachments_list:
        new_file= await discord.Attachment.to_file(attachment)
        files.append(discord.File(new_file.fp, filename=new_file.filename))
    return files
        
def printUserTag(user: discord.User): return '<@!'+str(user.id)+'>'
def printUsersTag(users: list): 
	text_format= ''
	for user in users: text_format+= ' <@!'+str(user.id)+'>' 
	return text_format
def printUserName(user: discord.User): return str(user.name)
def printUsersName(users: list): 
	text_format= ''
	for user in users: text_format+= ' '+str(user.name)
	return text_format

#   Sends a formatted log of a sent message to logSentMessage(), in db_manage.py
def registMessage(message_container: dict):
    logSentMessage('{}: {} [{}] ->{} | '.format(message_db[0]['channel_name'], printUserName(message_db[0]['sender']), len(message_db[0]['attachments']), printUsersName(message_container['receivers'])) + message_container['deliver_date'].strftime("%H:%M:%S, %d/%m/%Y"))


#   We keep tracking current time to send messages in real time
def trackTime():
    global wait_flag
    print('Tracking Time...')
    while True: 
        now = datetime.datetime.now().replace(microsecond=0)
        first_message_time= getMostRecentMessageTime()
        if not wait_flag and first_message_time and first_message_time <= now:
                client.dispatch('sendDMs')
                wait_flag= True
        sleep(1)


#  ================================================================================


def runClient(): client.run(getenv('SCHEDULING_BOT_TOKEN'))
if __name__ == "__main__":
    load_dotenv()
    Thread(target=runClient).start()
    Thread(target=trackTime).start()
    keep_alive()