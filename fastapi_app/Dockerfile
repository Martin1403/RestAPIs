FROM python:3.9-slim

RUN mkdir -p "orders/orders"
COPY requirements.txt orders/requirements.txt
RUN pip install -U pip
RUN pip install -r orders/requirements.txt
COPY . /orders

WORKDIR orders
EXPOSE 5002
CMD ["uvicorn", "orders:app", "--host", "0.0.0.0", "--port", "5002"]
