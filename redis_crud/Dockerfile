# Python base image 
FROM public.ecr.aws/lambda/python:3.8

# Copy and setup the app code
COPY redis_crud/app.py ./
RUN pip3 install requests

# Setup the Redis Extension
WORKDIR /opt
RUN mkdir extensions
WORKDIR /opt/extensions
COPY go_redis_ipc_extension_layer/bin/extensions/go-redis-ipc-extension-layer go-redis-ipc-extension-layer
RUN chmod u+x go-redis-ipc-extension-layer

# Setup the links to the Redis backend
ENV API_URI=<url for graphql endpoint>
ENV API_KEY=<key for graphql endpoint>
ENV SQS_QUEUE_NAME=<name for SQS queue>
ENV AWS_ACCESS_KEY_ID=<aws access key>
ENV AWS_SECRET_ACCESS_KEY=<aws secret access key>
ENV AWS_REGION=<aws region>

# Setup the Python Redis client layer
RUN mkdir /opt/python
WORKDIR /opt/python
COPY python_redis_proxy_layer/python/redis_proxy.py redis_proxy.py 
COPY python_redis_proxy_layer/python/requirements.txt requirements.txt

# Setup the web entery point
WORKDIR /usr/local/bin/
COPY aws-lambda-rie aws-lambda-rie

# Entry point to the function
CMD ["app.lambda_handler"]
