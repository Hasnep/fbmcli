from login import *
# from pprint import pprint
from pdb import *  # use set_trace() to debug
from datetime import datetime
import os
import tzlocal
local_timezone = tzlocal.get_localzone()  # get timezone


def timestamp_to_string(timestamp, tz=local_timezone):
    """Converts a timestamp string to a human readable string"""
    date_string = int(float(timestamp))/1000
    date_string = datetime.fromtimestamp(date_string, tz)
    date_string = date_string.strftime("%I:%M:%S %p")
    return date_string


def get_thread_names(threads_object):
    """Input a threads object and return the list of user facing thread names."""
    names_list = []
    for i in range(len(threads_object)):
        cur_thread = threads_object[i]
        if cur_thread.type == ThreadType.USER and cur_thread.nickname is not None:
            names_list.append(cur_thread.nickname)
        else:
            names_list.append(cur_thread.name)
    return names_list


def get_thread_uids(threads_object):
    """Input a threads object and return the list of UIDs for each thread."""
    uids_list = []
    for i in range(len(threads_object)):
        cur_thread = threads_object[i]
        uids_list.append(cur_thread.uid)
    return uids_list


def get_threads(n_threads):
    """Input a number of threads and return the last n threads as a threads object."""
    threads = client.fetchThreadList(limit=n_threads)
    return threads


def print_choose_a_thread(threads):
    """Input a threads object and print a list of threads with indices next to their names."""
    threads_names = get_thread_names(threads)
    max_i_length = len(str(len(threads) - 1))
    print("Choose a thread:")
    for i, thread_name in enumerate(threads_names):
        print("[" + " " * (max_i_length - len(str(i))) + str(i) + "] " + thread_name)
    return


def thread_id_input(n_threads):
    """Input a number of threads an return the index of the chosen thread or None if an invalid index is chosen."""
    input_string = input(option_prompt)
    try:
        chosen_thread_index = int(float(input_string))
    except TypeError:
        max_thread = n_threads - 1
        print("Enter a number between 0 and %s." % max_thread)  # TODO: Add the ability to search.
        return None
    else:
        if 0 <= chosen_thread_index < n_threads:
            return chosen_thread_index
        else:
            max_thread = n_threads - 1
            print("Enter a number between 0 and %s." % max_thread)
            return None


def uid_to_chat(input_uid):
    """Input a UID and return either a USER or a GROUP object."""
    chat = client.fetchThreadInfo(input_uid)  # get the information about the thread
    chat = chat.values()  # turn the dict into a view object
    chat = list(chat)  # turn the view object into a list object
    chat = chat[0]  # get the first item in the list
    return chat


def choose_thread(n_threads):
    """Input the number of threads and return the chosen thread."""
    threads = get_threads(n_threads)
    chosen_thread_index = None
    while chosen_thread_index is None:
        print_choose_a_thread(threads)
        chosen_thread_index = thread_id_input(n_threads)
    threads_uids = get_thread_uids(threads)
    chosen_thread_uid = threads_uids[chosen_thread_index]
    chosen_thread = uid_to_chat(chosen_thread_uid)
    return chosen_thread


def get_chat_names(chat):
    """Input a user or a group to get a dict with everyone's UIDs and names."""
    chat_names = dict()
    if chat.type == ThreadType.USER:
        # TODO: make an option to have "ME:", yourname, or your nickname as your representation.
        # Set own name
        my_uid = client.uid
        if chat.own_nickname is None:
            chat_names[my_uid] = "Me"
        else:
            chat_names[my_uid] = chat.own_nickname
        # Set the other person's name
        if chat.nickname is None:
            chat_names[chat.uid] = chat.name
        else:
            chat_names[chat.uid] = chat.nickname
        return chat_names
    elif chat.type == ThreadType.GROUP:
        for k_uid in chat.participants:
            if k_uid in chat.nicknames:
                chat_names[k_uid] = chat.nicknames.get(k_uid)
            else:
                # TODO: Try to call fetchUserInfo() fewer times.
                chat_names[k_uid] = client.fetchUserInfo(k_uid)[k_uid].name
        return chat_names
    else:
        print("idk what you've done, that's not a user or a group, that's a %s" % str(chat.type))
        return None


def print_chatlog(chat, chat_names=None):
    """Print the chatlog."""
    if chat_names is None:
        chat_names = get_chat_names(chat)

    chatlog = client.fetchThreadMessages(chat.uid)
    chatlog.reverse()

    for message in chatlog:
        print(timestamp_to_string(message.timestamp) + " " + chat_names.get(message.author) + ": " + message.text)


def send_message(message_text, thread_uid, thread_type):
    client.send(Message(text=message_text), thread_id=thread_uid, thread_type=thread_type)


def message_input(chat):
    """Input a chat and ask the user for a message or a command, then parse it, either returning the name of the command or None for a message."""
    input_string = ""
    while input_string == "":
        input_string = input(option_prompt)
    if input_string.lstrip()[0] == "/":
        typed_command = input_string.lstrip().split(" ")[0][1:]
        return typed_command
    else:
        send_message(input_string, chat.uid, chat.type)
        return None


selected_chat = choose_thread(option_n_threads)
selected_chat_names = get_chat_names(selected_chat)
print_chatlog(selected_chat, chat_names=selected_chat_names)
command = None
while not(command == "quit" or command == "q"):
    command = message_input(selected_chat)
    if command is None:
        os.system("cls")
        print_chatlog(selected_chat, chat_names=selected_chat_names)
    elif command == "like" or command == "l":
        print("Sending a like...")
print("Goodbye!")
client.logout()
