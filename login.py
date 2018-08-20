from fbconfig import *
import fbchat as fb
import pickle


def login(_config=config):
    try:
        with open(_config["cookies_path"], "rb") as handle:  # read the cookies file
            session_cookies = pickle.load(handle)
    except FileNotFoundError:
        print("No cookies file found, logging in with username and password.")
        try:
            client = fb.Client(_config["username"], _config["password"])  # log in using cookies
        except:
            print("Could not log in using username/password.")
            return None
    else:
        try:
            client = fb.Client(_config["username"], _config["password"], session_cookies=session_cookies)  # log in using cookies
        except:
            print("Could not log in using cookies or username and password.")
            return None

    session_cookies = client.getSession()  # put cookies in a variable
    with open(_config["cookies_path"], "wb") as handle:  # save the cookies to a file
        pickle.dump(session_cookies, handle)

    return client
