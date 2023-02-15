FROM python3.7.16
WORKDIR /app
COPY . .
ENV MAX_WORKERS="1"
ENV WEB_CONCURRENCY="1"
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python","APP/main.py"]
