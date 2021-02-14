FROM aicg4t1/tflite:2.1.0
ADD . /webapp
WORKDIR /webapp
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]