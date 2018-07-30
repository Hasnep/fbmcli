from login import *
from PyInquirer import *
from pprint import pprint
from datetime import datetime
import tzlocal
local_timezone = tzlocal.get_localzone()  # get timezone


def tstostring(timestamp, tz=local_timezone):
    """Converts a timestamp string to a human readable string"""
    date_string = int(float(timestamp))/1000
    date_string = datetime.fromtimestamp(date_string, tz)
    date_string = date_string.strftime("%I:%M:%S %p")
    return date_string


threads = client.fetchThreadList(limit=n_contacts_list)  # get the list of most recent threads
threads_list = []
for i in range(n_contacts_list):
    cur_thread = threads[i]
    if cur_thread.type == ThreadType.USER and cur_thread.nickname is not None:
        threads_list.append(cur_thread.nickname + " (" + str(i) + ")")
    else:
        threads_list.append(cur_thread.name + " (" + str(i) + ")")

# define a question to ask the user
choose_thread = [
    {
        'type': 'rawlist',
        'name': 'selected_thread',
        'message': 'Choose a thread:',
        'choices': threads_list
    },
]

selected_thread = prompt(choose_thread)  # ask the user to choose a thread from a list
selected_thread = selected_thread['selected_thread']  # get the answer as a string
selected_thread = selected_thread[-2: -1]  # subset the string to get the index
selected_thread = int(float(selected_thread))  # convert the string to a float then an int
selected_thread = threads[selected_thread]  # get the ith item of the recent threads list
selected_thread = selected_thread.uid  # get the uid of the thread
selected_thread = client.fetchThreadInfo(selected_thread)  # get the information about the thread
selected_thread = selected_thread.values()  # turn the dict into a view object
selected_thread = list(selected_thread)  # turn the view object into a list object
selected_thread = selected_thread[0]  # get the first item in the list

names = dict()
if selected_thread.type == ThreadType.USER:
    if selected_thread.own_nickname is None:
        names[client.uid] = "me"
    else:
        names[client.uid] = selected_thread.own_nickname  # TODO: make an option to have "ME:", yourname, or your nickname
    if selected_thread.nickname is None:
        names[selected_thread.uid] = selected_thread.name
    else:
        names[selected_thread.uid] = selected_thread.nickname
elif selected_thread.type == ThreadType.GROUP:
    for participant_uid in selected_thread.participants:
        if participant_uid in selected_thread.nicknames:
            names[participant_uid] = selected_thread.nicknames.get(participant_uid)
        else:
            participant_info = client.fetchUserInfo(participant_uid)
            participant_info = participant_info[participant_uid]
            names[participant_uid] = participant_info.name
else:
    print("selected thread is not a user or a group")

chat = client.fetchThreadMessages(selected_thread.uid)
chat.reverse()

for message in chat:
    print(tstostring(message.timestamp) + " " + names.get(message.author) + ": " + message.text)

client.logout()

# import pdb; pdb.set_trace()

# fetchThreadMessages
# fetchUnread()
# fetchAllUsers
