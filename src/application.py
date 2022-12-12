from flask import Flask, Response, request
from datetime import datetime
import json
import rest_utils
from service_factory import ServiceFactory
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv

# load environment variables fron .env
load_dotenv()

# Create the Flask application object.
application = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(application)

service_factory = ServiceFactory()


@application.route("/api/playlists/health", methods=["GET"])
def get_health():
    msg = {
        "name": "Playlist Microservice",
        "health": "Good",
        "at time": str(datetime.now())
    }
    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp

# /playlists
@application.route('/api/<resource_collection>', methods=['POST', 'OPTIONS'])
@cross_origin()
def do_resource_collection(resource_collection):
    request_inputs = rest_utils.RESTContext(request, resource_collection)
    svc = service_factory.get(resource_collection, None)

    if request_inputs.method == "POST":
        res = svc.create_resource(resource_data=request_inputs.data)
        rsp = Response(json.dumps(res), status=res['status'], content_type="application/json")
    elif request_inputs.method == "OPTIONS":
        rsp = Response("Options", status=200, content_type="application/json")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")

    return rsp

# playlists get info, update, delete
@application.route("/api/playlists/<id>", methods=["GET", "PUT", "DELETE", "OPTIONS"])
@cross_origin()
def getPlaylist(id):
    request_inputs = rest_utils.RESTContext(request, id)
    svc = service_factory.get("playlists", None)

    if request_inputs.method == "GET":
        res = svc.get_resource_by_id(id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    elif request_inputs.method == "PUT":
        res = svc.update_resource(id, resource_data=request_inputs.data)
        rsp = Response(json.dumps(res), status=res['status'], content_type="application/json")
    elif request_inputs.method == "DELETE":
        res = svc.delete_resource(id)
        rsp = Response(json.dumps(res), status=res['status'], content_type="application/json")
    elif request_inputs.method == "OPTIONS":
        rsp = Response("Options", status=200, content_type="application/json")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")

    return rsp

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5011)