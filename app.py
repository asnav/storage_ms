from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import uuid

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        filepath = "files"+self.path+".jpeg"
        if os.path.exists(filepath):
            self.send_response(200, 'OK')
            self.send_header('Content-type','image/jpeg')
            self.end_headers()
            with open(filepath, 'rb') as img:
                self.wfile.write(bytes(img.read()))
        else:
            self.send_response(404, "file not found")
            self.end_headers()

    def do_POST(self):
        file_length = int(self.headers['Content-Length'])
        if file_length == 0:
            self.send_response(401, 'Bad Request')
            self.end_headers()
        else:
            self.send_response(201, 'Created')
            self.send_header('Content-type','text/html')
            self.end_headers()
            id = str(uuid.uuid1())
            while os.path.exists("files"+id+".jpeg"):
                id = str(uuid.uuid1())
            with open("files/"+id+".jpeg", 'wb') as img:
                img.write(self.rfile.read(file_length))
            self.wfile.write(bytes(id, "utf8"))
        
    def do_PUT(self):
        file_length = int(self.headers['Content-Length'])
        if not os.path.exists("files"+self.path+".jpeg"):
            self.send_response(404, "file not found")
            self.end_headers()
        elif file_length == 0:
            self.send_response(401, 'Bad Request')
            self.end_headers()
        else:
            self.send_response(204, 'No Content')
            self.end_headers()
            with open("files/"+self.path+".jpeg", 'wb') as img:
                img.write(self.rfile.read(file_length))

    def do_DELETE(self):
        if os.path.exists("files"+self.path+".jpeg"):
            self.send_response(204, 'No Content')
            self.end_headers()
            os.remove("files"+self.path+".jpeg")
        else:
            self.send_response(404, "File Not Found")
            self.end_headers()

with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()