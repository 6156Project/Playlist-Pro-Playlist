from flask import Flask, Response, request
from datetime import datetime
import json
import rest_utils
from service_factory import ServiceFactory
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import boto3
import os

# load environment variables fron .env
load_dotenv()

# Create the Flask application object.
application = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(application)

service_factory = ServiceFactory()

@application.after_request
def after_request(rsp):
    try:
        print("[Playlist-Pro-Playlist] Working with this response")
        print(rsp)

        # Init an SNS client with boto3 and grab secrets from GitHub env
        # Can refactor this to init client somewhere else to improve latency
        sns_client = boto3.client(
            "sns",
            aws_access_key_id=os.environ.get("SNS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("SNS_SECRET_KEY"),
            region_name=os.environ.get("SNS_REGION")
        )

        string_rsp = rsp.get_data(as_text=True)
        data = json.loads(string_rsp)
        body = data["body"]
        if type(body) == list:
            print("[Playlist-Pro-Playlist] Processing get playlist requests")
            for x in body:
                x["request_type"] = "GET"
                print(x)
                # x look like this == {'id': '122784986734896795025413090857960306787', 'name': 'UpdateTest'}
                sns_client.publish(
                    TargetArn=os.environ.get("SNS_ARN"),
                    Message=json.dumps({"default": json.dumps(x)}),
                    MessageStructure="json"
                )
        elif type(body) == dict:
            print("[Playlist-Pro-Playlist] Processing create playlist requests")
            x = body
            x["request_type"] = "POST"
            print(x)
            # x look like this == {'id': '122784986734896795025413090857960306787', 'name': 'UpdateTest'}
            sns_client.publish(
                TargetArn=os.environ.get("SNS_ARN"),
                Message=json.dumps({"default": json.dumps(x)}),
                MessageStructure="json"
            )
        print("[Playlist-Pro-Playlist] Processed after_request")
    except Exception as ex:
        print("[Playlist-Pro-Playlist] Exception occurred on after_request")
        print(ex)
    return rsp

@application.route("/api/playlists/health", methods=["GET"])
def get_health():
    msg = {
        "name": "Playlist Microservice",
        "health": "Good",
        "at time": str(datetime.now()),
        "body": {
            "id": "1234567890",
            "name": "TestingName"
        }
    }
    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp

# /playlists
@application.route('/api/<resource_collection>', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def do_resource_collection(resource_collection):
    request_inputs = rest_utils.RESTContext(request, resource_collection)
    svc = service_factory.get(resource_collection, None)

    if request_inputs.method == "GET":
        res = svc.get_by_template(template=request_inputs.args,
                                  field_list=request_inputs.fields)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    elif request_inputs.method == "POST":
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