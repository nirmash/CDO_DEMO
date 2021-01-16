package ipc

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

func post(url string, jsonData string, secret string) string {
	var jsonStr = []byte(jsonData)
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonStr))
	req.Header.Set("Content-Type", "application/graphql")
	req.Header.Set("x-api-key", secret)

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	fmt.Println("response Status:", resp.Status)
	fmt.Println("response Headers:", resp.Header)
	body, _ := ioutil.ReadAll(resp.Body)
	return string(body)
}

func makeGraphQlCommand(cmd string) string {
	innerStr := "query { getRedis(Command: ##token## ) }"
	res := strings.Split(cmd, " ")
	j, _ := json.Marshal(res)
	innerObj := strings.Replace(innerStr, "##token##", string(j), -1)
	j2, _ := json.Marshal(innerObj)
	mtstr := `{ "query" : ##token## }`
	qVal := strings.Replace(mtstr, "##token##", string(j2), -1)
	return qVal
}

// Start begins running the sidecar
func Start(port string) {
	go startHTTPServer(port)
}

func writeToFileSystem(filename string, data string) {
	file, err := os.Create(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	_, err = io.WriteString(file, data)
	if err != nil {
		panic(err)
	}
	err = file.Sync()
	if err != nil {
		panic(err)
	}
}
func startHTTPServer(port string) {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		command, err := ioutil.ReadAll(r.Body)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		jsonCmd := makeGraphQlCommand(string(command))
		fmt.Fprintf(w, "Command: %s", post(os.Getenv("API_URI"), jsonCmd, os.Getenv("API_KEY")))
	})
	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		panic(err)
	}
}
