from __future__ import print_function
import httplib2
import os
from datetime import time, datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Friend.settings')
import schedule
import django
django.setup()
from directory.models import Page, Person
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
from slugify import slugify
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():

    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    
    """
   
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if len(events)>0:
        print(time.time)
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            try:
                Person.objects.get(name=event['summary'])
                slug=slugify(event['summary'])
                print("success")
                urlstring=('http://127.0.0.1:8000/directory/person/' + slug + '/email/')
                print (urlstring)
                driver = webdriver.PhantomJS()
                driver.get(urlstring)
            except Person.DoesNotExist:
                print(start, event['summary'])
           
                
        else:
            print("nay")
        print("Sleeping for 6 hours")
    else:
        print("No upcoming events")

schedule.every().day.at("23:59").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == '__main__':
    main()

