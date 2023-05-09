""" gRPC server """

from concurrent import futures
import logging
import time
from typing import Iterable

import grpc

from helloworld import helloworld_pb2, helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(
        self,
        request: helloworld_pb2.HelloRequest,
        context: grpc.ServicerContext
    ) -> helloworld_pb2.HelloReply:
        return helloworld_pb2.HelloReply(message=f'Hello, {request.name}!')

    def SayHelloStreamReply(
        self,
        request: helloworld_pb2.HelloRequest,
        context: grpc.ServicerContext
    ) -> Iterable[helloworld_pb2.HelloReply]:
        print(f'got request: {request.name}')
        for _ in range(10):
            yield helloworld_pb2.HelloReply(message=f'Hello, {request.name}!')
            time.sleep(1)


def serve():
    port = '50051'

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(
        Greeter(), server)

    server.add_insecure_port('[::]:' + port)
    server.start()

    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
