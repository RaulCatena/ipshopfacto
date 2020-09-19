FROM python:3.6.1-alpine
ADD server/ /project
WORKDIR /project/server
RUN pip install -r requirements.txt
CMD ["python","app.py"]
