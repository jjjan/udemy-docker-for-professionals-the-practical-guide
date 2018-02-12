FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python
RUN mkdir /csv
COPY * /csv/
RUN useradd -ms /bin/sh worker
WORKDIR /csv
RUN chown -R worker /csv
RUN chmod a+x csv_to_insert.py
USER worker
CMD ["/csv/csv_to_insert.py"]
