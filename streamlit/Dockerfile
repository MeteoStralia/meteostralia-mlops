#syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /app/

COPY requirements_streamlit.txt /app/

RUN pip install --no-cache-dir -r /app/requirements_streamlit.txt

COPY . /app/

EXPOSE 2222

CMD ["streamlit", "run", "app.py", "--server.port", "2222"]
