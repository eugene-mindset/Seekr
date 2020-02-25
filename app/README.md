# Running the App

## Notes

- API server served on <http://localhost:5000>
- React default serves on <http://localhost:3000>
- Need to have npm, nodejs, python installed.
- You can make a virtual environment in the repo so long as it is called venv or env. Git will ignore those files.

## Front End (Node.js)

1. Open a new terminal and head to /app/seeker
2. Enter the command `npm start` (might need to run `npm install` to get all the packages if it doesnt work)

## API Server (Flask)

1. Open a new terminal and head to /app
2. Create a virtual environment if haven't. This would be `virtualenv -p python3 env`
3. Start up your virtual environment (windows is `.\env\Scripts\activate`, linux is  `source .\env\bin\activate`)
4. With the virtual environment activated, `pip3 install -r requirements.txt`
5. Enter the command `python app.py`

## Database (MongoDB)

### WINDOWS

1. Head to the location of your mongodb installation
2. Run 'mongo.exe' from the bin subfolder, found in the version subfolder of the 'server' subfolder

### MAC

1. Open terminal and head to /app
2. Enter the command `mongod --dbpath=./data/db/`
