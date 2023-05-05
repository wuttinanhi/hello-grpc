package main

import (
	"context"
	"flag"
	"io"
	"log"
	"time"

	pb "hello-grpc/helloworld"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

const (
	defaultName = "world"
)

var (
	addr = flag.String("addr", "localhost:50051", "the address to connect to")
	name = flag.String("name", defaultName, "Name to greet")
)

func main() {
	flag.Parse()
	// Set up a connection to the server.
	conn, err := grpc.Dial(*addr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewGreeterClient(conn)

	// Contact the server and print out its response.
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	r, err := c.SayHello(ctx, &pb.HelloRequest{Name: *name})
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	log.Printf("Greeting: %s", r.GetMessage())

	ctx, cancel = context.WithCancel(context.Background())
	defer cancel()
	reply, err := c.SayHelloStreamReply(ctx, &pb.HelloRequest{Name: *name})
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}

	for {
		r, err := reply.Recv()
		if err != nil {
			if err == io.EOF {
				log.Println("stream end")
				break
			}

			log.Fatalf("could not greet: %v", err)
		}
		log.Printf("Stream reply: %s", r.GetMessage())
	}
}
