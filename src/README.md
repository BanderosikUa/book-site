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
### Database
Db used in this project is a PostgresSQL.

#### Env
Collect all your secret keys in config/settings/.env file.
For template .env check env_example file in config/settings, don't forget to rename the file.

#### Random data fill script
If you wanna fill your database with data, then just download book database from here: https://www.kaggle.com/datasets/lukaanicin/book-covers-dataset.
After unzip files in statitcfiles dir and run __python manage.py fill_db [--books] [--genres]__. Where --books and --genres is optional params that
define amount of genres and amount of books in separate genre.
