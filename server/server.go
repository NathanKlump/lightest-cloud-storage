package main

import (
    "fmt"
    "log"
    "net/http"
)

func handler ( writer http.ResponseWriter, response *http.Request ) {
	fmt.Fprint(writer, "hey there: ", response.URL.Path[1:])
}

func main() {
	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
