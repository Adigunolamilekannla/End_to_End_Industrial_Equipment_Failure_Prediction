FROM python:3.10-slim-buster
WORKDIR /main
COPY . /main 



RUN apt-get update && pip install -r requirements.txt
CMD ["python","main.py"]