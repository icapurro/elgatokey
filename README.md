# Elgato Key Light Air Automation on Mac OS Sonoma

Project based on https://github.com/akburg/elgatokeylight and adapted to work on Mac OS 14.X (Sonoma). 

Automate Elgato Key Light Air to switch on automatically when you join a Google Meet or Zoom call (or any app that in-fact uses a camera stream on a Mac OS) and switches it off when the stream ends.


## Monitoring camera stream on Mac OS 14.x (Sonoma)

`log stream --predicate 'subsystem == "com.apple.controlcenter" and composedMessage contains "Sorted active attributions from SystemStatus update:"'`

essentially monitors the stream log on Mac OS and filters out any sensor indicator changes in where:
* A `[cam]` string is present in the log line, the lights should be **ON**
* A `[cam]` is not  present in the log line, the lighs should be **OFF**

## Turning the Engato Key Light Air On and Off

`curl --location --request PUT 'http://<light IP address>:9123/elgato/lights' --header 'Content-Type: application/json' --data-raw '{"lights":[{"brightness":40,"temperature":162,"on":1}],"numberOfLights":1}'` 
  
credit: https://vninja.net/2020/12/04/automating-elgato-key-lights-from-touch-bar/

You need to change the local IP addresses of the lights based on your local setup in the script. The rest of the key/value pairs to configure the light are self-expalantory.

## Running the script and testing if everything works

You can run the script using Terminal, download the .sh file, edit it and run:

`python autolights.py`

and this will start to monitor your stream log.  Open any app that uses your web camera, maybe **Photo Booth** and see if your light(s) come on.  If they do not, check that you have entered the correct IP address for your light(s).  Easiest way to identify the IP address is to use the **Elgato Control Center** utility > **Key light settings** > and note the IP address for each light.

## AutoLights Setup Instructions

AutoLights can be set up to run automatically every time you start your Mac. Follow these steps to create an Automator app that will start the AutoLights script at login.

### Step 1: Creating an Automator App

1. **Open Automator**:
   - Find Automator in your Applications folder or search for it using Spotlight (`Cmd + Space` and type "Automator").

2. **Create a New Automator App**:
   - In Automator, select `File > New`.
   - Choose `Application` as the type of your document.

3. **Add a "Run Shell Script" Action**:
   - In the library of actions on the left, search for “Run Shell Script.”
   - Drag the “Run Shell Script” action to the workflow area on the right.

4. **Configure the Shell Script Action**:
   - In the shell script action box, replace the content with the following command: 
     ```bash
     python3 <path_to_your_autolights.py>
     ```
     Replace `<path_to_your_autolights.py>` with the actual path to your `autolights.py` script.

5. **Save Your Automator App**:
   - Go to `File > Save` and give your app a name, such as "AutoLightsApp."
   - Choose a location to save your app (e.g., Applications folder).

### Step 2: Adding the App to Login Items

1. **Open System Settings**:
   - Click on the Apple menu () at the top left corner of your screen and select `System Settings`.

2. **Navigate to Login Items**:
   - Go to `General > Login Items`.
   - This section allows you to manage apps that start automatically when you log in.

3. **Add Your Automator App**:
   - Click the `+` button to add a new item.
   - Navigate to where you saved your "AutoLightsApp" and select it to add to the list.

Now, every time you turn on your computer, the AutoLights script will automatically start and listen for your camera activity to manage the lights.

**Note**: Ensure that the path to `autolights.py` is correct and that Python 3 is installed on your Mac. The script requires Python 3 to run properly.
