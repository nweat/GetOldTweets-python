# -*- coding: utf-8 -*-
import sys,getopt,got,datetime,codecs,csv,time,sqlite3
from dateutil.relativedelta import relativedelta

def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except sqlite3.Error as er:
		print(er)
 
	return None


def create_tweet(conn, table, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10):
	sql = '''INSERT INTO ''' + table + '''_tweets VALUES(?,?,?,?,?,?,?,?,?,?)'''

	try:
		cur = conn.cursor()
		val = cur.execute(sql,(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10))
		conn.commit()
	except sqlite3.Error as er:
		print(er)


def patientDetails():
	print "to be implemented"
	print "use tweepy to get user details, label if advocate keyword in description, label if anxiety mentioned, label if specific bipolar 1 or 2"


def getMultipleUsersTweets(ipatients, tweetCriteria, conn):

	for usr in ipatients:
		usrnme = usr['username']
		diagnosis_date = datetime.datetime.strptime(usr['date_of_diagnosis'], '%d/%m/%Y %H:%M')
		tweetCriteria.username = usrnme
		since = diagnosis_date - relativedelta(years=2)
		until = diagnosis_date + relativedelta(years=2)
		tweetCriteria.since = since.strftime('%Y-%m-%d')
		tweetCriteria.until = until.strftime('%Y-%m-%d')

		print '\nRetrieving tweets from %s to %s for %s (Diagnosis made: %s)' % (since, until, usrnme, diagnosis_date)
		
		def receiveBuffer(tweets):
			for t in tweets:
				#print "%s %s %s\n" % (t.username, t.date.strftime("%Y-%m-%d %H:%M:%S"), t.text)
				#print t.username
				create_tweet(conn, tweetCriteria.illness, t.username, t.date.strftime("%Y-%m-%d %H:%M:%S"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)
				
			print 'More %d tweets saved in database...\n' % len(tweets)
			time.sleep(3)
 
		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
		print "Sleeping for 5 seconds..."
		time.sleep(5)
		continue

	print 'Done. Tweets saved. See table: %s_tweets \n' % tweetCriteria.illness
	conn.close()
		


def main(argv):

	if len(argv) == 0:
		print 'You must pass some parameters. Use \"-h\" to help.'
		return
		
	if len(argv) == 1 and argv[0] == '-h':
		print """\nTo use this jar, you can pass the folowing attributes:
	username: Username of a specific twitter account (without @)
	   since: The lower bound date (yyyy-mm-aa)
	   until: The upper bound date (yyyy-mm-aa)
 querysearch: A query text to be matched
   maxtweets: The maximum number of tweets to retrieve

 \nExamples:
 # Example 1 - Get tweets by username [barackobama]
 python Exporter.py --username "barackobama" --maxtweets 1\n

 # Example 2 - Get tweets by query search [europe refugees]
 python Exporter.py --querysearch "europe refugees" --maxtweets 1\n

 # Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
 python Exporter.py --username "barackobama" --since 2015-09-10 --until 2015-09-12 --maxtweets 1\n
 
 # Example 4 - Get the last 10 top tweets by username
 python Exporter.py --username "barackobama" --maxtweets 10 --toptweets\n"""
		return
 
	try:
		userlist = ''
		opts, args = getopt.getopt(argv, "", ("other=","illness=", "userList=", "username=", "since=", "until=", "querysearch=", "toptweets", "maxtweets="))
		
		tweetCriteria = got.manager.TweetCriteria()
		
		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg
				
			elif opt == '--since':
				tweetCriteria.since = arg
				
			elif opt == '--until':
				tweetCriteria.until = arg
				
			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg
				
			elif opt == '--toptweets':
				tweetCriteria.topTweets = True
				
			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)

			elif opt == '--userList':
				userlist = arg

			elif opt == '--illness':
				tweetCriteria.illness = arg
				
        # get tweets for multiple users from file or run default functionality
		if userlist != '':
			inputFile = codecs.open(userlist, "r", "utf-8")
			ipatients = got.manager.TweetManager.extractPatients(inputFile)
			conn = create_connection('data/sqlite/patient_tweets_GetoldTweets.sqlite')
			getMultipleUsersTweets(ipatients, tweetCriteria, conn)
		else:
			outputFile = codecs.open("output_got.csv", "w+", "utf-8")
			outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
			print 'Searching...\n'
			
			def receiveBuffer(tweets):
				for t in tweets:
					outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
				outputFile.flush();
				print 'More %d saved on file...\n' % len(tweets)
				time.sleep(5)
			
			got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	except arg:
		print 'Arguments parser error, try -h' + arg
	finally:
		print 'Goodbye!'
		

if __name__ == '__main__':
	main(sys.argv[1:])