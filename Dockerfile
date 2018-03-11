FROM alpine:latest

RUN apk add --update python3 py3-pip git

RUN git clone https://github.com/UnaPibaGeek/ctfr
WORKDIR ctfr
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "ctfr.py"]
CMD ["-h"]
