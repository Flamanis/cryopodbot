import discord
import asyncio
import random
import time
from pw_bot import *
client = discord.Client()

@client.event
async def on_ready():
	print('LOGGED IN!')

@client.event
async def on_message(message):
	if message.content.startswith('!optin'):
		role = discord.utils.get(message.server.roles, name='@updaters')
		tmp = await client.send_message(message.channel, 'Trying to add you, @' + str(message.author))
		await client.add_roles(message.author, role)
		await client.edit_message(tmp, 'Added!')
		await asyncio.sleep(30)
		await client.delete_message(tmp)
		await client.delete_message(message)
	elif message.content.startswith('!optout'):
		role = discord.utils.get(message.server.roles, name='@updaters')
		tmp = await client.send_message(message.channel, 'Trying to remove you, @' + str(message.author))
		await client.remove_roles(message.author, role)
		await client.edit_message(tmp, 'Removed!')
async def new_part_checker():
	await client.wait_until_ready()
	while True:
		file = open('newpart.txt', 'r')
		firstline = file.readline()
		if str(firstline)[0] == '1':
			topost = file.readline()
			tmp = await client.send_message(client.get_channel('226088087996989450'), topost)
			file.close()
			file = open('newpart.txt', 'w')
			file.write('0')
			file.close()
		await asyncio.sleep(30)
#async def reminder():
#	await client.wait_until_ready()
#	while True:
#		tmp = await client.send_message(client.get_channel('246162218104782848'), 'AUTOMATED MESSAGE: If you\'re not already subscribed on the discord, be sure to subscribe by doing !optin and if you feel the need to unsubscribe, just do !optout - in any chat! Also, here\'s some handy links:' + '\n' + 'Klok\'s Patreon: <https://www.patreon.com/klokinator>' + "\n" + 'My Github: <https://github.com/TGWaffles/cryopodbot>' + "\n" + 'Subreddit: <http://reddit.com/r/thecryopodtohell>')
#		await asyncio.sleep(21600)
#		await client.delete_message(tmp)
client.loop.create_task(new_part_checker())
#client.loop.create_task(reminder())
client.run(DISCORD_TOKEN)