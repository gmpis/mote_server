# mote_server 
This is a server for controlling Mote led stick

## Installation  
`pip install -r requirements.txt`  
  
Note: *If you haven't already installed pip/pip3, you can do so by running: `sudo apt install python3-pip`*  

## Run the app  
`export FLASK_APP=m_web_mote.py`  
`flask run`

Now you can access the app using a web browser at http://127.0.0.1:5000/

####  Advanced  
`export FLASK_APP=m_web_mote.py`   
`export FLASK_RUN_PORT=5005`  
`export FLASK_ENV=development` 

`flask run --host=0.0.0.0 --port=5005`  

## OR run the app using gunicorn:   
`gunicorn -w 1 -b 127.0.0.1:5005 m_web_mote:app`
