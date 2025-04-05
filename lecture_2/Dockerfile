FROM python:3.13 
COPY . .
RUN pip3 install -r requirements.txt 
CMD ["uvicorn", "hw.shop_api.main:app", "--port", "8080", "--host", "0.0.0.0"]
