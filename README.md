# SUAS-Competition

This is Flint Hill School's code for the Student Unmanned Aerial Systems competition.

---

## License Information
Copyright 2017 Vale Tolpegin, Peter Hussisian, James Villemarette.

Licensed under the MIT License.

---

## Installation

This section details how to install the necessary libraries in order to run our code.

### Installing OpenCV -- Mac OS X

OpenCV must be installed for this project to work. To install OpenCV's latest release, use Homebrew:

```
brew install opencv3 --with-tbb --with-cuda --with-contrib
```

This is a long process. After it is completed, you will have to link the python libraries. Find the generated ```cv2.so``` file, then copy it. Next, identify your local python instance's site-packages repository. Finally, copy the ```cv2.so``` file into the site-packages directory.

To test the installation, simply enter a quick command into terminal

```
python -c 'import cv2; print(cv2.__version__)'
```

This should print something like ```3.1.0```. If you get an error, that means that you did not install OpenCV correctly.

### Installing Other Dependencies

All libraries except SimpleWebSocketServer will install when you run ```bash ./install.sh```. To install SimpleWebSocketServer, clone https://github.com/FlintHill/simple-websocket-server and run a pip install command.

---

## Usage

This section details how to

### Using MAVProxy

To run MAVProxy, find the ID of the radio module (run ```ls /dev/``` and find the name of the ```usbserial``` device corresponding to the radio module) and then run the following command:

```
sudo python mavproxy.py --console --master=/dev/tty.usbserial-DEVICE_ID --out=tcpin:127.0.0.1:14551 --out=tcpin:0.0.0.0:14550
```

Assuming the ```python``` command references a Python 2.7.13 installation

### Using GCS

To run the Client script, cd into the ```gcs``` directory, then run:

```
export FLASK_APP=flask_gcs.py
python -m flask run --with-threads
```

Ensure that the version of Python that you are using is 2.7.x. If you attempt to use Python 3, the program will crash with a timeout exception.

---

## Git Cheatsheet

This is a quick cheatsheet for those that are new to git in the command line. Each bullet point below explains a different command in git.

- **Clone a repository**
 - ```git clone https://github.com/user_name/SUAS-Competition.git``` : This command will clone a remote git repository locally in the current directory
- **Help**
 - ```git remote add suas https://github.com/FlintHill/SUAS-Competition``` : This will add a remote repository to the local git repository, allowing you to pull/push to a different remote
- **Rebase your Local Repository**
 - ```git pull --rebase origin master``` : This will update your local repository with the origin's master branch. If you want to update your local repository from the official repository, run ```git pull --rebase suas master```. This will pull the master branch from the ```suas``` remote repository. These commands should be run after every time you commit, and before you make changes to your local code
- **Track (add) your changes**
 - ```git add --all``` : This command will make all changes in a local git repository tracked. This command must be executed before you attempt to commit your code
- **Commit your changes**
 - ```git commit -m "MESSAGE"``` : This command will commit your code with the commit message "MESSAGE". Please change the message to match what changes you made in the code during this commit
- **Send your changes to GitHub**
 - ```git push``` : This command will push your local changes to the ```origin``` remote repository
