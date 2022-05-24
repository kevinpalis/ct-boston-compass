# Boston Compass #

This is a simple application that utilizes the Boston Transportation System's API to provide the following:

1. Print all long_names of all routes of type 0 and 1, ie. subway routes
2. Print:
    - The name of the subway route with the most stops as well as a count of its stops.
    - The name of the subway route with the fewest stops as well as a count of its stops.
    - A list of the stops that connect two or more subway routes along with the relevant route names for each of those stops. 
3. List a rail route you could travel to get from one stop (source) to the other (destination).
4. Print all the stop names (for reference in case you need a list of all the valid input to source or destination).

> For the purpose of this application, I've acquired an API key which is used as default for every run of this application. However, it can be overriden using the -k flag, in case you want to use a different key.
> Note that not using a key will limit requests to 20 per minute. Using an API key raises this limit to 1000 requests per minute, which is more than enough for this application's purposes.

Some notes on the algorithm (finer details are in the inline documentation of compass.py):

- It tries to minimize API calls as much as possible so as not to saturate the server or hit request limits
- It tries to filter results in the server, ie. passing filter parameters on the API call - to be as efficient as possible.
- It uses a graph to store stops information as nodes/vertices and routes (subway lines) as edges.
- The graph is unweighted. We don't take into consideration the time it takes to get from one stop to another.
- It uses Breadth-first search to find a path between the two stops provided.
- Activating verbose printing will show the actual path the algorithm traverses to get from one stop to another.

## Libraries required (pre-provisioned)

This application utilizes the following libraries/technologies:

- Requests = for all HTTP requests to MBTA's API
- NetworkX = for graph storage and operations
- Pytest = for all testing

> The docker container this application comes in with should already provision necessary installations. See **Dockerfile**.
>
> As such, the only real requirement is that you have the **docker engine**.

## Running the application

There are two ways to run this application, in the order of preference:

### Run using the pre-built docker image

There is a pre-built docker image in Dockerhub ( **gadm01/boston-compass** ) - which means you don't even need to pull this repository. In a command line run the following:

```bash  
#Pull the docker image
docker pull gadm01/boston-compass

#Run the docker container
docker run --detach --name boston-compass -it gadm01/boston-compass

#Go inside the container's shell to run the CLI of boston-compass
docker exec -ti boston-compass bash
```

Once you're inside the container, everything will be provisioned for you so you can simply use boston-compass' CLI. Here are sample commands:

```bash  
#Navigate to boston-compass's root directory:
cd /home/compass
#Run the compass with all default values. 
python3 compass.py

#Run the compass with default values and higher verbosity
python3 compass.py -v

#Run the compass to find routes between source and destination stops (verbose)
python3 compass.py -s "Davis" -d "Butler" -v

#Show all subway stops (to see all valid values for source and destination)
python3 compass.py -a

#Print usage help
python3 compass.py -h
```

### Run by building from source (ie. docker build)

If you really want to build from source, here are the steps:

```bash  
#Make sure you are in the same directory as the Dockerfile, then run
docker build -t boston-compass .

#Run the docker container
docker run --detach --name boston-compass -it boston-compass

#Go inside the container's shell to run the CLI of triforce-link
docker exec -ti boston-compass bash
```
Once you're inside the container, you can use boston-compass' CLI as shown in the previous section.

## Running the tests

Assuming all steps before this section was successful, you can simply run pytest to run all unit tests:

```bash  
#Go to application's home
cd /home/compass
#To run all tests:
python3 -m pytest
#To run all tests with the name of the tests and better printings:
python3 -m pytest -v
#To run specific test, test_compass_invalid_source_stop test for example:
python3 -m pytest -v -k test_compass_invalid_source_stop
```

### Areas of improvement
- More unit tests and integration tests
- Include the order of stops that the train actually travels for a given route
- Include the time of travel when searching for routes between two stops

### Questions/Clarifications ###
Please contact:

* **Kevin Palis** <kevin.palis@gmail.com>