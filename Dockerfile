FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip intall --no-cash-dir -r requirements.txt
COPY . .
CMD ["python", "snake.py"]