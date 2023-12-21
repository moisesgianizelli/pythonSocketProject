FROM python:3.11
WORKDIR src 
COPY * /src/ 
RUN pip install -r ./requirnments.txt
CMD python ./server.py