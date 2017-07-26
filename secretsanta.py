import random
import argparse
from twilio.rest import TwilioRestClient

from boto import dynamodb2
from boto.dynamodb2.table import Table

parser = argparse.ArgumentParser(description='Secret Santa Sorting.')
parser.add_argument('account_sid', help='Twilio Account sid - twilio.com/user/account')
parser.add_argument('auth_token', help='Twilio Auth Token - twilio.com/user/account')
parser.add_argument('aws_access_key', help='AWS Access Key - docs.aws.amazon.com')
parser.add_argument('aws_secret_key', help='AWS Secret Key - docs.aws.amazon.com')
parser.add_argument('dry_run', action='store_false', help='Dry Run is True by default')
args = parser.parse_args()
print args.echo

# Your Account Sid and Auth Token from twilio.com/user/account
client = TwilioRestClient(args.account_sid, args.auth_token)

matches=[]
elves=[]

TABLE_NAME = 'santas'
REGION = 'us-east-1'

conn = dynamodb2.connect_to_region(
    REGION,
    aws_access_key_id=args.aws_access_key,
    aws_secret_access_key=args.aws_secret_key
)
all_santas = Table(
    TABLE_NAME,
    connection=conn
)

santas=set()

result_set = all_santas.scan()
for elf in result_set:
	santas.add(elf['name'])

matches=set(santas)

for key in santas:
	if matches:
		string= '****** ' + key + ' ******'
		print string
		elves=list(matches)
		elf = all_santas.get_item(name=key)
		if key in elves:
			elves.remove(key)
		elf_family=elf['family']
		#print 'Family: ' + elf_family
		match=random.choice(elves)
		match_item=all_santas.get_item(name=match)
		match_family=match_item['family']
		#print 'Match Family: ' + match_family
		while elf_family == match_family:
		  match=random.choice(elves)
		  match_item=all_santas.get_item(name=match)
		  match_family=match_item['family']
		  #print 'New Match Family: ' + match_family
		matches.remove(match)
		elf['match']=match
		elf.save()
		phone=elf['phone']
		string='Hi ' + key + '! Your match is ' + match + '. Gifts should be around $25. Merry Christmas!'
		print string
        if args.dry_run:
            print 'Dry Run: text'
        else
	      #message = client.messages.create(body=string,
		         # 	to=phone,    # Replace with your phone number
	         #	from_='+18605165159') # Replace with your Twilio number
	         #print message
