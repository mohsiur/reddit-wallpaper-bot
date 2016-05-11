import re, praw, requests, os, glob, sys, urllib
from bs4 import BeautifulSoup

MIN_KARMA = 500 #default minimum reddit karma

# Running the script with arguments

arg_len = len(sys.argv)
albumLink = "http://imgur.com/a/"
imageLink = "http://i.imgur.com/"
normLink  = "http://imgur.com/gallery/"
imageURLPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')

if arg_len < 2: 
	# No argument passed, download from default subreddits
	subreddit_list = ['earthporn']
elif arg_len >=2:
	subreddit_list.append(sys.argv[1])
	if arg_len >=3:
		MIN_KARMA = sys.argv[2]


def downloadImage(imageUrl, localFile):
	response = requests.get(imageUrl, stream = True)
	if response.status_code == 200:
		print('Downloading %s...'%(localFile))
		with open(localFile, 'wb') as f:
			for chunk in response.iter_content(4096):
				f.write(chunk)
			







# Connect to reddit
user_agent = "Reddit Image Downloads 1.0 by /u/banglatoker"
r = praw.Reddit(user_agent = user_agent)

# going through subreddits
# Only looking at top 25 results from a week
for subreddits in subreddit_list:
	submissions = r.get_subreddit(subreddits).get_top_from_week(limit = 20)
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
			downloadImage(wallpaper.url, localFile)

		elif imageLink in wallpaper.url:
			mo = imageURLPattern.search(wallpaper.url)
			imageFile = mo.group(2)
			localFile = 'reddit%s_%s_album_None_imgur_%s'%(subreddits, wallpaper.id, imageFile)
			downloadImage(wallpaper.url, localFile)

		elif normLink in wallpaper.url:
			htmlSource = requests.get(wallpaper.url).text
			soup = BeautifulSoup(htmlSource)
			matches = soup.select('.post-image-placeholder img')
			for match in matches:
				imageUrl = match['src']
				imageFile = imageUrl[imageUrl.rfind('/') + 1:]
			localFile = 'reddit%s_%s_album_None_imgur_%s'%(subreddits, wallpaper.id, imageFile)
			downloadImage(wallpaper.url, localFile)


