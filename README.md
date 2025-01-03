# savify
Python script(s) to archive your Spotify Discover weekly's

![image](https://github.com/user-attachments/assets/bfd5a88c-24de-4aca-922d-0838d35475cf)


This repo includes multiple files where the script functions differently depending on the use case. A short description per case will be provided below.
Note: "Discover Weekly" playlist no longer seem accessible through the Spotify API anymore, hence a decision was made to create scraping methods to solve this issue and then query for the song name + artist after that.

Tip: As each week a new playlist will be created, it could be useful to create a "folder" in spotify to place these in. The moving to the folder would have to be done manually due to this not being possible through Spotify's API.
The benefit of this is that it will allow you to play all playlists as if it's a single playlist while keeping it organized.

![image](https://github.com/user-attachments/assets/b7941706-67cd-4d25-9edd-9bc6830912bb)


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

Alternatively you could also create a scheduled task on your own PC:
https://learn.microsoft.com/en-us/windows/win32/taskschd/starting-an-executable-weekly
It's recommended to:
- Create a .bat file to execute the savify_single.py file, which you can then refer to in your action for the scheduled task
- Set the "Start in (optional)" to the directory your savify_single.py is located
- Set the weekly trigger on Monday, but consider putting the time a few hours after 00:00 incase of delays or it being updated for you differently
- Enable "Run task as soon as possible after a scheduled start is missed" so it will just start whenever you log in starting from that set schedule
