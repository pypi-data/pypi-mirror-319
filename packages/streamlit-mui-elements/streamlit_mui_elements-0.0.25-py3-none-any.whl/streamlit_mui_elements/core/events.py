import json
from threading import Thread
import tornado.ioloop
import tornado.web

event_store = {}

class DataHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

    def get(self):
        key = self.get_argument('key', None)
        self.write(json.dumps(event_store.get(key, {})))

    def post(self):
        data = json.loads(self.request.body)
        if data:
            key = data.get('key')
            event_store[key] = data 
        else:
            self.set_status(400)
            self.write({"status": "error", "message": "No key provided"})

def make_app():
    return tornado.web.Application([
        (r"/api/data", DataHandler),
    ])

def run_tornado():
    app = make_app()
    app.listen(8500)
    tornado.ioloop.IOLoop.current().start()

def start_event_server():  # keeping the name for compatibility
    server_thread = Thread(target=run_tornado)
    server_thread.start()
