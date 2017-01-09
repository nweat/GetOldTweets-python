# -*- coding: utf-8 -*-

import sys,getopt,got,datetime,codecs,csv,time

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
		illness = ''
		opts, args = getopt.getopt(argv, "", ("illness=", "patients=", "username=", "since=", "until=", "querysearch=", "toptweets", "maxtweets="))
		
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

			elif opt == '--patients':
				tweetCriteria.patients = arg

			elif opt == '--illness':
				illness = arg
				
		
		inputFile = codecs.open(tweetCriteria.patients, "r", "utf-8")
		ipatients = got.manager.TweetManager.extractPatients(inputFile)
		#python Exporter.py --illness depression_comorbid --patients data/depression_comorbid/depression_comorbid.csv --maxtweets 4000

		for usr in ipatients:
			usrnme = usr['username'][1:-1]
			outputFile = codecs.open("data/"+illness+"/"+usrnme+".csv", "w+", "utf-8")
			outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
			tweetCriteria.username = usrnme
			
			print '\nGetting tweets for - %s' % usrnme
			
			def receiveBuffer(tweets):
				for t in tweets:
					outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M:%S"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
				outputFile.flush();
				print 'More %d saved on file...\n' % len(tweets)
			
			got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

			outputFile.close()
			print 'Done. Output file generated %s.csv \n' % usrnme
			print '30 second sleep..\n'
			time.sleep(30)
			continue


	except arg:
		print 'Arguments parser error, try -h' + arg
	finally:
		print 'Done. Goodbye!'
		

if __name__ == '__main__':
	main(sys.argv[1:])