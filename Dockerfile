FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV DB_USERNAME="calendar-app"
ENV DB_PASSWORD="hue882gjng"
ENV DB_HOST="mongodb-service"
ENV DB_PORT="27017"
ENV DB_DATABASE="calendar_dbexit"
ENV SECRET_KEY="3f5eed7b6884e653ca2debd0653a92bfe9389a0351dd9589"
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
EXPOSE 5000
CMD ["flask", "run"]



