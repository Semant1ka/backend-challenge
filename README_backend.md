## Backend challenge project structure

- app.py - entry point for the app
- configuration.py - contains setup script for Db
- service.py - contains API implementation
- settings.py - contains settings for the Flask app
- test.py - contains tests (your Captain Obvious)

## How to run backend challenge

### Run with docker

In project folder run 

```
$ sudo dockebuild -t service .
$ sudo docker run -p 4000:5000 service
```

Send requests to http://0.0.0.0:4000/

### Run from command line

```
python3 app.py
```

Send requests to http://0.0.0.0:5000/

Flask app runs on default port (5000)