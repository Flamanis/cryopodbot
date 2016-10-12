#!/usr/bin/python
import sys
import logging
import discord
from discord.ext import commands
import praw
import pdb
import re
import time
#Imports all passwords from a hidden file ;)
from pw_bot import *
logging.basicConfig(level=logging.INFO)
user_agent = ("CryoBot 1.0")
#Starts the main section of the reddit bot and assigns it to r.
r = praw.Reddit(user_agent = user_agent)
#Connects to the TCTH sub.
subreddit = r.get_subreddit("thecryopodtohell")
#Logs into Bot's Account from hidden file above.
r.login(REDDIT_USERNAME, REDDIT_PASS)
#for submission in subreddit.get_new(limit = 1):
#	author = submission.author
#	print(author)
#	time.sleep(5)
#	if str(author).lower() == "klokinator":
#		print("TEST!")
#		time.sleep(5)
		#if str(submission.title)[0:4].lower() == "part":
#Fetches all messages sent to the bot.
messages = r.get_messages()
already_done = []
alreadyin = []
#For every message in the messages you just fetched:
for message in messages:
	#Open the username list
	file = open('list.txt', 'r+')
	#Add names from a username to a list and post ids to another.
	for line in file:
		linelen = len(line)
		newlinelen = linelen - 1
		if line[:newlinelen] not in alreadyin:
			alreadyin.append(line[:newlinelen])
	otherfile = open('done.txt', 'r+')
	for i in range(2):
		for line in otherfile:
			linelen = len(line)
			newlinelen = linelen - 1
			if line[:newlinelen] not in already_done:
				already_done.append(line[:newlinelen])
	#If the message talks about subscription, and if the author hasn't already been added and the id isn't done:
	if "unsubscribe" in str(message.body).lower() and str(message.author) in alreadyin and str(message.id) not in already_done:
		message.reply("BOT: You've been unsubscribed!")
		f = open("list.txt","r+")
		d = f.readlines()
		f.seek(0)
		for i in d:
			if str(message.author) not in i:
		                f.write(i)
		f.truncate()
		f.close()
		already_done.append(message.id)
		otherfile.write(str(message.id) + "\n")
	elif "subscribe" in str(message.body).lower() and str(message.author) not in alreadyin and str(message.id) not in already_done:
		#Double check to attempt to double-post proof.
		if str(message.author) not in alreadyin:
			#Write the sender's name in the username list.
			file.write(str(message.author) + "\n")
			#Tells the sender they've been added.
			message.reply("BOT: Thanks, you've been added to the list!")
			time.sleep(2)
			#Adds their name to the ID list and stuff.
			alreadyin.append(message.author)
			already_done.append(message.id)
			otherfile.write(str(message.id) + "\n")
	otherfile.close()
	file.close()
#Empty list to prevent double posts.
fixit = []
#For thread in the subreddit, out of the newest thread.
for submission in subreddit.get_new(limit=1):
	time.sleep(3)
	#Set variables to prevent annoying the reddit api.
	author = submission.author
	title = str(submission.title)
	id = str(submission.id)
	#Same as message checking but for threads.
	file = open('parts.txt','r+')
	for line in file:
		linelen = len(line)
		newlinelen = linelen - 1
		if line[:newlinelen] not in fixit:
			fixit.append(line[:newlinelen])
	#If the author is Klok and it begins with part, do this:
	if str(author).lower() == "klokinator" and title[0:4].lower() == "part" and id not in fixit:
		file.write(id + "\n")
		time.sleep(5)
		file.close()
		file = open('list.txt', 'r+')
		alreadyin = []
		#Post the comment on the thread.
		postedcomment = submission.add_comment("Hi. I'm a bot, bleep bloop." + "\n" + "\n" + "If you're about to post regarding a typo and this Part was just posted, please wait ten minutes, refresh, and then see if it's still there!" + "\n" + "\n" + "Also, if you want to report typos anywhere, please respond to this bot to keep the main post clutter free. Thank you!" + "\n" + "\n" + "\n" + "[Click Here to be PM'd new updates!](https://np.reddit.com/message/compose/?to=CryopodBot&subject=Subscribe&message=Subscribe) " + "[Click Here to unsubscribe!](https://np.reddit.com/message/compose/?to=CryopodBot&subject=unsubscribe&message=unsubscribe)" + "\n" + "\n" + "\n" + "If you want to donate to Klokinator, send paypal gifts to Klokinator@yahoo.com, but be sure to mark it as a gift or Paypal takes 10%. " + "\n" + "\n" + "Patreon can also be pledged to [here!](https://www.patreon.com/klokinator)")
		submission.set_flair("STORY", "story")
		#Sticky the comment that was just posted.
		postedcomment.distinguish(sticky=True)
		#Get the index list's ID.
		toedit = r.get_submission(submission_id='56tvbw')
		time.sleep(2)
		#Add post that was just posted to the index list.
		tempedit = toedit.selftext
		putin = tempedit + "\n" + "\n" + "[" + submission.title + "](" + submission.permalink + ")"
		time.sleep(2)
		toedit.edit(putin)
		time.sleep(2)
		#Put all users in the username file into a list, then:
		file.close()
		file = open('list.txt','r+')
		for line in file:
			linelen = len(line)
			newlinelen = linelen -1
			if line[:newlinelen] not in alreadyin:
				alreadyin.append(line[:newlinelen])
		#For every name in the list, send them this message with the link to the part.
		for name in alreadyin:
			r.send_message(name, "New Post!", "[New Post on /r/TheCryopodToHell!](" + submission.permalink + ")")
			time.sleep(2)
		file.close()
	else:
		file.close()
#Gets all comments in the subreddit, then flattens them.
subreddit_comments = subreddit.get_comments()
subcomments = praw.helpers.flatten_tree(subreddit_comments)
#Loops through every comment in the sub.
for comment in subcomments:
	#Opens file with comment ids.
	otherfile = open('done.txt','r+')
	#Do it twice to make sure.
	for i in range(2):
		for line in otherfile:
			linelen = len(line)
			newlinelen = linelen - 1
			if line[:newlinelen] not in already_done:
				already_done.append(line[:newlinelen])
	#If someone's tagging us and we've not processed their comment:
	if "/u/cryopodbot" in str(comment.body).lower() and str(comment.id) not in already_done:
		#If it's talking about the post, comment the post.
		if "post" in str(comment.body).lower():
			#Make sure the bot doesn't respond to itself.
			if str(comment.author).lower() != "cryopodbot":
				#Reply!
				comment.reply("Hi. I'm a bot, bleep bloop." + "\n" + "\n" + "If you're about to post regarding a typo and this Part was just posted, please wait ten minutes, refresh, and then see if it's still there!" + "\n" + "\n" + "Also, if you want to report typos anywhere, please respond to this bot to keep the main post clutter free. Thank you!" + "\n" + "\n" + "\n" + "[Click Here to be PM'd new updates!](https://np.reddit.com/message/compose/?to=CryopodBot&subject=Subscribe&message=Subscribe) " + "[Click Here to unsubscribe!](https://np.reddit.com/message/compose/?to=CryopodBot&subject=unsubscribe&message=unsubscribe)" + "\n" + "\n" + "\n" + "If you want to donate to Klokinator, send paypal gifts to Klokinator@yahoo.com, but be sure to mark it as a gift or Paypal takes 10%. " + "\n" + "\n" + "Patreon can also be pledged to [here!](https://www.patreon.com/klokinator)")
				#Post the ID to a file to prevent duplicates.
				otherfile.write(str(comment.id) + "\n")
		#If the post wants a flair and it's me or Klok:
		if "flair info" in str(comment.body).lower():
			if str(comment.author).lower() == "thomas1672" or str(comment.author).lower() == "klokinator":
				flairsubmtoset = r.get_submission(submission_id=str(comment.parent_id)[-6:])
				#Flair and stop duplicate flairing (would only waste processor time)
				flairsubmtoset.set_flair("INFO", "info")
				otherfile.write(str(comment.id) + "\n")
		if "flair question" in str(comment.body).lower():
			if str(comment.author).lower() == "thomas1672" or str(comment.author).lower() == "klokinator":
				flairsubmtoset = r.get_submission(submission_id=str(comment.parent_id)[-6:])
				flairsubmtoset.set_flair("QUESTION", "question")
				otherfile.write(str(comment.id) + "\n")
#Re-Save the file.
otherfile.close()
