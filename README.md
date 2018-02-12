# Docker for Professionals: The Practical Guide

#### Links

#### Notes and Commands

- Running ubuntu image and **"echo"** command  

  ```shell
  # docker run - creates a container
  # ubuntu - image name
  # echo - command in ubuntu image 
  sudo docker run -i -t ubuntu echo 'Hello World'
  ```

- Running named containers

  ```shell
  # --name - giving a name to the container 
  # d - detached
  sudo docker run --name server -d afakharany/server

  # -i interactice
  # -t it willl receive and respons  signals from the shell 

  # linking a container named 'server' with a 'server' variable inside 'checker'
  sudo docker run -it --link server:server --name checker afakharany/checker 
  # removing 'checker' container
  sudo docker rm -f checker
  # stoping container
  sudo docker stop server

  # displaying logs of container 'checker'; id can also be used
  sudo docker logs checker
  ```

- Running a command inside the container

  ```shell
  # running "ps" command 
  docker exec server1 ps -ef
  ```

- Storing a container's id

  ```shell
  # I variable
  CID=$(docker create busybox)

  # II file
  docker create --cidfile /tmp/mycontainter.cid busybox  

  ```

- Human friendly names

  ```shell
  # docker will generate some random name "happy_mclean"
  sudo docker run -d busybox sleep 30000

  udo docker ps
  CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
  339dbd1a5e16        busybox             "sleep 30000"       33 seconds ago      Up 32 seconds                           happy_mclean

  ```

- Creating neutral systems

  - read-only filesystems

  - environment variable injection

  - volumes

    ```shell
    docker run -d --read-only --name wpress wordpress
    ```
    ```shell
    # -e - passing an env. variable 
    docker run --name wpressDB -d -e MYSQL_ROOT_PASSWORD=admin mysql

    # running wordpress and linking to created mysql container
    # -v volumes, in this case we are allowing for modifications
    docker run -d --read-only --name wpress --link wpressDB:mysql -p 80 -v /run/apache2 -v /run/lock/apache2 -v /tmp wordpress
    ```

    ```shell
    # -e passing variables
    # env printing env. variables
    docker run -e DB=main -e USER=admin busybox env
    ```

- Recovering  from failures - restarting

  ```shell
  # --restart - auto restart container
  # on-failure[:max-retries] - only when stopped due to failure
  # unless-stopped - dont restart when container was stopped
  # always

  docker run -d --name displaydate --restart always busybox date
  ```

- Entrypoint is a command or a script executed when a container starting. Command  `sh -c` is used for execution. 

  ```shell
  # will call cat and display docker-entrypoints.sh  contents
  docker run --entrypoint="cat" mysql /usr/local/bin/docker-entrypoints.sh 
  ```

- removing containers

  ```shell
  docker rm <name or id>

  # remove container as soon as it stops
  docker run -it --rm --name displaydate busybox date
  ```

- Searching for images

  ```shell
  docker search mysql
  ```

- Pulling from non-standard docker repo

  ```shell
  pull quay.io/nitrous/wordpress
  ```

- Obstaining an image from a file

  ```shell
  # removing an image
  docker rmi busybox

  # loading the image from the file
  docker load -i busybox.tar

  # exporting the image to the file
  # busybox - image
  # busybox.tar - file
  docker save -o busybox.tar busybox:latest
  ```

- building an image

  ```shell
  docker build -t johndoe/mydockerimage .
  ```

- Volumes - "mount points" to the respective filesystems on the host OS

  - database data
  - the log data of a web application
  - dynamically changing data

  ```shell
  sudo docker run -d --volume /var/lib/mysql --name mysql-shared busybox echo Hello, I am the volumes container
  # volumes-from - container will use a volume created by another container 
  sudo docker run -d --volumes-from mysql-shared --name mysql1 -e MYSQL_ROOT_PASSWORD=admin mysql
  # mysql mysql - image, command
  sudo docker run -it --rm --link mysql1:mysqldb mysql mysql -u root -padmin -h mysqldb

  ```



  ```dockerfile
  FROM Ubuntu:latest
  RUN apt-get update
  RUN apt-get install python
  RUN mkdir /csv
  COPY * /csv/
  RUN useradd -ms /bin/sh worker
  WORKDIR /csv
  RUN chown worker /csv/csv_to_insert.py
  RUN chmod a+x csv_to_insert.py
  USER worker
  CMD ["/csv/csv_to_insert.py"]
  ```

  ```shell
  # binding volumes
  # /share - directory on a host system
  # /csv - directory visible inside the container
  docker run -it -v /share:/csv --rm afakharany/csvtosql
  
  # running witf read only mounted volume
  docker run -it --rm -v /csv:/csv:ro afakharany/csv
  
  # docker managed volumes
  # docker will map /csv onto some location on host's disc
  docker run -it --name csvContainer -v /csv afakharany/csv
  
  # checking where Docker save the mount point
  docker inspect -f "{{json .Mounts}}" csvContainer
  ```

- removing containers with volumes

  ```shell
  docker rm -v afakharany/csv
  ```

  ​





####  



#### Instructions