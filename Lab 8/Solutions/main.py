from flask import Flask
from flask_restful import Api, Resource
from collections import defaultdict
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
# from safrs import SAFRSAPI, SAFRSRestAPI  # api factory




app = Flask(__name__)
CORS(app)
api = Api(app)
messagesDictionary = defaultdict(list)

SWAGGER_URL = '/swagger'
API_URL = 'main.py'
swaggeruiBlueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"app_name": "name"})
app.register_blueprint(swaggeruiBlueprint, url_prefix=SWAGGER_URL)
# swaggerApi = SAFRSAPI(app, host="0.0.0.0", port=None, prefix=SWAGGER_URL)


class GetMessagesOfClient(Resource):
    def get(self, userId):
        returnData = messagesDictionary[str(userId)]
        messagesDictionary[str(userId)] = []
        return {"messages": returnData}

class SendMessagesToClient(Resource):
    def post(self, userId, message):
        messagesDictionary[str(userId)].append(message)
        return {"result": "Wysłanie powiodło się"}

api.add_resource(GetMessagesOfClient, "/get/<int:userId>")
api.add_resource(SendMessagesToClient, "/send/<int:userId>/<string:message>")


if __name__ == '__main__':
    app.run()


