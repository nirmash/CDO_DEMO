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
ENV API_URI="https://pu65bkndtvahlfy5nvhs5vzuhq.appsync-api.us-west-2.amazonaws.com/graphql"
ENV API_KEY="da2-scoukebkyzcbrd5mwc7zswe7bm"

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