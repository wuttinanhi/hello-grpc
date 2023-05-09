#!/bin/sh

# python -m grpc_tools.protoc -I../protos --python_out=. --pyi_out=. --grpc_python_out=. ../protos/helloworld.proto
# protoc -I../protos --python_out=. --pyi_out=. --grpc_python_out=. ../protos/helloworld.proto
# --plugin=grpc_python_plugin --python_out=grpc/helloworld --grpclib_python_out=grpc/helloworld

rm -rf ./helloworld
mkdir -p ./helloworld
# echo "" > ./helloworld/__init__.py
# protoc -I../protos --python_out=./helloworld --pyi_out=./helloworld ../protos/helloworld.proto

# python -m grpc_tools.protoc \
#     -I../protos \
#     --python_out=./helloworld \
#     --pyi_out=./helloworld \
#     --grpc_python_out=./helloworld \
#     ../protos/helloworld.proto

echo -e "import sys\nfrom pathlib import Path\nsys.path.append(str(Path(__file__).parent))" > ./helloworld/__init__.py

python -m grpc_tools.protoc \
	  --python_out ./helloworld \
	  --grpc_python_out ./helloworld \
	  --proto_path ../protos \
	  ../protos/helloworld.proto
