# ads-post

sudo docker run -itd -e POSTGRES_USER=ali -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=ads_post_db -p 5436:5432 --name ads_post_db postgres:11.6

alembic init alembic


alembic revision --autogenerate -m "initial migration"


alembic upgrade head