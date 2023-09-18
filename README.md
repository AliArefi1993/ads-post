# ads-post

## Dependencies

#### Project Requirements
Install project requirements with this command.
```
pip install -r app/requirements.txt
```
#### PostgreSQL Database
Install PostgreSQL or use docker to run an instance of PostgreSQL.
```
docker run -itd -e POSTGRES_USER=<USERNAME> -e POSTGRES_PASSWORD=<PASSWORD> -e POSTGRES_DB=<DATABASE_NAME> -p 5436:5432 --name postgresql postgres:11.6
```
Change the database url based on your configurations in alembic.ini file.
```
...
sqlalchemy.url = postgresql://<USERNAME>:<PASSWORD>@localhost:5436/<DATABASE_NAME>
...
```
After that we should migrate our database with this command.
```
alembic upgrade head
```
Set SECRET_KEY environment variable.
```
export SECRET_KEY=<YOUR_RANDOM_STRING_SECRET_KEY>
```

### Run project
To run the project run this command.
```
uvicorn app.main:app
```

Then you can access the swagger documentations in
```
http://127.0.0.1:8000/docs
```