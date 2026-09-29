FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY requirements.txt ./

RUN uv pip install --system -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]