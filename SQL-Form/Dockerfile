FROM python:3.10

RUN mkdir app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN apt update
RUN pip install --upgrade pip

EXPOSE 8080
EXPOSE 3306

CMD streamlit run app.py --server.port 8080