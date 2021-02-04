# redis_crud

This project is a simple Redis key counter built on top of https://github.com/nirmash/appsync-redis-api and demonstrates deploying the same function into different environments. 

## Function Logic
The function accepts a Redis key name and value in the Lambda event body, it then stores the key and value is Redis and increments a counter of overall key writes and of key writes for the key the function writes into. 

## Pre-requisites 
Go through the steps in https://github.com/nirmash/appsync-redis-api to install a Redis GraphQl endpoint. Make sure to record the GraphQl uri endpoint and access key values you obtain during the blog steps.

Make sure you have [Docker](https://docs.docker.com/get-docker/) installed on your machine.

## Deploy and run with SAM
This repo includes a `template.yaml` file for a SAM deployment. To deploy and test your function:

1. Update the `API_URI` and `API_KEY` values in the `template.yaml` file with the values you obtained deploying the `appsync-redis-api` github repository. 
2. From the terminal, execute `./build.sh` in the root folder of this repository (`redis_crud`).
3. Walk through the instructions deploying your function.
4. Capture the uri of the redis_crud function from the SAM deploy output.
5. To test your new function, use the `curl` command in the terminal:

    `curl -X POST -d "{ \"key\": \"keytwo\", \"value\": \"valone\" }" -H "Content-Type: application/json;charset=UTF-8"  <URL of the deployed function from step 4>` 

    If all is well, the function output should look like:
    `{"message": "CRUD count - 1 CRUD count for keytwo - 1"}`

## Run locally with Docker
This repo includes a `template.yaml` file for a SAM deployment. To deploy and test your function:

1. Update the `API_URI` and `API_KEY` values in the `Dockerfile` file with the values you obtained deploying the `appsync-redis-api` github repository.
2. Build your container locally by typing the below in the root folder of this repository (`redis_crud`):
    `docker build . -t redis_crud`
3. Execute your container and map it to port 80 on your machine:
    `docker run -it -p 80:80 redis_crud`
4. To test your new function, start a new terminal and use the `curl` command in the terminal:

    `curl -X POST -d "{ \"key\": \"keytwo\", \"value\": \"valone\" }" -H "Content-Type: application/json;charset=UTF-8"  http://localhost` 

    If all is well, the function output should look like:
    `{"message": "CRUD count - 1 CRUD count for keytwo - 1"}`

## Deploy and test your container in the cloud
Now that you have a container running locally, you can deploy it to your container orchestrator of choice. For example, you can setup an Elastic Container Service (ECS) cluster and configure it to use a Lambda container that is stored in a container registry like Docker Hub or Elastic Container Registry (ECR). For more information see:

* [Getting started with ECR](https://aws.amazon.com/ecr/getting-started/)
* [Getting started with ECS](https://aws.amazon.com/ecs/getting-started/)
