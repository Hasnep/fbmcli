from fbchat import *
from fbchat.models import *
import pickle
from fbconfig import *

cookies_path = "cookies.pickle"

try:
    with open(cookies_path, 'rb') as handle:  # read the cookies file
        session_cookies = pickle.load(handle)
        try:
            client = Client(username, password, session_cookies=session_cookies)  # log in using cookies
        except:
            print("Could not log in using cookies or username and password.")
except:
    print("No cookies file found, logging in with username and password.")
    try:
        client = Client(username, password)  # log in using cookies
    except:
        print("Could not log in using username/password.")

session_cookies = client.getSession()  # put cookies in a variable
with open(cookies_path, 'wb') as handle:  # save the cookies to a file
    pickle.dump(session_cookies, handle)
