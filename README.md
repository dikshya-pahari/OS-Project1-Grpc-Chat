# **Group Chat System - Distributed RPC Communication**

## **📌 Project Overview**

This is a **distributed group chat system** implemented using **gRPC in Python**. The system follows a **client-server model**, where multiple clients communicate asynchronously through a **central server**. The project is fully **containerized with Docker** for easy deployment and testing.

## **📂 Project Structure**

```
📁 grpc-chat
 ├── Dockerfile          # Docker configuration file
 ├── server.py           # Server-side implementation
 ├── client.py           # Client-side implementation
 ├── chat.proto          # gRPC service definitions
 ├── run_test_1.py       # Automated test script
 ├── README.md           # Project documentation
```

## **🛠️ Setup & Installation**

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/your-repo/grpc-chat.git
cd grpc-chat
```

### **2️⃣ Generate gRPC Code**

Before running the project, generate the necessary gRPC Python files:

```sh
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
```

### **3️⃣ Build the Docker Image**

```sh
docker build -t grpc-chat .
```

### **4️⃣ Run the Container**

To start the test automatically inside the container:

```sh
docker run --rm grpc-chat
```

To manually run the **server** and **clients**:

```sh
# Start the server
docker run --rm -it grpc-chat python3 server.py -client_ids 1,2,3 -port 50051
```

```sh
# Start a client (Alice)
docker run --rm -it grpc-chat python3 client.py -client_id 1 -server_ip localhost -port 50051 -message "Hello from Alice!"
```

## **🧪 Testing Scenarios**

The `run_test_1.py` script simulates real-world scenarios: 1️⃣ **Alice sends a message before Bob and Chad join.**\
✅ Expected: Bob and Chad receive Alice’s message when they come online.

2️⃣ **Bob sends a message when all are online.**\
✅ Expected: Alice and Chad receive it, but Bob does not.

3️⃣ **Doug (unauthorized) joins the server.**\
✅ Expected: Doug does not receive any messages.

To run the test:

```sh
python run_test_1.py
```

## **🚀 Future Improvements**

- **Message Persistence**: Store messages in a database instead of memory.
- **User Authentication**: Secure access with authentication tokens.
- **Group Customization**: Allow users to create chat rooms dynamically.
- **Logging**: Add structured logging for better debugging.

## **📌 Contributors**

- Dikshya Pahari
- University of Pittsburgh, PA (MSCS)


