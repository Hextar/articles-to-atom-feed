FROM python:3.7.2

MAINTAINER Stefano st.salidu@gmail.com

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt

WORKDIR /src

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /src

CMD ["python", "main.py", "-u","(url)"]
