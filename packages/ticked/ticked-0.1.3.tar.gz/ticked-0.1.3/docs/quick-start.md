# Setup Guide

# Installation

### Windows

I've found the best terminals for this are WezTerm and Microsoft's Windows Terminal - `wt`

Python 3.8+ is required (grab the latest, if you are able to)

Install Tick using pip
   ```powershell
   pip install tick
   ```

### macOS/Linux
Users can install Tick through pip or ~~brew~~ (Brew access coming soon)
   ```bash
   pip install tick
   ```
   ```bash
   brew install tick
   ```
   (If you're using tap)
   ```bash
   brew tap cachebag/tick
   ```
macOS users can also utilize iTerm2's terminal window customization settings to achieve the look seen in these images where the window is transparent/blurred: 

<img src="./images/ss1.png" alt="Screenshot of Tick interface" width="800">
<img src="./images/ss2.png" alt="Screenshot of Tick interface" width="800">

#### I'm sure Linux users using environments like Hyprland can achieve a similar look.

# Theme Customization

### Default Themes
Tick comes with several built-in themes via Textual:
- textual-dark and light
- solarized light
- monokai
- tokyo-night
- gruvbox (Tick's default)
- nord
- dracula

and more...

To change your theme, you can toggle your main menu with `Esc` and head over to settings:

<img src="./images/ss4.png" alt="Screenshot of Tick interface" width="800">

<img src="./images/ss5.png" alt="Screenshot of Tick interface" width="800">



### Creating Custom Themes (NOT DONE)

# Keyboard Navigation

### Good to know Global Shortcuts
- `Ctrl+Q`: Quit application in any view
- `Esc`: Toggle the main menu
- `Tab`: Change focus between elements on any given page

In general, you can navigate the entire app with your arrow, esc and enter keys, except for specific pages where the functionality requires a more graceful approach to navigation, wherein the controls for those pages will show at the footer of the app. Look into the docs of each page for more information.

# Spotify Integration (Premium Users Only)

Currently, the app is listed as "Under Development" through the Spotify Developer dashboard. I can onboard up to 25 users and give them access to the API so that you can listen to your Spotify playlists and access other features within Tick.

 **Please note:** This is only available to Premium users. Spotify currently does not grant access to users using a free subscription plan.

Please email me at alhakimiakrmj@gmail.com or message me on discord: cachebag, if you would like access to Spotify within Tick. Note: You will need to provide access to the email that you you have access to premium on in order to use the API.

A request has already been submitted to Spotify for extended access to all users.

### Usage
- Once you have been added to my user list, you need to create a .env file in the root directory where ticked was installed (i.e. ```/installfolder/venv/bin/ticked```) 
- Log into the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and fill that .env file with the following information:
```
SPOTIFY_CLIENT_ID=client-id
SPOTIFY_CLIENT_SECRET=client-secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

```
- Head over to the Spotfify page on Ticked and click the Authenticate button on the bottom right. 

<img src="./images/ss6.png" alt="Screenshot of Tick interface" width="800">





<img src="./images/ss7.png" alt="Screenshot of Tick interface" width="800">


 Control playback from your home view

<img src="./images/ss8.png" alt="Screenshot of Tick interface" width="800">


# Troubleshooting
### Common issues and their solutions:
1. Authentication Failed
    - Please make sure you have a _premium_ account. Spotify API does not give access to free users.
    - Ensure you gave me the right email to ensure access is properly granted.

2. 403 Error - Playback issues
    - The way Spotify's API works, you need to have either Spotify open in a Web Browser, or open on your Desktop app in order to listen to the music. Once you've opened either of those, you can minimize Spotify and return to Tick and continue listening to Spotify.
    - You are also able to simply turn Spotify on from your phone and control it's features from Ticked itself.
    - Please make sure you have a _premium_ account. Spotify API does not give access to free users.

3. Connection Problems
    - You _do_ need an internet connection to access Spotify. There is no offline access. 

For additional support or questions, please don't hesitate to open an issue on the [GitHub](https://github.com/cachebag/Tick) or contact me directly.