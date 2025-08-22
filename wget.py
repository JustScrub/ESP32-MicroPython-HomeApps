import socket

def extract_url_parts(url):
    host = url
    port = None
    path = "/"
    
    # Remove protocol prefix
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]

    # Find path start
    index = url.find("/")
    if index != -1:
        host = url[:index]
        path = url[index:]
    # Find port if specified
    index = host.find(":")
    if index != -1:
        port = int(host[index + 1:])
        host = host[:index]
    return host, port, path

def http_get(host, port, use_ssl, path="/", timeout=0):
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    if timeout > 0:
        s.settimeout(timeout)
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

def wget(url, port=None, O="*", use_ssl=True, content_only=True, t=1, T=0):
    host, port, path = extract_url_parts(url)
    port = port if port else (443 if use_ssl else 80)

    while True:
        try:
            response = http_get(host, port, use_ssl, path, timeout=T)
            break
        except Exception as e:
            print(f"Error: {e}")
            t -= 1
            if t == 0:
                print("Failed to retrieve the URL after retries.")
                return

    if content_only:
        header_end = response.find(b"\r\n\r\n") + 4
        response = response[header_end:]
    if O == "-":
        print(response.decode())
    elif O == "*":
        return response
    else:
        with open(O, "wb") as f:
            f.write(response)