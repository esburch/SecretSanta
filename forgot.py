import random
from twilio.rest import TwilioRestClient

from boto import dynamodb2
from boto.dynamodb2.table import Table

# Your Account Sid and Auth Token from twilio.com/user/account
client = TwilioRestClient()

matches=[]
elves=[]

TABLE_NAME = "santas"
REGION = "us-east-1"

conn = dynamodb2.connect_to_region(REGION)
all_santas = Table(
    TABLE_NAME,
    connection=conn
)

#santas={'Emily':'+18606058991','Ann':'+18606058993','Paul B':'+18606058946','Ashley':'+17073860608','Steve':'+17073981264'}

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
		print 'Match Family: ' + match_family
		while elf_family == match_family:
		  match=random.choice(elves)
		  match_item=all_santas.get_item(name=match)
		  match_family=match_item['family']
		  print 'New Match Family: ' + match_family
		matches.remove(match)
		# elf['match']=match
		# elf.save()
		phone=elf['phone']
		string=key + ' matched with ' + match + ' text ' + phone
		print string
