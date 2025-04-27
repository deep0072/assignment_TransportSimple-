# Use the official Python runtime image
FROM python:3.12.3

# Create the app directory
RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/
# run this command to install all dependencies 
RUN pip install  -r requirements.txt
RUN python -m pip install psycopg2-binary
COPY . /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


