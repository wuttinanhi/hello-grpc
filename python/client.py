""" gRPC client """


import logging

import grpc
from helloworld import helloworld_pb2, helloworld_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='world!'))
        print("Greeter client received: " + response.message)

        print("Will try to greet world stream ...")
        response = stub.SayHelloStreamReply(
            helloworld_pb2.HelloRequest(name='world!'))
        for res in response:
            print("Greeter client received: " + res.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
