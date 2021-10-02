FROM python:3
COPY requirements.txt .
RUN apt update
RUN apt-get install -y libmediainfo-dev
RUN apt-get install -y ffmpeg
RUN pip3 install -r requirements.txt
COPY / .
CMD [ "python", "./main.py" ]