#!/bin/sh

go build -o server/server server/main.go
./server/server
