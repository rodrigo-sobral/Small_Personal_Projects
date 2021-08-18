import datetime
message_db= []

#   Inserts and manages all messages scheduled to be delivered at the right time (from the most recent to the latest one)
def insertNewMessage(message_container: dict):
    try: compareTime2Now(message_container['deliver_date'])
    except Exception as e: raise ValueError(str(e))

    #   Compare year, month, day, hour, minute, second of message_container to existing messages
    for message_index in range(len(message_db)):
        if message_container['deliver_date'] <= message_db[message_index]['deliver_date']:
            message_db.insert(message_index, message_container)
            return True
        elif message_container['deliver_date'] > message_db[message_index]['deliver_date']: continue
    message_db.append(message_container)

#   Compare year, month, day, hour, minute, second of message_container to real time and raise error if out of date       
def compareTime2Now(deliver_date: datetime):
    now = datetime.datetime.now()
    if deliver_date < now:
        raise ValueError(':warning: Invalid date. You must insert a date after {}:{}:{} {}/{}/{}\n'.format(now.hour, now.minute, now.second, now.day, now.month, now.year))
    return

#   Get the first message that must be delivered
def getMostRecentMessageTime(): 
    return message_db[0]['deliver_date'] if len(message_db)!=0 else None


#  ================================================================================


#   Logs sent messages
def logSentMessage(sent_message: str):
    with open('./logs/sent_messages.log', 'a') as log_file: log_file.write(sent_message+'\n')

def clearLogs():
    with open('./logs/sent_messages.log', 'w') as log_file: log_file.write('')