import random
import os
import argparse
from twilio.rest import Client

from boto import dynamodb2
from boto.dynamodb2.table import Table

parser = argparse.ArgumentParser(description='Secret Santa Sorting. Twilio Account SID and Auth Token should be environment variables.')
parser.add_argument('action', help='Options: assign send')
args = parser.parse_args()

ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

client = Client()

matches=[]
elves=[]

TABLE_NAME = 'santas_test'
REGION = 'us-east-1'

conn = dynamodb2.connect_to_region(REGION)

all_santas = Table(
    TABLE_NAME,
    connection=conn
)

santas=set()

result_set = all_santas.scan()
for elf in result_set:
    santas.add(elf['name'])

matches=set(santas)

def sendTexts():
    for key in santas:
        if matches:
            string= '****** ' + key + ' ******'
            print string
            elves=list(matches)
            elf = all_santas.get_item(name=key)
            if key in elves:
                elves.remove(key)

            phone=elf['phone']
            match=elf['match']
            textMessage='Hi ' + key + '! Your match is ' + match + u". Gifts should be around $25. Merry Christmas! \U0001F384 \U0001F381"
            message = client.messages.create(body=textMessage,
                        to=phone,    # Replace with your phone number
                   from_='+18605165159') # Replace with your Twilio number
            print message

def assignMatches():
    for key in santas:
        if matches:
            string= '****** ' + key + ' ******'
            print string
            elves=list(matches)
            elf = all_santas.get_item(name=key)
            if key in elves:
                elves.remove(key)
            elf_family=elf['family']
            print 'Family: ' + elf_family
            match=random.choice(elves)
            match_item=all_santas.get_item(name=match)
            match_family=match_item['family']
            print 'Match Family: ' + match_family
            attempt = 0
            if attempt < 5:
              while elf_family == match_family:
                match=random.choice(elves)
                match_item=all_santas.get_item(name=match)
                match_family=match_item['family']
                print 'New Match Family: ' + match_family
              attempt+=1
            matches.remove(match)
            elf['match']=match
            elf.save()

accepted_strings = {'assign', 'send'}


if args.action in accepted_strings:
    if args.action == 'assign':
        try:
            assignMatches()
            pass
        except Exception as e:
            raise

    if args.action == 'send':
        try:
            sendTexts()
            pass
        except Exception as e:
            raise

else:
    raise
