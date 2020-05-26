FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /store
WORKDIR /store
COPY . /store/
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "store.wsgi"]
