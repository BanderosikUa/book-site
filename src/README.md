# Book-site
This site designed to buy, search and rating books.

## Requirements
To install all libraries run the following:
`pip install -r requirements.txt`

Also, you need set up your virtual environment.


### Settings
Converted to python package, that contains base, local, production, staging and
test .py files for all servers we need to start.

To start server use this command:
```python
python manage.py runserver --settings=config.settings.local(or other server we need)
```

You also can set DJANGO_SETTINGS_MODULE environment variable.

Windows command: `set DJANGO_SETTINGS_MODULE=config.settings.local`

until venv is started. To add permanent variable add this line in venv/Scripts/activate.bat
#### Env
Collect all your secret keys in config/settings/.env file.
