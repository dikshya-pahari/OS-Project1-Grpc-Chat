import grpc
import asyncio
from concurrent import futures
import chat_pb2
import chat_pb2_grpc
import argparse

class ChatServer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self, client_ids):
        self.messages = []  # Stores (client_id, message)
        self.clients = {cid: 0 for cid in client_ids}  # Tracks last read index per client

    async def SendMessage(self, request, context):
        self.messages.append((request.client_id, request.message))
        print(f"Message from Client {request.client_id}: {request.message}")
        return chat_pb2.Empty()

    async def GetMessages(self, request, context):
        if request.client_id not in self.clients:
            return chat_pb2.MessageList(messages=[])
        
        last_read = self.clients[request.client_id]
        new_messages = [chat_pb2.ChatMessage(client_id=cid, message=msg)
                        for i, (cid, msg) in enumerate(self.messages[last_read:], last_read)
                        if cid != request.client_id]
        
        self.clients[request.client_id] = len(self.messages)
        return chat_pb2.MessageList(messages=new_messages)

async def serve(client_ids, port):
    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServer(client_ids), server)
    server.add_insecure_port(f'[::]:{port}')
    await server.start()
    print(f"Server started on port {port} with clients {client_ids}")
    await server.wait_for_termination()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-client_ids', type=str, required=True, help='Comma-separated client IDs')
    parser.add_argument('-port', type=int, required=True, help='Server port')
    args = parser.parse_args()

    client_ids = list(map(int, args.client_ids.split(',')))
    asyncio.run(serve(client_ids, args.port))
