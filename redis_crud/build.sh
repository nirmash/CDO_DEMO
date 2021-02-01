cd go_redis_ipc_extension_layer
pwd
./build.sh
cd ..
sam build
sam deploy --stack-name key-log-redis --region us-west-2 --no-confirm-changeset --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-135zhihkdzt7i --s3-prefix key-log-redis

