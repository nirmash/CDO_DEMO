rm redis_lib.zip
rm python/.DS_Store
zip -r redis_lib.zip python/
aws lambda publish-layer-version --layer-name "python-redis-proxy-layer" --zip-file  "fileb://redis_lib.zip"