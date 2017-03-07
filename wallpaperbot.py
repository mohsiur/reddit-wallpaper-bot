import re, praw, requests, os, glob, sys, urllib
from bs4 import BeautifulSoup

MIN_KARMA = 250 #default minimum reddit karma

# Running the script with arguments

arg_len = len(sys.argv)
filters = 0 # 0 = hot 1 = all 2 = By year 3 = By month 4 = week 5 = day 6 = hour
albumLink = "http://imgur.com/a/"
imageLink = "http://i.imgur.com/"
normLink  = "http://imgur.com/gallery/"
imageURLPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')
subreddit_list = []

if arg_len < 2: 
	# No argument passed, download from default subreddits
	subreddit_list = ['earthporn']
elif arg_len >=2:
	subreddit_list.append(sys.argv[1])
	if arg_len ==3:
		filters = int(sys.argv[2])
	elif arg_len > 3:
		MIN_KARMA = int(sys.argv[3])

def downloadImage(imageUrl, localFile, subreddit):
	response = requests.get(imageUrl, stream = True)
	dirname = '%s/'%(subreddit)
	localFile = dirname+localFile
	if response.status_code == 200:
		print('Downloading %s to %s....'%(localFile, subreddit))
		try:
			os.makedirs(dirname)
		except OSError:
			if os.path.isdir(dirname):
				with open(localFile, 'wb') as f:
					for chunk in response.iter_content(4096):
						f.write(chunk)
			else:
				print ("Error")	

# Connect to reddit
user_agent = "Reddit Image Downloads 1.0 by /u/banglatoker"
clientId = '4IhD1FlhQfN9Uw'
clientSecret = 'vCZ2NuJfBaWpwqcJV89IPBbrUz0'
r = praw.Reddit(client_id = clientId,
		client_secret = clientSecret,
		user_agent=user_agent)

# going through subreddits
# Only looking at top 25 results from a week
for subreddits in subreddit_list:
	if filters == 0: 
		submissions = r.subreddit(subreddits).hot()
	elif filters == 1: 
		submissions = r.subreddit(subreddits).top('all')
	elif filters == 2:
		submissions = r.subreddit(subreddits).top('year')
	elif filters == 3:
		submissions = r.subreddit(subreddits).top('month')
	elif filters == 4:
		submissions = r.subreddit(subreddits).top('week')
	elif filters == 5:
		submissions = r.subreddit(subreddits).top('day')
	
	elif filters == 6:
		submissions = r.subreddit(subreddits).top('hour')

	for wallpaper in submissions:
		# Checking if conditions are met
		if "imgur.com/" not in wallpaper.url:
			continue
		if wallpaper.score < MIN_KARMA:
			continue
		if len(glob.glob('reddit_%s_%s_*'%(subreddits, wallpaper.id))) > 0:
			continue
		
		if albumLink in wallpaper.url:
			albumID = wallpaper.url[len(albumLink):]
			htmlSource = requests.get(wallpaper.url).text
			#Parsing Data
			soup = BeautifulSoup(htmlSource)
			matches = soup.select('.post-image-placeholder img')
			for match in matches:
				imageUrl = match['src']
				imageFile = imageUrl[imageUrl.rfind('/') +1:]
				localFile = 'reddit%s_%s_album_%s_imgur_%s'%(subreddits, wallpaper.id, albumID, imageFile)
				downloadImage(imageUrl, localFile, subreddits)

		elif imageLink in wallpaper.url:
			mo = imageURLPattern.search(wallpaper.url)
			imageFile = mo.group(2)
			localFile = 'reddit%s_%s_album_None_imgur_%s'%(subreddits, wallpaper.id, imageFile)
			downloadImage(wallpaper.url, localFile, subreddits)

		elif normLink in wallpaper.url:
			htmlSource = requests.get(wallpaper.url).text
			soup = BeautifulSoup(htmlSource)
			matches = soup.select('.post-image-placeholder img')
			for match in matches:
				imageUrl = match['src']
				imageFile = imageUrl[imageUrl.rfind('/') + 1:]
			localFile = 'reddit%s_%s_album_None_imgur_%s'%(subreddits, wallpaper.id, imageFile)
			downloadImage(wallpaper.url, localFile, subreddits)
