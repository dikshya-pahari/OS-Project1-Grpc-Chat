import grpc
import asyncio
import chat_pb2
import chat_pb2_grpc
import argparse

async def send_message(client_id, server_ip, port, message):
    async with grpc.aio.insecure_channel(f'{server_ip}:{port}') as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        await stub.SendMessage(chat_pb2.ChatMessage(client_id=client_id, message=message))
        print(f"Client {client_id} sent message: {message}")

async def get_messages(client_id, server_ip, port):
    async with grpc.aio.insecure_channel(f'{server_ip}:{port}') as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        response = await stub.GetMessages(chat_pb2.ClientRequest(client_id=client_id))
        for msg in response.messages:
            print(f"Client {msg.client_id} says: {msg.message}")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-client_id', type=int, required=True, help='Client ID')
    parser.add_argument('-server_ip', type=str, required=True, help='Server IP')
    parser.add_argument('-port', type=int, required=True, help='Server port')
    parser.add_argument('-message', type=str, help='Message to send')
    args = parser.parse_args()

    if args.message:
        await send_message(args.client_id, args.server_ip, args.port, args.message)
    await get_messages(args.client_id, args.server_ip, args.port)

if __name__ == '__main__':
    asyncio.run(main())
