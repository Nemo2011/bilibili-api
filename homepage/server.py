from wsgiref.simple_server import make_server
import app

if __name__ == '__main__':
    server = make_server('0.0.0.0', 5000, app.app)
    server.serve_forever()
