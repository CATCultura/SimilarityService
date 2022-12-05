FROM python:3.7.14-alpine3.15

ADD ./ /py-service/

WORKDIR /py-service

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["SimilarityServiceController.py"]