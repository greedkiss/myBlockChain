FROM python:3.6-alpine

WORKDIR /app

COPY requirement.txt /app
RUN cd /app &&\
    pip install -r requirement.txt

COPY core.py /app

EXPOSE 5000

CMD ["python", "core.py", "--port", "5000"]