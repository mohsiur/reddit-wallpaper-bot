import re, praw, requests, os, glob, sys, urllib

# Public variables
MIN_KARMA = 250 #default minimum reddit karma
filters = 0
subreddit_list = []
# Main function
def main(filters):
	arg_len = len(sys.argv)
	if arg_len < 2: 
		# No argument passed, download from default subreddits
		subreddit_list = ['earthporn']
	elif arg_len >=2:
		subreddit_list.append(sys.argv[1])
		if arg_len ==3:
			filters = int(sys.argv[2])
		elif arg_len > 3:
			MIN_KARMA = int(sys.argv[3])
	r = connectToReddit()
	submissions = getSubReddit(filters, r, subreddit_list)
	print(submissions)
	getWallpapers(submissions, subreddit_list)
	

def connectToReddit():
	user_agent = "Reddit Image Downloads 1.0 by /u/banglatoker"
	client_id = '4IhD1FlhQfN9Uw'
	client_secret = 'vCZ2NuJfBaWpwqcJV89IPBbrUz0'
	r = praw.Reddit(client_id = client_id,
			client_secret = client_secret,
			user_agent=user_agent)
	return r

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

# Return a collection of wallpapers meeting the filtered criteria
def getSubReddit(filters, r, subreddit_list):
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
	return submissions

# Only works for jpg
def getWallpapers(submissions, subreddits):
	for subreddit in subreddits:
		for wallpaper in submissions:
			if ".jpg" not in wallpaper.url:
				continue
			if wallpaper.score < MIN_KARMA:
				continue
			if glob.glob('reddit_%s_%s.jpg'%(subreddit, wallpaper.id)) > 0:
				print("Wallpaper already exists")
				continue
			imageUrl  = wallpaper.url
			imageID   = wallpaper.id
			localFile = 'reddit_%s_%s.jpg'%(subreddit, wallpaper.id)
			downloadImage(imageUrl, localFile, subreddit)

main(filters)
