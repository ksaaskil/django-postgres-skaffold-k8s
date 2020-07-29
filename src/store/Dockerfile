FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /store
WORKDIR /store

ADD requirements.txt /store
RUN pip install -r requirements.txt

ADD . /store

RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "store.wsgi"]
