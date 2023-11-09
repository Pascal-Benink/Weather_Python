# Weather_python

## How to install
To install you need docker on your pc\
docker download:https://www.docker.com/products/docker-desktop/ \
Python 3.12 is needed \
if you meet all the requirements the procedure is the following 
1. download the code
2. open the code in your code editor (Visual studio code, Pycharm ect.)
3. use requirements.txt to install all packages using: pip install -r requirements. txt in the terminal
4. copy the .env.examle content and place it in a new file called .env
5. make a account at https://developer.accuweather.com/ and make a app then copy the api key and place it after API_KEY=
4. do the following command in your code editor terminal: docker compose up -d
5. and run the python script.

Now you have the script running and you can see if the weather is bikeble for you
you can also change the bikable parameters in config.json if you want to

## What is this app
This app is a checker to check if the weather is bikeable by you standards. you can change the parameters in the config.json.
The app uses the following api routes:
/locations/v1/cities/ipaddress to check if at the location of your ipaddress the weather is bikeable by your standards.
/currentconditions/v1/ to see if the water is bikeale at the location above

## Connections
you can connect to the api via:http://127.0.0.1:5000/
