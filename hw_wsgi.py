import urlparse

def application(environ, start_response):
    data = "Hello, world\n\nGET:\n"
    getQuery = urlparse.parse_qs(environ['QUERY_STRING'])
    for key in getQuery.keys():
        for param in getQuery[key]:
	    data += key + ' = ' + param + '\n'
    data += "\nPOST:\n"
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
	request_body_size = 0
    postQuery = urlparse.parse_qs(environ['wsgi.input'].read(request_body_size))
    for key in postQuery.keys():
        for param in postQuery[key]:
	    response_body += key + ' = ' + param + '\n'
    start_response("200 OK", [
    ("Content-Type", "text/plain"),
    ("Content-Length", str(len(data))),
    ])
    return data
