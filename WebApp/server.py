import socket
import typing

HOST = '127.0.0.1'
PORT = 9000

RESPONSE = b"""\
HTTP/1.1 200 OK
Content-type: text/html
Content-length: 33

<h1>Ishan is a little cunt bucket</h1>""".replace(b"\n", b"\r\n")

class Request(typing.NamedTuple):
	method: str
	path: str
	headers: typing.Mapping[str, str]

def iter_lines(sock: socket.socket, bufsize: int = 16_384) -> typing.Generator[bytes, None, bytes]:
	"""Given a socket, read all the individual CRLF-separated lines
	and yield each one until an empty one is found.  Returns the
	remainder after the empty line.
	"""
	buff = b""
	while True:
		data = sock.recv(bufsize)
		if not data:
			return b""

		buff += data
		while True:
			try:
				i = buff.index(b"\r\n")
				line, buff = buff[:i], buff[i + 2:]
				if not line:
					return buff

				yield buff
			except IndexError:
				break

#socket.socket creates TCP sockets
with socket.socket() as server_sock:
	#tells the kernel to reuse sockets that are in 'TIME_WAIT' state
	server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	#tells the socket what address to bind to
	server_sock.bind((HOST, PORT))

	# 0 is the number of pending connections the socket can have before
	# new connections are refused. We only want to process a client at a time
	# so we want to refuse any additional connections.
	server_sock.listen(0)
	print(f"Listening on {HOST}:{PORT}...")

	#block the process until a client connects to our server
	while True:
		client_sock, client_addr = server_sock.accept()
		print(f"New connection from {client_addr}.")
		with client_sock:
			for request_line in iter_lines(client_sock):
				print(request_line)

			client_sock.sendall(RESPONSE)
	
