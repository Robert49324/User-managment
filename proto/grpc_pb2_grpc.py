# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import grpc_pb2 as proto_dot_grpc__pb2


class UserServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUser = channel.unary_unary(
            "/grpc.UserService/GetUser",
            request_serializer=proto_dot_grpc__pb2.GetUserRequest.SerializeToString,
            response_deserializer=proto_dot_grpc__pb2.GetUserResponse.FromString,
        )


class UserServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_UserServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetUser": grpc.unary_unary_rpc_method_handler(
            servicer.GetUser,
            request_deserializer=proto_dot_grpc__pb2.GetUserRequest.FromString,
            response_serializer=proto_dot_grpc__pb2.GetUserResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "grpc.UserService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class UserService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUser(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/grpc.UserService/GetUser",
            proto_dot_grpc__pb2.GetUserRequest.SerializeToString,
            proto_dot_grpc__pb2.GetUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )