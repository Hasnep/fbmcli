# fbmcli
A Facebook Messenger Command-line Interface written in Python.

Currently uses a file called fbconfig.py to load configs.

## Commands (none implemented yet)
* `/switch` or `/s` - change to a different conversation
* `/react` or `/r` - react to a message
* `/like large/medium/small` or `/l l/m/s` - send a like
* `/config` or `/c` - refresh configs

## Configs (none implemented yet)
Default options first.
### Login
* Log in with:
    * Cookies with password fallback
    * Password
    * Username and password
### Choose thread
* Show `x` threads in list
* Show most recent message next to thread name:
    * Show
    * Do not show
### Message info
* Align my messages:
    * Left
    * Right
* Show own name as:
    * Nickname
    * First name
    * Full name
    * Me
    * Do not show
* Show other people's names as:
    * Nicknames
    * First names
    * Full names
    * Do not show
* Show names for:
    * Only the first message in a group
    * Every message
### Dates
* Show dates:
    * Only when the date changes
    * Every message
    * Do not show
* Show timestamps:
    * Only after `x` minutes of inactivity
    * Every message
    * Do not show
### Special messages
* Show emojis as:
    * Unicode emojis
    * Unicode descriptions
    * The `?` symbol
    * Do not show
* Show reactions as:
    * Unicode emojis
    * ASCII emoticons (customisable)
    * Text descriptions
    * Do not show
* Show likes as:
    * Description with size
    * Description
    * Do not show
* Show stickers as:
    * Description
    * Do not show
### Notifications
* Show notifications:
    * Do not show
    * Play a sound
    * Show W10 notifications
