# savify
Python script(s) to archive your Spotify Discover weekly's

## Info
This repo includes multiple files where the script functions differently depending on the use case. A short description per case will be provided below.
Note: "Discover Weekly" playlist no longer seem accessible through the Spotify API anymore, hence a decision was made to create scraping methods to solve this issue and then query for the song name + artist after that.

### savify_scheduler
This version was originally made to basically just run and execute the tasks using the schedule library. This is **not** suitable for if you don't plan on having the app running actively, use any other type of task scheduler or manually want to execute the tasks of archiving this weeks Discover Weekly.
