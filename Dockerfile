FROM python:3.12.9-alpine3.20 as dev

WORKDIR /work 

COPY ./requirements.txt /work/requirements.txt

RUN pip install -r requirements.txt

COPY . /work

ENTRYPOINT ["python3"]

CMD ["-u", "main.py"]
