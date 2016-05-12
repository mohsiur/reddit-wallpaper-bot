# reddit-wallpaper-bot
A Reddit bot to download wallpapers/images from various subreddits

## Usage

#### Clone repository

`git clone http://github.com/mohsiur/reddit-wallpaper-bot.git`

#### In Terminal run the following script

`python wallpaperbot.py [subreddit] [filters] [MIN_KARMA]`

#### Filters
* 0 = Hot (Default)
* 1 = All 
* 2 = Year
* 3 = Month
* 4 = Week
* 5 = Day
* 6 = Hour

If no arguments passed default is downloads hottest 100 with 250+ Karma from /r/earthporn

#### Features to be added
* A text file containing filters, subreddits ad karma values so that only the file needs to be updated and not the code
* Schedule with cron
* Make a GUI
* Clean up code
