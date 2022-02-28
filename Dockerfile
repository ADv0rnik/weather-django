FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update && apk add python3-dev gcc libc-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN apk add libffi-dev
RUN pip install -r requirements.txt

COPY . .
RUN ls -la

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]



