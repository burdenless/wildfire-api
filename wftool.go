/////////////
//
// WFTool
// WildFire API tool written in Go
//
// Developed by: Byt3smith
//
/////////////

package main

import (
	"fmt"
	"github.com/jmcvetta/napping"
)

var BASE_URL = "https://wildfire.paloaltonetworks.com/publicapi/"
var API_KEY = ""
var SAMPLE = "a1f79a4108555cb1e163119d00c5444b"

type Foo struct {
	md5 string
  apikey string
}


type ResponseUserAgent struct {
	Useragent string `json:"user-agent"`
}

// A Params is a map containing URL parameters.
type Params map[string]string


func main() {

	// Start Session
	s := napping.Session{}
  url := BASE_URL + "get/sample"
	fmt.Println("URL:>", url)

	fmt.Println("--------------------------------------------------------------------------------")
	println("")

	fooParams := napping.Params{"md5": SAMPLE, "apikey": API_KEY}
	p := fooParams

	res := ResponseUserAgent{}
	resp, err := s.Post(url, &p, &res, nil)
	if err != nil {
    fmt.Println("Error in request")
	}
	//
	// Process response
	//
	println("")
	fmt.Println("response Status:", resp.Status())
	fmt.Println("--------------------------------------------------------------------------------")
	fmt.Println("Header")
	fmt.Println(resp.HttpResponse().Header)
	fmt.Println("--------------------------------------------------------------------------------")
	fmt.Println("RawText")
	fmt.Println(resp.RawText())
	println("")
}
