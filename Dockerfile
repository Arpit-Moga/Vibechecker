FROM python:3.12
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY mcp_server/ ./mcp_server/
EXPOSE 80
CMD ["uvicorn", "mcp_server.main:app", "--host", "0.0.0.0", "--port", "80"]
