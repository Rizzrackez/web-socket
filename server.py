import socket
from views import *
from database_query import *

# Urls address list.
URLS = {
    '/': home_page,
    '/correct_page': correct_page,
    '/send_message': send_message,
    '/all_messages': view_messages,
}


# Request parser. Returns a HTTP method and url address request. If HTTP method = 'POST' calls a insert_data function.
def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]

    if method == 'POST':
        insert_data(request)

    return method, url


# HTTP headers generator. Returns a HTTP status code and request code.
def generate_headers(method, url):

    if not url in URLS:
        return 'HTTP/1.1 404 Page not found\n\n', 404

    return 'HTTP/1.1 200 OK\n\n', 200


# HTML tag generator. Returns a HTML code.
def generate_content(code, url, method, request):
    if code == 404:
        return '<h1>404 PAGE NOT FOUND</h1>'

    if code == 405:
        return '<h1>405 METHOD NOT ALLOWED</h1>'

    return URLS[url](method)


# Response generator. Returns HTTP status code and HTML code in bytes.
def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url, method, request)
    return (headers + body).encode()


# Starts the server, keeps it active, gets a requests and send responses.
def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        try:
            response = generate_response(request.decode('utf-8'))
            client_socket.sendall(response)
        except:
            pass
        client_socket.close()


if __name__ == '__main__':
    print('-------------')
    print('Server start!')
    print('-------------')
    print('Connection to database lab10_db!\n\n')
    run()
