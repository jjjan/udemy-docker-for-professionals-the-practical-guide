# Docker for Professionals: The Practical Guide

#### Using Docker Containers

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
  
  # status of containers
  sudo docker ps
  
  # -i interactice
  # -t it will receive and respons  signals from the shell 
  
  # linking a container named 'server' with a 'server' variable inside 'checker'
  sudo docker run -it --link server:server --name checker afakharany/checker 
  # removing 'checker' container
  sudo docker rm -f checker
  # stoping container
  sudo docker stop server
  # sudo docker stop container_name/id
  # sudo docker start container_name/id
  # sudo docker restart container_name/id
  
  # displaying logs of container 'checker'; id can also be used
  sudo docker logs checker
  ```

- Running a command inside the container

  ```shell
  # running "ps" command 
  docker exec server1 ps -ef
  ```

- The PID namespace

  ```bash
  docker run -d --name server1 busybox nc -l -p 0.0.0.0:7070 
  
  docker run -d --name server1 busybox nc -l -p 0.0.0.0:8080
  
  # each container has it's own  PID 
  docker exec server1 ps -ef
  PID   USER     TIME   COMMAND
      1 root       0:00 nc -l -p 0.0.0.0:7070
      6 root       0:00 ps -ef
  
  docker exec server2 ps -ef
  PID   USER     TIME   COMMAND
      1 root       0:00 nc -l -p 0.0.0.0:8080
      7 root       0:00 ps -ef
  
  # adding --pid host  will overwritte the isolation
  ```

  

- Storing a container's id

  ```shell
  # I variable
  CID=`docker create busybox`
  
  # II file
  docker create --cidfile /tmp/mycontainter.cid busybox  
  
  ```

- Human friendly names

  ```shell
  # docker will generate some random name "happy_mclean"
  sudo docker run -d busybox sleep 30000
  
  sudo docker ps
  CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
  339dbd1a5e16        busybox             "sleep 30000"       33 seconds ago      Up 32 seconds                           happy_mclean
  
  ```

- Creating neutral systems

  - read-only filesystems - prevents any changes to the underlying system.  Apps use databases to store and manage their data.

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
    
    # wordpress with variables
    docker run -d --read-only --name wpress --link wpressDB:mysql -p 80 -v /run/apache2 -v /run/lock/apache2 -v /tmp -e WORDPRESS_DB_HOST=database_hostname -e WORDPRESS_DB_NAME=the_database_name wordpress 
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

- Removing containers

  ```shell
  docker rm <name or id>
  
  # remove container as soon as it stops
  docker run -it --rm --name displaydate busybox date
  ```

- Searching for images

  ```shell
  docker search mysql
  ```

- Repository i.e. `quay.io/replicatedcom/nagios`

  - Host: `quay.io`
  - Username: `replicatedcom`
  - Image: `nagios`

- An image can be further identified by using tags. A tag often reflects the image version. A tag is added at the end of the image name, preceded by a colon. 

- Searching

  ```bash
  docker search mysql
  ```

- Pulling from non-standard docker repo

  ```shell
  pull quay.io/nitrous/wordpress
  ```

- Obtaining an image from a file

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

- building own image

  - Create an empty directory `mkdir mydockerimage`

  - Create a script file called **runner.sh**

    ```
    #!/bin/sh
    echo "Server started at " $(date)
    while true; do
    # The loop is doing nothing. It is just to keep the container running in the
    background
    sleep 5
    done
    ```

  - Create a Dockerfile

    ```
    FROM busybox:latest
    RUN mkdir /runner
    COPY ./runner.sh /runner
    RUN adduser -DHs /bin/sh worker
    WORKDIR /runner
    RUN chown worker runner.sh
    RUN chmod a+x runner.sh
    USER worker
    CMD ["/runner/runner.sh"]
    ```

  - Build your image

    ```
    docker build –t masteringdocker/server:latest
    ```

#### Persistent storage

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

- "bind mount" volume type
  - It refers to volumes that have user-specified mount points on the host operating
    system.
  - This type is used when you want to share data between the container and the host.

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
 
  ```

- Docker managed volumes
  - When you use managed volumes, you do not specify a mount point for the volume
    on the host filesystem. Instead, Docker mages this volume on some location on the
    host filesystem.

```bash
  # docker managed volumes
  # docker will map /csv onto some location on host's disc
  docker run -it --name csvContainer -v /csv afakharany/csv
  
  # checking where Docker save the mount point
  docker inspect -f "{{json .Mounts}}" csvContainer
```

- Sharing volumes the host-dependent way

```bash
# mounting /share:/csv
docker run --name csv -d –v /share:/csv afakharany/csv
docker start mysql1
# mounting /share:/mnt
docker run -it –v /share:/mnt --rm --name mysql-client --link
mysql1:mysqldb mysql mysql –u root –padmin –h mysqldb
```

- Generalized volume sharing

  - When the number of volumes get larger, and if you are mixing between docker-managed and bind volumes it is better to use `--volumes-from`

  ```bash
  docker run --name csv -d –v /share:/csv –v /csv2 --rm afakharany/csv
  
  # inherits volumes from  csv container
  docker run -it –volumes-from csv --rm --name mysql-client --link mysql1:mysqldb mysql mysql –u root –padmin –h mysqldb
  ```

  - Do not use when:
    - container needs to find the data on a specific mount point name that is different than the one used in the parent container
    - more than one mount point are having the same name
    - you are planning to change the read/write access permissions of the inherited volumes

- Referencing managed volumes

  - Managed volumes cannot be shared except by using --volumes-from. They cannot be removed except when the owning container is removed

  - It is a common practice to create a container for each managed volume used on the system
  - Removing containers with volumes

  ```shell
  docker rm -v afakharany/csv​
  ```

#### Networking in Docker

- Closed container

  - This container does not have any access to the outside world
  - Container will not be reachable from outside the host

  ```bash
  docker run --rm --net none busybox ifconfig –a
  ```

- Bridged containers

  - default type of networks in Docker containers
  - In this mode, the container has two interfaces: the loopback interface, and another private interface that is connected to the host’s virtual interface and the bridge (docker0)
  - This is the one used to connect to the outside network
  - All communication  is done through the IP addresses

  ```bash
  docker run --name bridgedcontainer -d  busybox nc -l 0.0.0.1:10000
  
  ```

- Containers' name resolution

  - you can assign a hostname to the container while creating it 

    - using the –hostname flag.
    - hostname is used by the container internally. It is not visible from the outside.
    - Docker overrides the DNS by manually assigning a hostname to the container.

    ```
    docker run --rm --hostname helloDocker busybox nslookup helloDocker
    ```

    - specifying one or more DNS servers that will be used in name resolution

    ```
    docker run --rm --dns=8.8.4.4 --dns=8.8.8.8 busybox nslookup google.com
    ```

  - You can  instruct the containers to use a domain name

    ```bash
    # myserver.example.com - fully qualified domain name
    # client is instructed to append example.com by default with --dns-search.
    
    docker run --rm –dns-search google.com busybox nslookup mail
    
    ```

  - Manually assigning hostnames to IP addresses using the `–add-host` flag.

    ```bash
    docker run --rm –add-host www.google.com:127.0.0.1 busybox ping www.google.com
    ```

- Controlling connections to the container

  - By default, bridged containers cannot be reached from outside the host.
  - You can allow specific ports to be accessible from the outside network using port forwarding, flag `-p`

  ```bash
  #  N container's port number bound to a random host port
  -p N
  # n - host port, N - container's port
  -p N:n
  # N - container's port number bound to a random host port but only on the
  # interface specified by the IP address
  -p ip_address::N
  # N - container's port number bound to  'n' host's port but only on the
  # interface specified by the IP address
  -p ipaddress:n:N
  ```

  

  -  Assigning random host ports to all the ports exposed by a given container

  ```bash
  docker run –P httpd
  ```

  - To determine which ports on the container are mapped to which ports on the host use: `docker ps`, `docker inspect` , or `docker port`

- Joined containers - more than one container sharing the same network interface

  - Used if you have containers that need to communicate with each other but you don’t want any external access

  ```bash
  docker run --name server1 -d --net none busybox nc -l 127.0.0.1:8888
  
  docker run -it --rm --net container:server1 busybox netstat -al
  ```

  - conflicts may arise when running programs that have the same port numbers on
    two joined containers

- Open containers

  - Open containers have full access to the host's interface. They can use ports that are numbered lower than 1024.

  ```
  docker run –it --net host busybox ifconfig –a
  ```

- How do containers "know" about each other - lining

  - When linking an entry will be added to the DNS override list (/etc/hosts) specifying the hostname and the IP address of the target machine to be easily discovered

  ```bash
  docker run –d --name webserver1 httpd
  docker run –it --rm --link webserver1:web busybox wget web
  ```

- Environment variables creation

```bash
# will produce a list of environment variables that were automatically created when the container was linked.

docker run –d --name baseserver --expose 8080 –expose 9090 busybox nc –l 0.0.0.0:8080

docker run --rm –it --link baseserver:server busybox env
# there will be a variable starting with the alias followed by 'NAME' (SERVER_NAME), then the container's name and the link alias separated by a slash.
# ie. SERVER_NAME=/client2/server

#The rest of the environment variables can be classified as follows:
#ALIAS_PORT_PORT_NUMBER_PROTOCOL_PORT
#ALIAS_PORT_PORT_NUMBER_PROTOCOL_ADDR: this refers to the interface IP address on which
#the port is bound.
#ALIAS_PORT_PORT_NUMBER_PROTOCOL_PROTO: the name of the protocol (TCP or UDP).
#ALIAS_PORT_PORT_NUMBER_PROTOCOL: this will have all the previous information encoded in one URL.
```

#### SECURITY & ISOLATION

##### Memory allowance

- Limiting the amount of memory that can be used by the container: `-m` or `--memory` 
- Docker prevent the container from exceeding that amount (bytes (b), kilobytes (k), megabytes (m) or gigabytes (g)).

```bash
docker run --name webserver –m 512m httpd
```

- Make sure whether or not the application can function properly within the assigned memory limits
- If any application runs out of memory it may start writing error messages indicating that in the logs
  and it may crash. Use `--restart` to mitigate this issue.

##### CPU allowance

- By restricting the percentage of CPU cycles the container will use relative to the sum of all computing cycles available to the other containers `--cpu-shares`.
  - If a container needs more CPU than the assigned to it and that amount of CPU cycles is available on the host, the container will just break the limit and use the extra cycles.

```bash
docker run –d --cpu-shares 1024 –name hogger1
afakharany/hogger
docker run –d --cpu-shares 2048 –name hogger2
afakharany/hogger
```

- By setting the container to work on only a set of CPU cores `–cpuset-cpus` flag.
  - It can be specified in the following ways:
    - --cpu-set 0 for using only the first CPU of the host
    - --cpu-set 0-2 for using the first, the second, and the third CPUs
    - --cpu-set 0,2 for using the first and the third processors

```bash
docker run –d --name hogger --cpuset-cpus 0 afakharany/hogger –c
```

##### Controlling access to devices

- Some devices are automatically mapped by Docker and some others aren't.
- To map a device from the host to the container you can use the --device flag.
- Mapping the cdrom device on the host (/dev /sr0) to a device with the same name
  on the container.

```bash
# --privileged flag to be able to mount the device
docker run -it --rm --privileged --device /dev/sr0:/dev/sr0
busybox mkdir /media && mount /dev/sr0 /media && ls -l /media
```

##### Determining the container's user account

- By default, Docker containers run as the root use account.
- Inspect the container for the user and UID

```bash
docker create –name myUser busybox sleep 3000
docker inspect --format="{{ .Config.User }}" myUser
```

- If the result of the above command is nothing, then the default user is root with UID 0. Otherwise,
  the author of the image has chosen to make it "run-as" a specific user.

- Another option is to run a quick test on an image to determine the user account by
  which the container will be run.
- The id command is used to display the UID and the username of the current user.

```
docker run --rm --entrypoint "" busybox:latest id
```

##### Changing the default user

- You can change the default user that is used to run the container when running or creating it.
- You must select a user that already exists in the container.
- Available users on a give container:

```
docker run --rm -it --entrypoint "" busybox cat /etc/passwd | cut -d: -f 1,3,4,5
```

- Running the container with a choosen user

```
docker run --user nobody busybox id
```

- The --user (or –u) option can be used also for specifying groups, UIDs and GIDs.

```
docker run --user 99 busybox id
docker run --user www-data:www-data busybox id
```

- You should develop the habit of setting passwords and/or locking the root account in containers that do not do that by default

##### Handling permissions on volumes

```bash
echo "file contents" > /share/sharedfile.txt
ls -l /share/
# -rw-r--r-- 1 root root   14 lis  2 17:50 sharedfile.txt
chmod 600 /share/sharedfile.txt
ls -l /share/sharedfile.txt
# -rw------- 1 root root 14 lis  2 17:50 /share/sharedfile.txt
docker run -it -v /share:/share busybox cat /share/sharedfile.txt
# file contents
docker run -it --user nobody -v /share:/share busybox cat /share/sharedfile.txt
# cat: can't open '/share/sharedfile.txt': Permission denied
# The nobody user cannot access the text file because the UID is different.
# However the root user could read the file as the root account on the container and the one on the host share the same UID 0.

```

####  Packaging software in images

#### Software packaging

- Creating a new image from existing container.

```bash
 docker run --name base busybox touch /welcome.txt
 docker commit base base_image
 docker rm base
 docker run -it --rm base_image ls -l /welcome.txt
```

- Creating ubuntu image with python

```bash
docker run --name python ubuntu /bin/bash
# installing python in an container 
apt-get update
apt-get install python

docker commit python ubpython
docker run --rm -it ubpython python --version

```

##### Determining changes 

````bash
docker diff base_container
````

- Report with A D, C prefixes
  - A : Added
  - D : Deleted
  - C : Changed

- Commiting with an author and a message

```bash
docker commit -a "@afakharany" -m "Installed Python 2.7" base_container ubpython
```

##### The entrypoint configuration

```bash
# will run python and python interpreter
docker run -it --name python --entrypoint python ubpython
```

##### The commit command options

- Variables are inherited if not provided

```bash
# -e - env variable
docker run -it --name shared -e MYVAR=Hello busybox
# a - author, m - message
docker commit -m "Added MYVAR" -a "@afakharany" shared shared-image

docker run --rm -it shared-image echo $MYVAR
```

- File operations in UFS

```bash
docker run --name test busybox rm /etc/localtime
docker diff test
# C /etc
# D /etc/localtime

docker run --name test2 busybox touch /etc/localtime
docker diff test2
# C /etc
# C /etc/localtime

```

##### The commit command and UFS

- Any changes made to the UFS file system are written to the top-most layer, in addition to the metadata of that layer.
- A layer metadata contains the unique identifier, the identifier of the layer below it, and information about the container that was used to create the layer.
- The image id is also the id of the top most layer. This is also the ID that gets printed when the commit command is used.

- Tags identify the image and let you to keep many version of the image

```bash
root@DockerDemo:~# docker commit -m "install python" -a "@afakharany"
python-int afakharany/ubpython:v1
sha256:54ed4d035c33012cde0598f5342220157a69371b1e6fdf33cae13311c540c5
0b
```

- Tags can be added to the image at built time, or when committing changes, or even afterwards
  using the docker tag command. 

```bash
docker tag afakharany/ubpython afakharany/ubpython:v1
```

##### Image layer sizes and limits

- Layers are immutable.
- Any change made to an image creates a new layer.
- The layer limit  is a number indicating the maximum amount of layers that can be created on an image.
- Check  the available layers using the command `docker history`.

##### Working with flat file systems

- Exporting image

```bash
docker run --name myContainer afakharany/ubpython:latest
docker export --output myContainer.tar myContainer
```

- Importing tar to an image

```bash
docker import – myImage < myContainer.tar
```

