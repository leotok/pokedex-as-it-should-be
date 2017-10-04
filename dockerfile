FROM continuumio/anaconda:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
# RUN pip install -r requirements.txt
RUN pip install -r anaconda-pip-requirements.txt
ENTRYPOINT ["python"]
CMD ["app/api/app.py"]