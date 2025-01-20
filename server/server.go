// main.go
package main

import (
	"fmt"
	"html/template"
	"net/http"
	"time"
)

type PageData struct {
	Count int
}

func main() {
	// Initialize counter
	count := 0

	// Serve static files
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	// Main page handler
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		tmpl := template.Must(template.ParseFiles("client/index.html"))
		data := PageData{Count: count}
		tmpl.Execute(w, data)
	})

	// Increment counter endpoint
	http.HandleFunc("/increment", func(w http.ResponseWriter, r *http.Request) {
		count++
		// Add a small delay to make the update visible
		time.Sleep(100 * time.Millisecond)
		fmt.Fprintf(w, "<div id='count'>%d</div>", count)
	})

	fmt.Println("Server starting on :8080...")
	http.ListenAndServe(":8080", nil)
}
