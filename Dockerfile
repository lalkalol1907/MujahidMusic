FROM python:3
COPY requirements.txt .
RUN apt-get update
RUN apt-get install -y libmediainfo-dev
RUN apt-get update
RUN apt-get install -y ffmpeg --fix-missing
RUN pip3 install -r requirements.txt --use-deprecated=legacy-resolver
COPY / .
CMD [ "python", "./main.py" ]