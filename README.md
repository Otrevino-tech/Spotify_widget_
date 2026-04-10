# Spotify_Widget 
a simple spotify widget I made for class, but will use for streaming purposes. 

## BETA 
### what's left? 
- Need to package into app
- add creditional middle man
- 

## Setup 
--- WARNING --- 
this setup is only for those who know IDEs, basic software, and 

### 1. Create Spotify App
before you go down this rabbit hole
> when the dashboard calls for a callback, use:  *http://127.0.0.1:8888/callback*
if you dont know how to do this go [here]([https://www.example.com](https://developer.spotify.com/documentation/web-api))

### 2. Add code into your system 
1. create a folder *REMEMBER WHERE*
2. download the zip file from MAIN.
3. extract the folder into your new folder

### 3. Configuring ENV file 
1. locate your spotify **client_id** and **secret_id** from your *spotify for developer dashboard*
2. locate your ENV text file and copy and paste these ids into the file
the file should look like this: 
>`SPOTIFY_CLIENT_ID=`\n
>`SPOTIFY_CLIENT_SECRET=`

if you do not have git bash, powershell should work

### 4. run the Virtual Environment and widget
* If you have git bash * 
> 1. cd into folder
> 2. run: `source .\venv\Scripts\activate`
> 3. then run: `python spotify_widget`
## Notes
1. 
