import socket

def extract_host(url):
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    slash_index = url.find("/")
    if slash_index != -1:
        return url[:slash_index]
    return url

def http_get(host, port, use_ssl, path="/"):
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    if use_ssl:
        import ssl
        s = ssl.wrap_socket(s)
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    s.send(request.encode())
    response = b""
    while True:
        data = s.recv(1024)
        if not data:
            break
        response += data
    s.close()
    return response

def wget(url, port=None, o="-", use_ssl=True, content_only=True, t=1):
    host = extract_host(url)
    port = port if port else (443 if use_ssl else 80)
    path = url[url.find(host) + len(host):] or "/"

    response = http_get(host, port, use_ssl, path)
    if content_only:
        header_end = response.find(b"\r\n\r\n") + 4
        response = response[header_end:]
    if o == "-":
        print(response.decode())
    else:
        with open(o, "wb") as f:
            f.write(response)