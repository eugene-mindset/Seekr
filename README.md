# Seekr: JHU OOSE PROJECT SPRING 2020
[![Build status](https://travis-ci.com/jhu-oose/2020-spring-group-Seekr.svg?token=Vxy2zEXxUQmZnx9hqykp&branch=master)](https://travis-ci.com/jhu-oose/2020-spring-group-Seekr)

# Deployed At:
http://ec2-54-83-146-52.compute-1.amazonaws.com/

# Running the App

## Notes

- API server served on <http://localhost:5000>
- React default serves on <http://localhost:3000>
- Nodejs version 13.9.0
- Python version 3.7.5
- Need to have npm, nodejs, python installed.
- You can make a virtual environment in the repo so long as it is called venv or env. Git will ignore those files.

## Front End (ReactJS)

1. Open a new terminal and head to /app/seeker
2. Enter the command `npm install` to get the correct node modules and packages needed to run the front end.
3. Enter the command `npm start` 


## API Server (Flask)

1. Create a virtual environment if haven't. This would be `virtualenv -p python3 env`
2. Start up your virtual environment (windows is `.\env\Scripts\activate`, linux is  `source .\env\bin\activate`)
3. With the virtual environment activated, `pip3 install -r requirements.txt`
4. run start_server.sh

## Database (MongoDB)

### WINDOWS

1. Head to the location of your mongodb installation
2. Run 'mongo.exe' from the bin subfolder, found in the version subfolder of the 'server' subfolder

### MAC

1. Open terminal and head to /app
2. Enter the command `mongod --dbpath=./data/db/`

## Deployment (AWS)
1. ssh -i /path/to/your/seekr.pem ubuntu@ec2-54-83-146-52.compute-1.amazonaws.com
2. cd (into project folder)
3. git pull (currently due to hot reloading from being in dev mode)
4. tmux a (to open up the background terminals running the app, use tmux commands)
