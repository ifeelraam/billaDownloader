# BIlla Quality Telegram MULTI PLatform Media Downloader Bot

## Features:
- Download media from platforms like Instagram, Facebook, YouTube, Spotify, Gaana, JioSaavn, and TeraBox.
- Allows downloading private Instagram Reels, Stories, and Facebook videos with login.
- Users can choose between downloading video/audio and select the platform with quality options .

- SUPPORT GROUP CHAT : @BillaCore
- SUPPORT CHANNEL : @BillaSpace


   
Certainly! Here's a list of commands and features for the bot in the script you provided:

Command List and Description: 

/start

Description: Starts the bot and provides a welcome message with options for downloading media (either video or audio). How it works: When the user sends /start, they will receive a message with two options: "Download Video" and "Download Audio." 

Platform Selection (Inline Keyboard)

Description: After selecting either "Download Video" or "Download Audio," the user is presented with a list of platforms to choose from: Spotify Gaana JioSaavn Instagram Reels Instagram Story YouTube Facebook TeraBox How it works: The user clicks on one of these platform buttons, and the bot will guide the user to provide the corresponding media URL (e.g., a link to a Spotify song or a Facebook video). 

Login Commands for Instagram and Facebook:

Instagram Login:

Description: To download private Instagram Reels or Stories, the bot prompts the user to log in with their Instagram username and password. How it works: The user sends their Instagram username and password in the format: username password. After a successful login, they can download private Instagram media. 

Facebook Login:

Description: Similar to Instagram, this command allows the user to log in to Facebook with their credentials to download private Facebook media. How it works: The user sends their Facebook username and password in the format: username password. After a successful login, the bot will be able to download private Facebook videos. 

Media Download (Message Handling):

Description: After logging in to the appropriate platform (if required), the bot listens for a URL to download media from that platform. How it works: Once the user selects a platform (e.g., Spotify, Instagram Reels, YouTube), the bot asks the user to send a URL (e.g., a YouTube video URL or a Spotify song link). The bot will then download the media and provide a response. Example Flow: The user sends /start. The bot responds with an inline keyboard asking the user to choose between "Download Video" or "Download Audio." The user selects "Download Video." The bot responds with an inline keyboard to choose the platform, e.g., Spotify, YouTube, Instagram, Facebook, etc. The user selects a platform (e.g., "Instagram Reels"). If the platform requires a login (Instagram or Facebook), the bot will prompt the user to log in with their credentials. After logging in successfully (if applicable), the bot asks for the media URL (e.g., a link to a Spotify song or an Instagram reel). The user provides the URL. The bot processes the request, downloads the media, and replies with a success message or error message if something went wrong. Command List Summary: 

Let me know if you need any further clarification or additional features!





## Setup Locally In VPS or Termux {TERMUX ACQUIRES DEVICE STORAGE WHEN FILES ARE DOWNLOADED }:
1. Clone the repository:
   ```bash
   git clone https://github.com/ifeelraam/billaDownloader.git

2. install requirements to run the bot in your vps
 ```bash
pip install -r requirements.txt

3. vi config.env for  bot variables
press ctrl +c when done  &  :wq to save 

4. run the bot { if not works create virtual environmnt then run cmd} 
python3 bot.py
 Or
python bot.py

