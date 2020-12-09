
import sys
import os
import datetime
import hashlib
from flask import Flask, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy

try:
    from flask_admin import Admin
    from flask_admin.contrib import sqla
except:
    print("Failed to import flask-admin")
from safrs import SAFRSAPI  # api factory
from safrs import SAFRSBase  # db Mixin
from safrs import SAFRSFormattedResponse
from safrs import jsonapi_attr
from safrs import jsonapi_rpc  # rpc decorator
from safrs.api_methods import startswith  # rpc methods
from functools import wraps
from flask_cors import CORS

# This html will be rendered in the swagger UI
description = """
<a href=http://jsonapi.org>Json:API</a> compliant API built with https://github.com/thomaxxl/safrs <br/>
- <a href="https://github.com/thomaxxl/safrs/blob/master/examples/demo_pythonanywhere_com.py">Source code of this page</a><br/>
- <a href="/ja/index.html">reactjs+redux frontend</a>
- <a href="/admin/person">Flask-Admin frontend</a>
- Auto-generated swagger spec: <a href=/api/swagger.json>swagger.json</a><br/>
- <a href="/swagger_editor/index.html?url=/api/swagger.json">Swagger2 Editor</a> (updates can be added with the SAFRSAPI "custom_swagger" argument)
"""
db = SQLAlchemy()


def test_decorator(f):
    @wraps(f)
    def fwrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        result.status_code = 200
        #result.headers['Location'] = 'https://blah/bleh'
        #result.data = json.dumps({'hoho' : 'ddd' })
        return result
    return fwrapper


# SQLAlchemy Mixin Superclass with multiple inheritance


class BaseModel(SAFRSBase, db.Model):
    __abstract__ = True



class Message(BaseModel):
    """ description: data base for messages """
    __tablename__ = "Messages"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    fromId = db.Column(db.Integer)
    toId = db.Column(db.Integer)
    send_time = db.Column(db.DateTime, default=datetime.datetime.now())
    pm = db.Column(db.Boolean, default = False)

    custom_decorators = [test_decorator]

    def __str__(self):
        return f'{self.message}'

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getMessagesInPm(cls, *args, **some_body_key):
        """
                  description :     getMessagesInPm between two ids
                  summary: getMessagesInPm
                  responses:
                      200:
                          description: "Good10"
                          schema:
                             {
                                  "type":"object",
                                  "properties":{
                                      "meta":{
                                              "type":"object",
                                              "properties":{
                                                  "result":{
                                                      "type":"object",
                                                      "properties":{
                                                          "id":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          "fromId":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          "toId":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          "send_time":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          "message":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          }
                                                      }
                                                  }
                                          }
                                  }
                              }
              """
        toId = some_body_key['varargs'].split()[0]
        fromId = some_body_key['varargs'].split()[1]
        content = {"id": [], "fromId": [], "toId": [], "send_time": [], "message": []}
        for msg in db.session.query(Message).filter_by(toId=toId, fromId=fromId, pm = True).all():
            content["id"].append(str(msg.id))
            content["fromId"].append(str(msg.fromId))
            content["toId"].append(str(msg.toId))
            content["send_time"].append(str(msg.send_time))
            content["message"].append(str(msg.message))

        db.session.query(Message).filter_by(toId=toId, fromId=fromId, pm = True).delete()
        db.session.commit()

        return content



    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getMessagesByUserID(cls, *args, **some_body_key):
        """
                  description : Enter to varargs name
                  summary: GetMessagesByUserID
                  responses:
                      200:
                          description: "Good"
                          schema:
                             {
                                  "type":"object",
                                  "properties":{
                                      "meta":{
                                              "type":"object",
                                              "properties":{
                                                  "result":{
                                                      "type":"object",
                                                      "properties":{
                                                          "id":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          "fromId":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          "toId":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          "send_time":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          "message":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          }
                                                      }
                                                  }
                                          }
                                  }
                              }
              """


        content = {"id": [], "fromId": [], "toId": [], "send_time": [], "message": []}
        for msg in db.session.query(Message).filter_by(toId=some_body_key['varargs'] , pm = False).all():
            content["id"].append(str(msg.id))
            content["fromId"].append(str(msg.fromId))
            content["toId"].append(str(msg.toId))
            content["send_time"].append(str(msg.send_time))
            content["message"].append(str(msg.message))

        db.session.query(Message).filter_by(toId=some_body_key['varargs'], pm = False).delete()
        db.session.commit()

        return content


class User(BaseModel):
    """
        description: My user description
    """

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    online = db.Column(db.Boolean, default = False)

    def __str__(self):
        return f'{self.login}'


    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def GetAuthenticationStatus(cls, *args, **some_body_key):
        """
            description : Enter to varargs user name
            summary: GetAuthenticationStatus
            responses:
                200:
                    description: "Good"
                    schema:
                       {
                            "type":"object",
                            "properties":{
                                "meta":{
                                        "type":"object",
                                        "properties":{
                                            "result":{
                                                "type":"object",
                                                "properties":{
                                                        "result":"string",
                                                    }
                                                }
                                            }
                                    }
                            }
                        }
        """
        login = some_body_key['varargs'].split()[0]
        password = some_body_key['varargs'].split()[1]
        user = db.session.query(User).filter_by(login=login, password=password).first()
        if user is not None:
            user.online = True
            db.session.commit()
            return {"result": "success"}
        return {"result": "failed"}


    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def Logout(cls, *args, **some_body_key):
        """
            description :  Logout user
            summary: Logout
            responses:
                200:
                    description: "Good4"
                    schema:
                       {
                            "type":"object",
                            "properties":{
                                "meta":{
                                        "type":"object",
                                        "properties":{
                                            "result":{
                                                "type":"object",
                                                "properties":{
                                                        "result":"string",
                                                    }
                                                }
                                            }
                                    }
                            }
                        }
        """
        login = some_body_key['varargs']
        user = db.session.query(User).filter_by(login=login).first()
        if user is not None:
            user.online = False
            db.session.commit()
            return {"result": "success"}
        return {"result": "failed"}

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getAllOnlineUsers(cls, *args, **some_body_key):
        """
                  description : gett list of online users
                  summary: getAllOnlineUsers
                  responses:
                      200:
                          description: "Good7"
                          schema:
                             {
                                  "type":"object",
                                  "properties":{
                                      "meta":{
                                              "type":"object",
                                              "properties":{
                                                  "result":{
                                                      "type":"object",
                                                      "properties":{
                                                          "users":{
                                                                  "type":"array",
                                                                  "items":"string"
                                                              },
                                                          }
                                                      }
                                                  }
                                          }
                                  }
                              }
              """
        content = {"users": []}
        for user in db.session.query(User).filter_by(online=True).all():
            content["users"].append(str(user.login))
        return content

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getIdByLogin(cls, *args, **some_body_key):
        """
            description : get Id By Login
            summary: getIdByLogin
            responses:
                200:
                    description: "Good3"
                    schema:
                       {
                            "type":"object",
                            "properties":{
                                "meta":{
                                        "type":"object",
                                        "properties":{
                                            "result":{
                                                "type":"object",
                                                "properties":{
                                                        "result":"string",
                                                    }
                                                }
                                            }
                                    }
                            }
                        }
        """
        if db.session.query(User).filter_by(login=some_body_key['varargs']).first() is not None:
            id = db.session.query(User).filter_by(login=some_body_key['varargs']).first().id
            return {"result": str(id)}

        return {"result": "success"}

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getLoginById(cls, *args, **some_body_key):
        """
            description : get Login by id
            summary: getLoginById
            responses:
                200:
                    description: "Good4"
                    schema:
                       {
                            "type":"object",
                            "properties":{
                                "meta":{
                                        "type":"object",
                                        "properties":{
                                            "result":{
                                                "type":"object",
                                                "properties":{
                                                        "result":"string",
                                                    }
                                                }
                                            }
                                    }
                            }
                        }
        """
        if db.session.query(User).filter_by(id=int(some_body_key['varargs'])).first() is not None:
            login = db.session.query(User).filter_by(id=int(some_body_key['varargs'])).first().login
            return {"result": login}

        return {"result": "success"}

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def AddUser(cls, *args, **some_body_key):
        """
            description : add user to db
            summary: AddUser
            responses:
                200:
                    description: "Good2"
                    schema:
                       {
                            "type":"object",
                            "properties":{
                                "meta":{
                                        "type":"object",
                                        "properties":{
                                            "result":{
                                                "type":"object",
                                                "properties":{
                                                        "result":"string",
                                                    }
                                                }
                                            }
                                    }
                            }
                        }
        """
        login = some_body_key['varargs'].split()[0]
        password = some_body_key['varargs'].split()[1]
        if db.session.query(User).filter_by(login=login).first() is not None:
            return {"result": "failed"}
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        return {"result": "success"}

    @classmethod
    @jsonapi_rpc(http_methods=['POST'])
    def SendMessages(cls, fromId, toId, message, pm):
        """
        args:
            fromId: fromID
            toId: toId
            message: message
            pm: pm
        """

        message = Message(fromId = fromId, toId = toId, message = message, pm = pm)
        db.session.add(message)
        db.session.commit()
        return {"result": "success"}




def start_api(swagger_host="127.0.0.1", PORT=None):

    SAFRSBase.db_commit = False

    with app.app_context():
        db.init_app(app)
        db.create_all()
        userAdmin = User(login = "admin", password = "admin")
        db.session.add(userAdmin)
        db.session.commit()

        custom_swagger = {
            "info": {"title": "Chat"},
        }  # Customized swagger will be merged

        api = SAFRSAPI(
            app,
            host=swagger_host,
            port=PORT,
            prefix=API_PREFIX,
            custom_swagger=custom_swagger,
            schemes=["http"],
            description=description,
        )

        for model in [User, Message]:
            # Create an API endpoint
            api.expose_object(model)

        # see if we can add the flask-admin views
        try:
            admin = Admin(app, url="/admin")
            for model in [User, Message]:
                admin.add_view(sqla.ModelView(model, db.session))
        except Exception as exc:
            print(f"Failed to add flask-admin view {exc}")


API_PREFIX = "/api"  # swagger location
app = Flask("Chat Api", template_folder="/home/thomaxxl/mysite/templates")

app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///", DEBUG=False)  # DEBUG will also show safrs log messages + exception messages

@app.route("/")
def goto_api():
    return redirect(API_PREFIX)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5000
    start_api(HOST, PORT)
    CORS(app)
    app.run(host=HOST, port=PORT, threaded=False)