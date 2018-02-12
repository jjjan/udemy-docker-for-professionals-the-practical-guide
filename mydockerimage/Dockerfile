FROM busybox:latest
RUN mkdir /runner
COPY ./runner.sh /runner
# adding user worker with sh as a shell tool
RUN adduser -DHs /bin/sh worker
WORKDIR /runner
RUN chown worker runner.sh
RUN chmod a+x runner.sh
USER worker
CMD ["/runner/runner.sh"]
