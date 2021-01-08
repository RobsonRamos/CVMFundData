FROM alpine
 
RUN apk add --no-cache python3-dev  && python3 -m ensurepip && pip3 install --no-cache --upgrade pip setuptools 
 
WORKDIR /app

# # Copy everything which is present in my docker directory to working (/app)
COPY /requirements.txt /app

RUN apk add gcc libc-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY src /app


EXPOSE 5000 
 

# These commands will be replaced if user provides any command by himself
CMD ["python3", "-u", "./app.py"]


