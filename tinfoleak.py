#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import tweepy
import sys
import getopt
import datetime

# OAuth Settings
# How to obtain the API key:
# Go to https://dev.twitter.com/apps/new
# Copy the consumer key (API key), consumer secret, access token and access token secret
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# App parameters (please, don't modify these values!)
program_name = "tinfoleak"
program_version = "v0.9"
program_date = "09/11/2013"

# Global parameters
arg_name = "" # twitter account
arg_count = 100 # number of tweets to be analyzed
arg_time = 0 # 1 = show the time in the results, 0 = don't show the time in the results
arg_basic = 0 # 1 = show basic info for the user, 0 = don't show basic info for the user
arg_source = 0 # 1 = show the application used by the user, 0 = don't show the application used by the user
arg_hashtags = 0 # 1 = show the hashtags, 0 = don't show the hashtags
arg_mentions = 0 # 1 = show the user mentions, 0 = don't show the user mentions
arg_find = "" # word to search in the user timeline
arg_geo = 0 # 1 = show the geolocation info, 0 = don't show the geolocation info
arg_stime = "00:00:00" # start time (filter)
arg_etime = "23:59:59" # end time (filter)
arg_sdate = "1900/01/01" # start date (filter)
arg_edate = "2100/01/01" # end date (filter)
source = [] # store the applications (twitter client)
hashtags = [] # store the hashtags
user_mentions = [] # store the user mentions
tweet_with_word = [] # store the tweets filtered by the specified word
geo_info = [] # store the geolocation info
sdate = datetime.datetime.now() # the current date and time
color = "[1;96m" # color used in the headers


################
# Show credits
################
def show_credits():
	try:
		print "+++ "
		print "+++ " + program_name + " " + program_version + " - \"Get detailed information about a Twitter user\""
		print "+++ Vicente Aguilera Diaz. @vaguileradiaz"
		print "+++ Internet Security Auditors"
		print "+++ " + program_date
		print "+++ " 
		print

	except Exception, e:
		print "[ show_credits() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# Show usage
################
def show_usage():
	print "Usage:\n# " + sys.argv[0] + " [-n|--name] username [-c|--count] count [-t|--time] [-b|--basic] [-s|--source] [-h|--hashtags] [-m|--mentions] [-g|--geo] [--stime] stime [--etime] etime [--sdate] sdate [--edate] edate [-f|--find] word "
	print "\t(*) username: Twitter account"
	print "\t    count: number of tweets to analyze (default value: 100)"
	print "\t    time: show time in every result (default value: off)"
	print "\t(+) basic: show basic information about the username (default value: off)"
	print "\t(+) source: show applications used by username (default value: off)"
	print "\t(+) hashtags: show hashtags used by username (default value: off)"
	print "\t(+) mentions: show twitter accounts used by username (default value: off)"
	print "\t(+) geo: show geo information in every result (default value: off)"
	print "\t    stime: filter tweets from this start time. Format: HH:MM:SS (default value: 00:00:00)"
	print "\t    etime: filter tweets from this end time. Format: HH:MM:SS (default value: 23:59:59)"
	print "\t    sdate: filter tweets from this start date. Format: YYYY/MM/DD (default value: 1900/01/01)"
	print "\t    edate: filter tweets from this end date. Format: YYYY/MM/DD (default value: 2100/01/01)"
	print "\t(+) word: filter tweets that include this word"
	print 
	print "\t(*) Required parameter"
	print "\t(+) One of these parameters must be informed"
	print "\n\tExamples:"
	print "\t\t# " + sys.argv[0] + " -n vaguileradiaz -b"
	print "\t\t# " + sys.argv[0] + " -n stevewoz -c 10 -g"
	print "\t\t# " + sys.argv[0] + " -n vaguileradiaz -t -h -m"
	print "\t\t# " + sys.argv[0] + " -n vaguileradiaz -t -c 500 -f secret"
	print "\t\t# " + sys.argv[0] + " -n vaguileradiaz -s -h -m -c 1000 -stime 08:00:00 -etime 18:00:00\n"


################
# Get options
################
def get_options():
	global arg_name
	global arg_count
	global arg_time
	global arg_basic
	global arg_source
	global arg_hashtags
	global arg_mentions
	global arg_geo
	global arg_find
	global arg_stime
	global arg_etime
	global arg_sdate
	global arg_edate

	try:
		opts, args = getopt.getopt(sys.argv[1:], "n:c:tbshmgf:", ["name=","count=","time","basic","source","hashtags","mentions","geo","find=","stime=","etime=", "sdate=","edate="])
		for o, a in opts:
			if o in ("-n", "--name"):
				arg_name = a
			elif o in ("-c", "--count"):
				arg_count = a
			elif o in ("-t", "--time"):
				arg_time = 1
			elif o in ("-b", "--basic"):
				arg_basic = 1
			elif o in ("-s", "--source"):
				arg_source = 1
			elif o in ("-h", "--hashtags"):
				arg_hashtags = 1
			elif o in ("-m", "--mentions"):
				arg_mentions = 1
			elif o in ("-g", "--geo"):
				arg_geo = 1
			elif o in ("-f", "--find"):
				arg_find = a
			elif o in ("--stime"):
				arg_stime = a
			elif o in ("--etime"):
				arg_etime = a
			elif o in ("--sdate"):
				arg_sdate = a
			elif o in ("--edate"):
				arg_edate = a
	except:
		if str(sys.exc_info()[1]) != '1':
			print "[get_options] Unexpected error:", sys.exc_info()[1]
		show_usage()
		sys.exit(1)

################
# Show final message
################
def show_final_message():
	try:
		tdelta = datetime.datetime.now() - sdate
		hours, remainder = divmod(tdelta.seconds, 3600)
		minutes, seconds = divmod(remainder, 60)
		print "\tElapsed time: %02d:%02d:%02d" % (hours, minutes, seconds)	
		print " "
		print "See you soon!"
		print " "
		sys.exit(0)

	except Exception, e:
		print "[ show_final_message() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# User authentication
################
def user_auth():
	try:
		global user
		global auth
		global api
		# User authentication
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

		# Tweepy (a Python library for accessing the Twitter API)
		api = tweepy.API(auth)
		user = api.get_user(arg_name)

	except Exception, e:
		print "[ user_auth() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# Get basic info for twitter user name
################
def get_basic_info():
	try:
		print chr(27) + color + "\tAccount info" + chr(27) + "[0m"
		print "\t-------------------"
		print "\tScreen Name:\t\t ", user.screen_name
		print "\tUser name:\t\t ", user.name
		print "\tTwitter Unique ID:\t ", user.id
		print "\tAccount created at:\t ", user.created_at.strftime('%m/%d/%Y')
		print "\tFollowers:\t\t ", user.followers_count
		print "\tTweets:\t\t\t ", user.statuses_count
		print "\tLocation:\t\t ", user.location
		print "\tDescription:\t\t ", user.description
		print "\tURL:\t\t\t ", user.url
		print "\tProfile image URL:\t ", user.profile_image_url
		print " "

	except Exception, e:
		print "[ basic_info() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# Get source
################
def get_source(tweet_source, tweet_created_at):
	try:
		add = 1
		for index, item in enumerate(source):
			if tweet_source == item[0]:
				add = 0	
		if add:
			source.append([tweet_source, str(tweet_created_at.strftime('%m/%d/%Y')), str(tweet_created_at.time())])

	except Exception, e:
		print "[ get_source() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# Get hashtags user mentions
################
def get_hashtags_user_mentions(request, name, tag, tweet_info, tweet_created_at):
	try:
		tmp = ""
		for i in tweet_info:
			if i[name].encode('utf-8'):
				tmp = tmp + tag + i[name].encode('utf-8') + " "
		if len(tmp):
			if not [tmp, tweet_created_at.strftime('%m/%d/%Y'), tweet_created_at.time()] in request:
				if arg_time:
					request.append([tmp, tweet_created_at.strftime('%m/%d/%Y'), tweet_created_at.time()])
				else:
					add = 1
					for m in request:
						if tmp.lower() in m[0].lower(): 
							add = 0
					if add:
						request.append([tmp, tweet_created_at.strftime('%m/%d/%Y'), tweet_created_at.time()])

	except Exception, e:
		print "[ get_hashtags_user_mentions() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# Get geo info
################
def get_geo_info(tweet_place, tweet_geo, tweet_created_at):
	try:
		splace = ""
		sgeo = ""
		add = 0
		if tweet_place:
			splace = tweet_place.name.encode('utf-8')
			add = 1
		if tweet_geo:
			sgeo = tweet_geo['coordinates']
			add = 1
		if add:
			sinfo = splace + " " + str(sgeo)
			geo_info.append([sinfo, str(tweet_created_at.strftime('%m/%d/%Y')), str(tweet_created_at.time())])

	except Exception, e:
		print "[ get_geo_info() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# Get tweets with word
################
def get_tweets_with_word(tweet_text, tweet_created_at):
	try:
		if arg_find.lower() in tweet_text.lower():
			tweet_with_word.append([tweet_text, str(tweet_created_at.strftime('%m/%d/%Y')), str(tweet_created_at.time())])

	except Exception, e:
		print "[ get_tweets_with_word() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# Is valid
################
def is_valid(tweet):
	try:
		valid = 1
		time = str(tweet.created_at.time())
		if time < arg_stime or time > arg_etime:
			valid = 0

		date = str(tweet.created_at.strftime('%Y/%m/%d'))
		if date < arg_sdate or date > arg_edate:
			valid = 0

		return valid

	except Exception, e:
		print "[ is_valid() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# Get detail info for twitter user name
################
def get_details():
	try:
		page = 1
		tweets = 0
		while True:
			timeline = api.user_timeline(screen_name=user.screen_name, include_rts=True, count=arg_count, page=page)
			if timeline:
				for tweet in timeline:
					tweets += 1
					if is_valid(tweet):
						if arg_source:
							get_source(tweet.source.encode('utf-8'), tweet.created_at)
						if arg_hashtags:
							get_hashtags_user_mentions(hashtags, 'text', '#', tweet.entities['hashtags'], tweet.created_at)
						if arg_mentions:				
							get_hashtags_user_mentions(user_mentions, 'screen_name', '@', tweet.entities['user_mentions'], tweet.created_at)
						if arg_geo:				
							get_geo_info(tweet.place, tweet.geo, tweet.created_at)
						if arg_find:
							get_tweets_with_word(tweet.text.encode('utf-8'), tweet.created_at)
					sys.stdout.write("\r\t" + str(tweets) + " tweets analyzed")
					sys.stdout.flush()										
					if tweets >= int(arg_count):
						break
			else:
				break
			page += 1
			if tweets >= int(arg_count):
				break
		print 
	except Exception, e:
		print "[ get_details() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# Show tweet info
################
def show_tweet_info(tweet_info, header):
	try:
		print
		if arg_time:
			print chr(27) + color + "\tDate         Time       " + header + chr(27) + "[0m"
		else:
			print chr(27) + color + "\tDate         " + header + chr(27) + "[0m"
		print "\t------------------------------------"
		c = 0
		for i in tweet_info:
			if arg_time:
				print "\t" + str(i[1]) + " - " + str(i[2]) + " - " + str(i[0])
			else:
				print "\t" + str(i[1]) + " - " + str(i[0])
			c = c + 1
		print "\n\t" + str(c) + " results."
		print " "

	except Exception, e:
		print "[ show_tweet_info() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

################
# Main function
################
def main():
	try:
		show_credits()
		get_options()

		if arg_name == "" :
			show_usage()
		else:
			if arg_basic or arg_source or arg_hashtags or arg_mentions or arg_find or arg_geo:
				user_auth()
				if arg_basic:
					get_basic_info()
				if arg_source or arg_hashtags or arg_mentions or arg_find or arg_geo:
					get_details()
				if arg_source:
					show_tweet_info(source, "Source")
				if arg_hashtags:
					show_tweet_info(hashtags, "Hashtags")
				if arg_mentions:
					show_tweet_info(user_mentions, "User mentions")
				if arg_geo:
					show_tweet_info(geo_info, "Geolocation information")
				if arg_find:
					show_tweet_info(tweet_with_word, "Word [" + arg_find + "]")
			else:
				show_usage()

		show_final_message()

	except Exception, e:
		print "[ main() Error]\n\tError message:\t " + e.message[0]['message'] + "\n\tError code:\t " + str(e.message[0]['code']) + "\n"
		sys.exit(1)

main()

