FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /store
WORKDIR /store
COPY . /store/
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
