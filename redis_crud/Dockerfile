FROM public.ecr.aws/lambda/python:3.8

COPY redis_crud/app.py   ./
COPY python_redis_proxy_layer/python/redis_proxy.py ./redis_proxy.py
RUN pip3 install requests
WORKDIR /opt
RUN mkdir extensions
WORKDIR /opt/extensions
COPY go_redis_ipc_extension_layer/bin/extensions/go-redis-ipc-extension-layer go-redis-ipc-extension-layer
RUN chmod u+x go-redis-ipc-extension-layer
RUN mkdir python
WORKDIR /opt/extensions/python
COPY python_redis_proxy_layer/python/redis_proxy.py redis_proxy.py 
COPY python_redis_proxy_layer/python/requirements.txt requirements.txt 
ENV API_URI="https://pu65bkndtvahlfy5nvhs5vzuhq.appsync-api.us-west-2.amazonaws.com/graphql"
ENV API_KEY="da2-scoukebkyzcbrd5mwc7zswe7bm"

CMD ["app.lambda_handler"]  