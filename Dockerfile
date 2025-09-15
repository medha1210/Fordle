FROM python:3.11-slim


WORKDIR /app


COPY gcp_req.txt .
RUN pip install --no-cache-dir -r gcp_req.txt


COPY . .


EXPOSE 8080

CMD ["sh", "-c", "streamlit run fordle_app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]


