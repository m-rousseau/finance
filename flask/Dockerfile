FROM python:3.7-alpine
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
ADD main.py /app
# EXPOSE 5000
RUN pip3 install -r requirements.txt
CMD ["python", "main.py"]