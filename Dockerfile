FROM python:3.9.15-slim

ADD ./ /py-service/

WORKDIR /py-service

RUN pip install --upgrade pip

RUN pip install flask-restx

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["SimilarityServiceController.py"]
