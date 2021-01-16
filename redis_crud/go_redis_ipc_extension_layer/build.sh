GOOS=linux GOARCH=amd64 go build -o bin/extensions/go-redis-ipc-extension-layer main.go
chmod +x bin/extensions/go-redis-ipc-extension-layer
FL=bin/extensions/.DS_Store
rm -f bin/extensions/.DS_Store
cd bin
zip -r extension.zip extensions/