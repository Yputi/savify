# savify
Python script(s) to archive your Spotify Discover weekly's

This repo includes multiple files where the script functions differently depending on the use case. A short description per case will be provided below.
Note: "Discover Weekly" playlist no longer seem accessible through the Spotify API anymore, hence a decision was made to create scraping methods to solve this issue and then query for the song name + artist after that.

## savify_scheduler
This version was originally made to basically just run and execute the tasks using the schedule library. This is **not** suitable for if you don't plan on having the app running actively, use any other type of task scheduler or manually want to execute the tasks of archiving this weeks Discover Weekly.
This version has only been tested locally.
- `pip install spotipy`
- `pip install python-dotenv`
- `pip install beautifulsoup4`
- `pip install schedule`

## savify_single
This version will perform the archiving task only once when starting the app. This is meant for when not running the app continuously, either starting it manually or through a different type of scheduler.

www.pythonanywhere.com can be used for this, even for free with the beginner tier - "A limited account with one web app at your-username.pythonanywhere.com".
Some general steps for getting this to work on pythonanywhere are:
- Download/copy savify_single.py first
- Create your .env file with all the required information from the Spotify Developer portal
- Run savify_single.py locally once first so it creates the .cache file for you (part of Spotipy). This also means you should make sure you have installed spotipy, dotenv, etc.
- Log in on pythonanywhere.com
- Go to the "Files" tab and create a new directory if you wish for savify
- upload savify_single.py, .env and .cache to this directory
- At the top of the page, click "Open Bash console here". Use this to install:
   - `pip install spotipy`
   - `pip install python-dotenv`
   - `pip install beautifulsoup4`
- Run the savify_single.py to confirm if it works. If that's done, you can create a task to run it on specific moments through the "Task" tab
