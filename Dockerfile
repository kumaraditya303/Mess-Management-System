# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y 
RUN apt-get install wkhtmltopdf -y
# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy files to work directory
WORKDIR /code
ADD . /code

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "runserver:app", "--bind", "0.0.0.0:8000","--thread=17","--log-level=DEBUG"]
