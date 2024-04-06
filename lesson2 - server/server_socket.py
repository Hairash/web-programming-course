import socket


def handle_request(client_socket):
    """Handles a single HTTP request received from the client."""
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")

    # This is a very basic HTTP response. A real server should send proper HTTP headers.
    http_response = """\
HTTP/1.1 200 OK

<html>
<head title="New">
</head>
<body style="color:red">
Hello, World! This is a very simple HTTP server.
</body>
</html>
"""
    client_socket.sendall(http_response.encode('utf-8'))
    client_socket.close()


def simple_http_server(host='127.0.0.1', port=8080):
    """A very simple HTTP server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Listening on {host}:{port}...")

        while True:
            # Accept a connection from a client
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            handle_request(client_socket)


if __name__ == '__main__':
    simple_http_server()
