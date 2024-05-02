FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 3100

# Run the application with a non-root user
RUN addgroup --system app && adduser --system --group app

USER app

ENTRYPOINT ["gunicorn", "app:app"]