FROM python:3

COPY ["requirements.txt", "/usr/src/"]

WORKDIR /usr/src

RUN pip3 install -r requirements.txt

COPY [".", "/usr/src/"]

ENTRYPOINT ["python3", "ctfr.py"]

CMD ["--help"]
