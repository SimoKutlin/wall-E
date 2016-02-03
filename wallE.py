import os
import time
import ast
import subprocess
import smtplib
import soundcloud
from ConfigParser import ConfigParser

def printHeader():
    print "                                     _   _"
    print "                                   /u@) (@\\"
    print "                               nn      Y"
    print "                               'Y  ____H____"
    print '                                \V |- ["] -|___,,'
    print "                                 \\ |T 'T' T|___nn"
    print "                                 | ||  |  ||   UU"
    print "                                /` `\\wall.E`\\"
    print "                               /  /A \\  /  A \\"
    print "                               L______J L_____J"
    print ' *---------------------------------------------------------------------------*'
    print ' |                              Waaaaallleeee                                |'
    print ' *---------------------------------------------------------------------------*\n'
    return;

def check_config():
# if no config exists default config stub will be created
    if not os.path.isfile(configPath):
	print 'No walle.ini was found, walle-E will create new one!\n'

        config.add_section('CREDENTIALS')
        config.add_section('PLAYLISTS')
        config.add_section('PATH')
        config.set('CREDENTIALS', 'client_id', 'XXXXXXXXXXXXXXXXXXXX')
        config.set('CREDENTIALS', 'client_secret', 'XXXXXXXXXXXXXXXXXXXX')
        config.set('CREDENTIALS', 'soundcloud_user', 'soundcloud_email')
        config.set('CREDENTIALS', 'soundcloud_pw', 'soundcloud_password')
        config.set('CREDENTIALS', 'reporting_mail', 'sender_email')
        config.set('CREDENTIALS', 'reporting_pw', 'sender_password')
        config.set('CREDENTIALS', 'notification_mail', 'report_receiver_mail')
        config.set('PATH', 'pathtomusic', 'where/to/save/songs/')

        with open(configPath, 'w') as configfile:
            config.write(configfile)

        print('Created new walle.ini! Please setup and rerun!')
        exit(0)

    return

def configurePlaylists():
    print 'setting up playlists'
    client = soundcloud.Client(
        client_id=credentials['ID'],
        client_secret=credentials['secret'],
        username=credentials['soundcloud_mail'],
        password=credentials['soundcloud_pw']
    )

    foundSets = client.get('/me/playlists/')
    configuredSets = '{\n'

    for set in foundSets:
	if set.title == '//TODO':
	    config.set('PLAYLISTS', 'todoListID', set.id)
	else:
            configuredSets += "'" + str(set.id) + "' : '" + str(set.title) + "',\n"

    configuredSets += '}'
    config.set('PLAYLISTS', 'sets', configuredSets)

    with open(configPath, 'w') as configfile:
        config.write(configfile)

    print 'Playlists found and set, review config and adjust folder, then rerun again!'
    exit(0)
    return;

def getDirectory( id ):
    for set in sets.keys():
        tmp_set = client.get('/me/playlists/' + set)
        tmp_tracks = tmp_set.tracks

        for tmp_track in tmp_tracks:
            if id == tmp_track['id']:
                return sets[set];

    #song in no playlist, use soundcloud root directory
    return '';

def downloadSong( url, path ):
    # check if https url, if not correct it first
    if 'https' not in url:
	url = url.replace('http', 'https', 1)
    try:
	dl_path = basePath
	# check if specific directory is set for song, if not use root soundcloud directory
        if path:
	    dl_path = dl_path + path

        output = subprocess.check_output(["scdl", "-p", dl_path, "-l", url], stderr=subprocess.STDOUT)
	print output
	
	# downloading song failed, remember song to notify user
	if '<url> malformed' in output:	    
	    failed_downloads[url] = path

    except OSError:
        print 'Error ocurred, shutting down Walle!'
        sendMail( 1 )
        exit(0)
    print '\n'
    return;

def sendMail( error, didSmth, failedOnes=None ):
    msg = 'walle-E reporting status on daily basis from ' + time.strftime("%d.%m.%Y") + ":\n\n"

    if didSmth == 0:
        msg += "Todolist was found empty, so there was nothing to do."
    else:
        if error == 0:
            if not failedOnes:
                msg += "Successfully downloaded " + str(len(todo_list)) +  " songs!"
            else:
                msg += "Tried downloading " + str(len(todo_list)) +  " songs, however could not download these urls:\n"
	        for key, value in failedOnes.iteritems():
                    msg += "    >> " + key + " \n"
        
                msg += "\n but walle-E tried his best!"
        else:
            msg += "While downloading a song walle-E encountered an error, but wall-E tried his best!"

    msg += "\n\n have a nice day\n wall-E over and out"
    fullMsg = "\r\n".join(["From: " + credentials['reporting_mail'], "To: " + credentials['notification_mail'], "Subject: wall-E status reporting", "", msg])

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(credentials['reporting_mail'], credentials['reporting_pw'])
    server.sendmail(credentials['reporting_mail'], credentials['notification_mail'], fullMsg)
    server.quit()
    return;

printHeader()

# check if config file exists, if not set up and shutdown wall-E
config = ConfigParser()
configPath = os.path.realpath(__file__)
configPath = configPath[:configPath.rfind('/')] + '/walle.ini'
check_config()

# read credentials and playlist information from config file
print 'Walle reading config...'
config.read(configPath)

credentials = {}
credentials['ID'] = config.get('CREDENTIALS', 'client_id')
credentials['secret'] = config.get('CREDENTIALS', 'client_secret')
credentials['soundcloud_mail'] = config.get('CREDENTIALS', 'soundcloud_user')
credentials['soundcloud_pw'] = config.get('CREDENTIALS', 'soundcloud_pw')
credentials['reporting_mail'] = config.get('CREDENTIALS', 'reporting_mail')
credentials['reporting_pw'] = config.get('CREDENTIALS', 'reporting_pw')
credentials['notification_mail'] = config.get('CREDENTIALS', 'notification_mail')

if not config.has_option('PLAYLISTS', 'todoListID'):
    configurePlaylists()

todoListID = config.get('PLAYLISTS', 'todoListID')
sets = ast.literal_eval(config.get('PLAYLISTS', 'sets'))
basePath = os.path.expanduser('~') + '/' + config.get('PATH', 'pathtomusic')

print 'Config read!\n'

# set up connection to soundcloud
print 'Connecting to soundcloud...\n'
client = soundcloud.Client(
    client_id=credentials['ID'],
    client_secret=credentials['secret'],
    username=credentials['soundcloud_mail'],
    password=credentials['soundcloud_pw']
)

print 'Fetching todo list...'
todolist = client.get('/me/playlists/' + todoListID)
songs = todolist.tracks

#no songs found, nothing to download
if len(songs) == 0:
   print 'Walle did not find any songs, reporting status and returning to sleep...'
   sendMail(0, 0)
   exit(0)
elif len(songs) == 1:
   print 'Walle found one track to download...\n'
else:
   print 'Walle found ', len(songs), ' tracks to download...\n'

#gather songs to download
print 'Walle is now gathering the tracks set to download...'
fetch_list = {}
for track in songs:
   fetch_list[track['id']] = track['permalink_url']
print 'Walles todolist is complete!\n'

#set up file system folders
print 'Walle setting up folders...'
for folder in sets.values():
    tmp_path = basePath + '/' + folder
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
print 'Folders setup!\n'

#lookup folder to save song
print 'Looking up folders for found songs...'
todo_list = {}
for track_id in fetch_list.keys():
    todo_list[fetch_list[track_id]] = getDirectory(track_id)
print 'Folders found & set!\n'

#download songs
print 'Walle will download songs now...\n'
failed_downloads = {}
for key, value in todo_list.iteritems():
    downloadSong( key, value)
print '\nDownload finished!\n'

#send mail report
print 'Sending report mail...'
sendMail(0, 1, failed_downloads)
print 'Report sent!\n'

#clear soundcloud todolist
print 'Cleaning todolist...'
todolist.tracks = map(lambda id: dict(id=id), [0])
client.put(todolist.uri, playlist={'tracks':todolist.tracks})
print 'Todolist cleaned!\n'

print 'Walle over&out!'

exit(0)
