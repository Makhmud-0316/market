run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate
admin:
	python manage.py createsuperuser