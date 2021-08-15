import discord, datetime
from dotenv import load_dotenv
from keep_alive import keep_alive
from db_manage import insertNewMessage, message_db, getMostRecentMessageTime
from os import getenv
from threading import Thread
from time import sleep

def defineBotIntents():
    intents = discord.Intents.default()
    intents.members = True
    return intents
client = discord.Client(command_prefix='!', intents=defineBotIntents(), help_command='!sch help')
wait_flag= False

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

        #   Clear date and hours from message
        command.content= clearString(command.content[:command.content.find(' | ')])
        message_container= {
            'sender': command.author,
            'receivers': tagged_users,
            'content': command.content,
            'deliver_date': deliver_date
        }
        
        try: insertNewMessage(message_container)
        except Exception as e: return await command.channel.send(str(e))
        
        return await command.channel.send(':white_check_mark: Your message \'{}\' will be sent to{} at '.format(message_container['content'], printUsersTag(message_container['receivers'])) + deliver_date.strftime("%H:%M:%S, %d/%m/%Y"))

@client.event
async def on_sendDMs():
    global wait_flag
    for receiver in message_db[0]['receivers']:
        await receiver.send('{} sent you a message: {}'.format(printUserTag(message_db[0]['sender']), message_db[0]['content']))
    message_db.pop(0)
    wait_flag= False


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


#   ================================================================================
#   Add a 0 to the beginning of deciaml numbers to make them more readable
def clearString(string: str):
    string= string[:string.find('<@!')]
    while string[0].isspace(): string= string[1:]
    while string[-1].isspace(): string= string[:-1]
    return string

def getOnlyHours(inputed_date:str):
    today= datetime.datetime.now()
    try: hour= datetime.datetime.strptime(inputed_date, '%H:%M:%S')
    except:
        try: hour= datetime.datetime.strptime(inputed_date, '%H:%M')
        except: return None
    return today.replace(hour=hour.hour, minute=hour.minute, second=hour.second, microsecond=0)
def getHoursAndDate(inpute_date: str):
    if inpute_date.find(' ')==-1: return None
    try: date= datetime.datetime.strptime(inpute_date, '%H:%M:%S %d/%m/%Y')
    except:
        try: date= datetime.datetime.strptime(inpute_date, '%H:%M %d/%m/%Y')
        except: return None
    return date

def printUserTag(user: discord.User): return '<@!'+str(user.id)+'>'
def printUsersTag(users: list): 
	text_format= ''
	for user in users: text_format+= ' <@!'+str(user.id)+'>' 
	return text_format


#  ================================================================================


def runClient(): client.run(getenv('SCHEDULING_BOT_TOKEN'))
if __name__ == "__main__":
    load_dotenv()
    Thread(target=runClient).start()
    Thread(target=trackTime).start()
    keep_alive()