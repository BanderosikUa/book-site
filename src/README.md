## Requirements
To install all necessary libraries, run:

```bash
pip install -r requirements.txt
```

Make sure to set up your virtual environment before proceeding.

### Settings
This project uses a Python package for settings, with configurations for base, local, production, staging, and test environments.

To start the server, use:
```python
python manage.py runserver --settings=config.settings.local
```
(Replace local with the desired environment.)


Alternatively, you can set the DJANGO_SETTINGS_MODULE environment variable:

Windows command: `set DJANGO_SETTINGS_MODULE=config.settings.local`

To make this setting permanent, add the following line to venv/Scripts/activate.bat:
### Database
The project uses PostgreSQL as the database.

#### Env
Store all your secret keys in the config/settings/.env file. For an example, check the env_example file in config/settings and rename it to .env.

#### Populating the Database
To populate your database with sample data, download the book dataset from here[https://www.kaggle.com/datasets/lukaanicin/book-covers-dataset]. After unzipping the files into the staticfiles directory, run:
```python
python manage.py fill_db [--books] [--genres]. 
```
Where --books and --genres is optional params that

Both --books and --genres are optional parameters that specify the number of books and genres.
