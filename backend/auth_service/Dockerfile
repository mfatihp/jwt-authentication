FROM python:3.12.11-bookworm


WORKDIR /app

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip

COPY . .
RUN pip install --no-cache-dir -r auth_requirements.txt

EXPOSE 8000


CMD ["uvicorn", "auth:app", "--host", "0.0.0.0", "--port", "8000"]