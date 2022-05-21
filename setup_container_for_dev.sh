#Reference commands for developers
#You can either run this script directly or run the commands in here one by one.
#@author Kevin Palis

#Step 1: build this container from source - you need to be in the directory where the Dockerfile is located
docker build --force-rm=true -t boston-compass .
#Step 2: run the container and mount the source directory as volume - this will allow you to make changes without having to rebuild and re-ran the container ala python env
#needs to be in the root directory of the project
docker run -v $(pwd)/compass:/home/compass -p 8080:8080 --detach --name boston-compass -it boston-compass
#Step 3: write your code. Changes will automatically be picked up by the running container
#Note: To run your code, you need to exec into the container. Tip: Just keep a terminal session that's always inside the container.
# docker exec -ti boston-compass bash -c "<run your script>"
