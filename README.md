# wall-E
                                         _   _
                                       /u@) (@\\
                                   nn      Y
                                   'Y  ____H____
                                    \V |- ["] -|___,,
                                     \\|T 'T' T|___nn
                                     | ||  |  ||   UU
                                    /` `\\wall.E`\\
                                   /  /A \\  /  A \\
                                   L______J L_____J

small python based soundcloud downloader
===

Requirements
---
- Python 3
- pip
- Soundcloud account
- soundcloud playlist with title '//TODO'
- Gmail account for mail reporting

Installation
---
```
pip install --upgrade -r requirements.txt
```

Setup
---
Run the script once to create the following basic config stub which will be saved as 'walle.ini'
```
[CREDENTIALS]
client_id = XXXXX
client_secret = XXXXX
soundcloud_user = soundcloud_email
soundcloud_pw = soundcloud_password
reporting_mail = sender_email
reporting_pw = sender_password
notification_mail = report_receiver_mail

[PLAYLISTS]

[PATH]
pathtomusic = where/to/save/tracks/
```
Fill in the credentials as shown, to get the client_id and client_secret visit 
https://auth0.com/docs/connections/social/soundcloud

For mail reporting fill in the credentials of the mail adress reports should be sent from, current version of wall-E only supports gmail accounts, notification mail can be from any provider.

After that rerun the script to continue setting up the config.
It is of fundamental importance to have a playlist titled '//TODO', otherwise wall-E will not know which tracks to download :disappointed:

The script will now fill the PLAYLIST section of the config file as shown
```
[PLAYLISTS]
todolistid = 1234567890
sets = {
        '0123456789' : 'playlist1',
        '9012345678' : 'playlist2',
        '8901234567' : 'playlist3',
        }
```
Last step is to ajdust the found playlist names to corresponding directory names in which the tracks will be saved if they are contained in the according playlist,
otherwise the downloaded tracks will be saved in the root directory set in the config file.
Now wall-E is ready for his tasks, regardless of wether triggered manually or as cronjob.

Troubleshooting
---
Remove `walle.ini` and rerun setup!
