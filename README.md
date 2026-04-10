# Spotify_Widget 
a simple spotify widget I made for class, but will use for streaming purposes. 

## BETA 
### what's left? 
- Need to package into app
- add creditional middle man
- 
<br>
## Setup 
--- WARNING --- 
this setup is only for those who know IDEs, basic software, and 

### 1. Create Spotify App
before you go down this rabbit hole
> when the dashboard calls for a callback, use:  *http://127.0.0.1:8888/callback*<br>
<br>
if you dont know how to do this go [here]([https://www.example.com](https://developer.spotify.com/documentation/web-api))
<br>
### 2. Add code into your system 
1. create a folder *REMEMBER WHERE*
2. download the zip file from MAIN.
3. extract the folder into your new folder
<br>
### 3. Configuring ENV file 
1. locate your spotify **client_id** and **secret_id** from your *spotify for developer dashboard*
2. locate your ENV text file and copy and paste these ids into the file

>the file should look like this: <br>
>`SPOTIFY_CLIENT_ID=`<br>
>`SPOTIFY_CLIENT_SECRET=`<br>

3. save and close the ENV file
<br>
### 4. run the Virtual Environment and widget
if you do not have git bash, powershell should work
* If you have git bash * 
> 1. cd into folder
> 2. run: `source .\venv\Scripts\activate`
> 3. then run: `python spotify_widget`
<br>
## Notes
1. It is a simple widget
2. it does not have an apk or win app wrapper *yet*
3. if you know how to program in C it is very customizable.
4. I might plan on making a second window that helps with customization
5. ...

