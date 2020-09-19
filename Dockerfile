FROM python:3.6.1-alpine
COPY server /server
WORKDIR /server
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python","app.py"]
