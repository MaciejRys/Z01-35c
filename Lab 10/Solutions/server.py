
import datetime
from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib import sqla
from safrs import SAFRSAPI  # api factory
from safrs import SAFRSBase  # db Mixin
from safrs import jsonapi_rpc  # rpc decorator
from flask_socketio import SocketIO, send, emit

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

# SQLAlchemy Mixin Superclass with multiple inheritance


class BaseModel(SAFRSBase, db.Model):
    __abstract__ = True



class Message(BaseModel):
    """
        description: My Message description
    """
    __tablename__ = "Messages"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    fromId = db.Column(db.Integer)
    toId = db.Column(db.Integer, default = -1)
    send_time = db.Column(db.DateTime, default=datetime.datetime.now())
    isRead = db.Column(db.Boolean, default = False)


    def __str__(self):
        return f'{self.message}'
    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getMessagesInChat(cls, *args, **kwargs):
        """
      description: getMessagesInChat
      summary: getMessagesInChat
      responses:
        '200':
          description: OK
          schema:
            type: array
            items:
              type: object
              properties:
                fromId:
                  type: string
                toId:
                  type: string
                send_time:
                  type: string
                  format: date-time
                message:
                  type: string
        """
        content = []
        for msg in db.session.query(Message).filter_by(toId=-1).all():
            object = {"fromId": str(msg.fromId), "toId": str(msg.toId), "send_time": str(msg.send_time), "message": str(msg.message)}
            content.append(object)
        return content

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getMessagesInPm(cls, *args, **kwargs):
        """
      description: getMessagesInPm
      summary: getMessagesInPm
      responses:
        '200':
          description: OK
          schema:
            type: array
            items:
              type: object
              properties:
                fromId:
                  type: string
                toId:
                  type: string
                isRead:
                  type: string
                send_time:
                  type: string
                  format: date-time
                message:
                  type: string
        """
        toId = kwargs['varargs'].split()[0]
        fromId = kwargs['varargs'].split()[1]
        isCallback = kwargs['varargs'].split()[2]
        content = []
        for msg in db.session.query(Message).filter_by(toId=int(toId), fromId=int(fromId)).all():
            object = {"fromId": str(msg.fromId), "toId": str(msg.toId), "isRead": str(msg.isRead),"send_time": str(msg.send_time), "message": str(msg.message)}
            content.append(object)
            msg.isRead = True
        db.session.commit()

        for msg in db.session.query(Message).filter_by(fromId=int(toId), toId=int(fromId)).all():
            object = {"fromId": str(msg.fromId), "toId": str(msg.toId), "isRead": str(msg.isRead), "send_time": str(msg.send_time), "message": str(msg.message)}
            content.append(object)
        db.session.commit()
        if isCallback == "False":
            socketio.emit('refreshMessagesInPMafterGet', {'fromId': fromId, 'toId': toId})
        sortedContent = sorted(content, key=lambda k: k['send_time'])

        return sortedContent

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getNumberOfUnreadMessagesForUser(cls, *args, **kwargs):
        """
      description: getNumberOfUnreadMessagesForUser
      summary: getNumberOfUnreadMessagesForUser
      responses:
        '200':
          description: OK
          schema:
            type: array
            items:
              type: object
              properties:
                fromId:
                  type: string
                send_time:
                  type: string
                  format: date-time
                numberOfMessages:
                  type: string
        """

        toId = kwargs['varargs']
        content =[]

        for msg in db.session.query(Message).filter_by(toId=int(toId)).all():
            if msg.isRead == False:
                if any(x['fromId'] == str(msg.fromId) for x in content):
                    for index, item in enumerate(content):
                        if item['fromId'] == str(msg.fromId):
                            item['numberOfMessages'] = str(int(item['numberOfMessages']) + 1)
                            if msg.send_time > item['send_time']:
                                item['send_time'] = msg.send_time
                else:
                    object = {"fromId": str(msg.fromId), "send_time": msg.send_time, "numberOfMessages": str(1)}
                    content.append(object)
            else:
                if not(any(x['fromId'] == str(msg.fromId) for x in content)):
                    object = {"fromId": str(msg.fromId), "send_time": msg.send_time, "numberOfMessages": str(0)}
                    content.append(object)

        for msg in db.session.query(Message).filter_by(fromId=int(toId)).all():
            if msg.toId != -1:
                if any(x['fromId'] == str(msg.toId) for x in content):
                    for index, item in enumerate(content):
                        if item['fromId'] == str(msg.toId):
                            if msg.send_time > item['send_time']:
                                item['send_time'] = msg.send_time
                else:
                    object = {"fromId": str(msg.toId), "send_time": msg.send_time, "numberOfMessages": str(0)}
                    content.append(object)

        content = sorted(content, key=lambda k: k['send_time'])
        content.reverse()
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
    def getAuthenticationStatus(cls, *args, **kwargs):
        """
            description: getAuthenticationStatus
            summary: getAuthenticationStatus
            responses:
                '200':
                    description: OK
                    schema:
                        type: string
        """
        login = kwargs['varargs'].split()[0]
        password = kwargs['varargs'].split()[1]
        user = db.session.query(User).filter_by(login=login, password=password).first()
        if user is not None:
            user.online = True
            db.session.commit()
            socketio.emit('login')
            return "success"
        return "failed"


    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def logout(cls, *args, **kwargs):
        """
            description: logout
            summary: logout
            responses:
                '200':
                    description: OK
                    schema:
                        type: string
        """

        login = kwargs['varargs']
        user = db.session.query(User).filter_by(login=login).first()
        if user is not None:
            user.online = False
            db.session.commit()
            socketio.emit('login')
            return "success"
        return "failed"

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getAllUsers(cls, *args, **kwargs):
        """
      description: getAllUsers
      summary: getAllUsers
      responses:
        '200':
          description: OK
          schema:
            type: array
            items:
              type: object
              properties:
                id:
                  type: string
                login:
                  type: string
                online:
                  type: string
        """
        content = []
        for user in db.session.query(User).filter_by().all():
            object = {"id": str(user.id), "login": str(user.login), "online": str(user.online)}
            content.append(object)
        content = sorted(content, key=lambda k: k['online'])
        content.reverse()
        return content

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getIdByLogin(cls, *args, **kwargs):
        """
            description: getIdByLogin
            summary: getIdByLogin
            responses:
                '200':
                    description: OK
                    schema:
                        type: string
        """
        login = kwargs['varargs']
        if db.session.query(User).filter_by(login=login).first() is not None:
            id = db.session.query(User).filter_by(login=login).first().id
            return str(id)
        return "failed"

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def getLoginById(cls, *args, **kwargs):
        """
            description: getLoginById
            summary: getLoginById
            responses:
                '200':
                    description: OK
                    schema:
                        type: string
        """
        id = kwargs['varargs']
        if db.session.query(User).filter_by(id=int(id)).first() is not None:
            login = db.session.query(User).filter_by(id=int(id)).first().login
            return login
        return "failed"

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def addUser(cls, *args, **kwargs):
        """
            description: addUser
            summary: addUser
            responses:
                '200':
                    description: OK
                    schema:
                        type: string
        """
        login = kwargs['varargs'].split()[0]
        password = kwargs['varargs'].split()[1]
        if db.session.query(User).filter_by(login=login).first() is not None:
            return "failed"
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        socketio.emit('login')
        return "success"

    @classmethod
    @jsonapi_rpc(http_methods=['GET'])
    def sendMessages(cls, *args, **kwargs):
        """
            description: sendMessages
            summary: sendMessages
            responses:
                '200':
                    description: OK
                    schema:
                        type: string
        """
        lista = kwargs['varargs'].split(" ",2)
        fromId =lista[0]
        toId = lista[1]
        messageString = lista[2]
        message = Message(fromId = int(fromId), toId = int(toId), message = messageString, send_time = datetime.datetime.now())
        db.session.add(message)
        db.session.commit()
        if int(toId) == -1:
            socketio.emit('refreshMessages')
        else:
            socketio.emit('refreshMessagesInPMafterSend',{'fromId' :fromId, 'toId' :toId })
        return "success"




def start_api(swagger_host="127.0.0.1", PORT=None):

    SAFRSBase.db_commit = False

    with app.app_context():
        db.init_app(app)
        db.create_all()
        userAdmin = User(login = "admin", password = "admin")
        testMessage = Message(message = "test", fromId = "1")
        db.session.add(userAdmin)
        db.session.add(testMessage)
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
socketio = SocketIO(app)

@app.route("/")
def goto_api():
    return redirect(API_PREFIX)

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5000
    start_api(HOST, PORT)
    # app.run(host=HOST, port=PORT, threaded=False)
    socketio.run(app)

