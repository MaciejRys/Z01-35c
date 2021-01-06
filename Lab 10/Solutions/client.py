# region Import
from __future__ import print_function
import datetime
from openapi_client.api.messages_api import MessagesApi
from openapi_client.api.users_api import UsersApi
from openapi_client.api_client import ApiClient, Configuration
from tkinter import *
import socketio

configuration = Configuration(
    host="http://127.0.0.1:5000/api"
)
sio = socketio.Client()


@sio.event
def login():
    GetOnlineUsers()

@sio.event
def refreshMessages():
    GetMessages()

@sio.event
def refreshMessagesInPMafterGet(data):
    apiInstance = UsersApi(ApiClient())
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = data['toId']  # str | GetMessagesByUserName arguments (optional)
    tologin = apiInstance.get_login_by_id0(include=include, fields_user=fields_user, varargs=varargs)
    if tologin in listOfPM:
        GetMessagesInPm(tologin, listOfPM[tologin], True)
        GetOnlineUsers()


@sio.event
def refreshMessagesInPMafterSend(data):
    apiInstance = UsersApi(ApiClient())
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = data['fromId']  # str | GetMessagesByUserName arguments (optional)
    fromlogin = apiInstance.get_login_by_id0(include=include, fields_user=fields_user, varargs=varargs)
    if fromlogin in listOfPM:
        GetMessagesInPm(fromlogin, listOfPM[fromlogin])
        GetOnlineUsers()
    else:
        GetOnlineUsers()



def getMessagesInChat():
    # Create an instance of the API class
    apiMessageInstance = MessagesApi(ApiClient())
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_message = 'writer_user,recipient_user,text,send_time'  # str | Message fields to include (csv) (optional) (default to 'writer_user,recipient_user,text,send_time')
    varargs = ""  # str | GetAuthenticationStatus arguments (optional)
    api_response = apiMessageInstance.get_messages_in_chat0(include=include, fields_message=fields_message, varargs=varargs)
    return api_response


def AuthenticationStatus(login, password):
    api_instance = UsersApi(ApiClient())
    include = 'include_example'  # str | User relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = login + " " + password  # str | GetAuthenticationStatus arguments (optional)
    api_response = api_instance.get_authentication_status0(include=include, fields_user=fields_user, varargs=varargs)
    if api_response == 'success':
        return True
    return False


def Logout(login):
    sio.disconnect()
    api_instance = UsersApi(ApiClient())
    include = 'include_example'  # str | User relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = login  # str | GetAuthenticationStatus arguments (optional)
    api_response = api_instance.logout0(include=include, fields_user=fields_user, varargs=varargs)
    root.quit()



def AddUser(login, password):
    api_instance = UsersApi(ApiClient())
    include = 'include_example'  # str | User relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = login + " " + password  # str | GetAuthenticationStatus arguments (optional)
    api_response = api_instance.add_user0(include=include, fields_user=fields_user, varargs=varargs)
    if api_response == 'success':
        return True
    return False


def SendMessageInPm(toLogin, myLogin, message, messageContentPM, textPM):
    message_detail_ = f' {message} : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \n'
    textPM.insert(END, message_detail_, 'cyan')
    messageContentPM.set("")
    apiInstance = UsersApi(ApiClient())
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = myLogin  # str | GetMessagesByUserName arguments (optional)
    myId = int(apiInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs))
    varargs = toLogin  # str | GetMessagesByUserName arguments (optional)
    toId = int(apiInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs))
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = str(myId) + " " + str(toId) + " " + message  # str | GetMessagesByUserName arguments (optional)
    UserSendMessages = apiInstance.send_messages0(include=include, fields_user=fields_user, varargs=varargs)
    if UserSendMessages == 'success':
        return True
    return False


def SendMessageToServer(fromLogin, message):
    apiInstance = UsersApi(ApiClient())
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = fromLogin  # str | GetMessagesByUserName arguments (optional)
    fromId = apiInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs)
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = fromId + " " + str(-1) + " " + message  # str | GetMessagesByUserName arguments (optional)
    UserSendMessages = apiInstance.send_messages0(include=include, fields_user=fields_user, varargs=varargs)
    if UserSendMessages == 'success':
        return True
    return False

def SendMessage():
    SendMessageToServer(login.get(), messageContent.get())
    messageContent.set("")


def GetOnlineUsers():
    if not sio.connected:
        return
    onlineList.delete(0, 'end')
    apiMessageInstance = MessagesApi(ApiClient())
    apiUserInstance = UsersApi(ApiClient())
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = login.get()  # str | GetMessagesByUserName arguments (optional)
    myId = apiUserInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs)
    fields_message = 'writer_user,recipient_user,text,send_time'  # str | Message fields to include (csv) (optional) (default to 'writer_user,recipient_user,text,send_time')
    varargs = myId  # str | GetAuthenticationStatus arguments (optional)
    api_response = apiMessageInstance.get_number_of_unread_messages_for_user0(include=include, fields_message=fields_message, varargs=varargs)
    varargs = ""   # str | GetAuthenticationStatus arguments (optional)
    users = apiUserInstance.get_all_users0(include=include, fields_user=fields_user, varargs=varargs)
    index = 0
    writedUsers = []
    for i in api_response:
        varargs = i['from_id']  # str | GetMessagesByUserName arguments (optional)
        userLogin = apiUserInstance.get_login_by_id0(include=include, fields_user=fields_user, varargs=varargs)
        if userLogin != login.get():
            online = "offline"
            if any((x['login'] == userLogin and x['online'] == "True") for x in users):
                online = "online"
            onlineList.insert(index, userLogin + " " + online + " unread: " + i['number_of_messages'])
            writedUsers.append(userLogin)
            index += 1

    for i in range(len(users)):
        if users[i]['login'] != login.get() and users[i]['login'] not in writedUsers :
            online = "offline"
            if users[i].online == "True":
                online = "online"
            onlineList.insert(index, users[i].login + " " + online + " unread: 0 ")
            index += 1

def GetMessages():
    messages = getMessagesInChat()
    apiInstance = UsersApi(ApiClient())
    text.delete('1.0', END)
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = login.get()  # str | GetMessagesByUserName arguments (optional)
    myId = apiInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs)
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    if len(messages) != 0:
        for i in range(len(messages)):
            varargs = messages[i].from_id  # str | GetMessagesByUserName arguments (optional)
            fromlogin = apiInstance.get_login_by_id0(include=include, fields_user=fields_user,
                                                     varargs=varargs)
            if messages[i].from_id == myId:
                message_detail_ = f'{messages[i].message} :{messages[i].send_time.strftime("%Y-%m-%d %H:%M:%S")}\n'
                text.insert(END, message_detail_, 'right')
            else:
                message_detail_ = f'{messages[i].send_time.strftime("%Y-%m-%d %H:%M:%S")} {fromlogin}:{messages[i].message} \n'
                text.insert(END, message_detail_)

def GetMessagesInPm(toLogin, textPM, isCallback = False):
    apiMessageInstance = MessagesApi(ApiClient())
    apiUserInstance = UsersApi(ApiClient())
    textPM.delete('1.0', END)
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = login.get()  # str | GetMessagesByUserName arguments (optional)
    toId = apiUserInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs)
    varargs = toLogin  # str | GetMessagesByUserName arguments (optional)
    fromId = apiUserInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs)
    fields_message = 'writer_user,recipient_user,text,send_time'  # str | Message fields to include (csv) (optional) (default to 'writer_user,recipient_user,text,send_time')
    varargs = toId + " " + fromId + " " + str(isCallback)  # str | GetMessagesByUserName arguments (optional)
    messages = apiMessageInstance.get_messages_in_pm0(include=include, fields_message=fields_message, varargs=varargs)
    if len(messages) != 0:
        for i in range(len(messages)):
            if messages[i].from_id == fromId:
                message_detail_ = f'{messages[i].send_time.strftime("%Y-%m-%d %H:%M:%S")} {toLogin.split()[0]}: {messages[i].message}\n'
                textPM.insert(END, message_detail_)
            else:
                message_detail_ = f'  {messages[i].message} :{messages[i].send_time.strftime("%Y-%m-%d %H:%M:%S")} \n'
                if messages[i].is_read == "False":
                    textPM.insert(END, message_detail_, 'cyan')
                else:
                    textPM.insert(END, message_detail_, 'right')

def startPrivateChatWindow(toLogin):
    toLogin = toLogin.split()[0]
    PMWindow = Toplevel(root)
    PMWindow.protocol("WM_DELETE_WINDOW",lambda: closePM(toLogin, PMWindow))
    PMWindow.title("Private chat " + login.get() + " with " + toLogin)
    canvasPM = Canvas(PMWindow, width=300, height=250)
    textPM = Text(PMWindow, height=10)
    textPM.pack(side="left")
    textPM.tag_configure("right", justify='right',foreground="white", background = "blue" )
    textPM.tag_configure("cyan", justify='right',foreground="white", background = "cyan" )
    scroll_y = Scrollbar(PMWindow, orient="vertical", command=textPM.yview)
    scroll_y.pack(side="left", expand=True, fill="y")
    textPM.configure(yscrollcommand=scroll_y.set)
    labelPM = Label(PMWindow, text="Message:")
    canvasPM.create_window(100, 85, window=labelPM)
    messageContentPM = StringVar()
    messageEntryPM = Entry(PMWindow, textvariable=messageContentPM)
    canvasPM.create_window(200, 85, window=messageEntryPM)
    send_buttonPM = Button(PMWindow, text="Send", command=lambda: SendMessageInPm(toLogin, login.get(), messageContentPM.get(), messageContentPM, textPM))
    canvasPM.create_window(200, 115, window=send_buttonPM)
    canvasPM.pack(side="right")
    labelPM2 = Label(PMWindow, text="private chat with :")
    canvasPM.create_window(150, 135, window=labelPM2)
    labelRecipient = Label(PMWindow, text=toLogin)
    canvasPM.create_window(220, 135, window=labelRecipient)
    listOfPM[toLogin] = textPM
    GetMessagesInPm(toLogin, textPM)
    GetOnlineUsers()

def closePM(login, window):
    if login in listOfPM:
        listOfPM.pop(login)
        window.destroy()



def AddUserWindow():
    UserWindow = Toplevel(root)
    canvasUserWindow = Canvas(UserWindow, width=300, height=200)
    canvasUserWindow.create_window(170, 20, window=Entry(UserWindow, textvariable=newLogin))
    canvasUserWindow.create_window(90, 20, window=Label(UserWindow, text="login"))
    newPassword_entry = Entry(UserWindow, textvariable=newPassword)
    canvasUserWindow.create_window(170, 40, window=newPassword_entry)
    canvasUserWindow.create_window(80, 40, window=Label(UserWindow, text="password"))
    search_button = Button(UserWindow, text="Add user", command=lambda: AddUser(newLogin.get(), newPassword.get()))
    canvasUserWindow.create_window(150, 70, window=search_button)
    canvasUserWindow.pack(side="right")

def SignIn():
    if AuthenticationStatus(login.get(), password.get()):
        canvas.delete("all")
        root.title(login.get())
        root.protocol("WM_DELETE_WINDOW", lambda: Logout(login.get()))
        sio.connect('http://127.0.0.1:5000')
        text.pack(side="left")
        scroll_y = Scrollbar(root, orient="vertical", command=text.yview)
        scroll_y.pack(side="left", expand=True, fill="y")
        text.configure(yscrollcommand=scroll_y.set)
        canvas.config(width=500, height=250)
        label6 = Label(text=f'Login:{login.get()}')
        canvas.create_window(50, 25, window=label6)
        label = Label(text="Message:")
        canvas.create_window(50, 85, window=label)
        messageEntry = Entry(textvariable=messageContent)
        canvas.create_window(170, 85, window=messageEntry)
        send_button = Button(text="Send", command=SendMessage)
        canvas.create_window(150, 115, window=send_button)
        addUserWindowButton = Button(text="Add User", command=AddUserWindow)
        canvas.create_window(150, 145, window=addUserWindowButton)
        canvas.create_window(350, 100, window=onlineList)
        startPWWindowButton = Button(text="start private chat", command=lambda: startPrivateChatWindow(onlineList.get(ANCHOR)))
        canvas.create_window(300, 200, window=startPWWindowButton)
        GetOnlineUsers()
        GetMessages()
    else:
        label = Label(text="This user doesnt exist.")
        canvas.create_window(150, 100, window=label)

root = Tk()
root.title("Messenger")
text = Text(root, height=15)
text.tag_configure("right", justify='right',foreground="white", background = "blue" )
canvas = Canvas(width=300, height=200)
login = StringVar()
password = StringVar()
newLogin = StringVar()
newPassword = StringVar()
recipientName = StringVar()
messageContent = StringVar()
chatHistory = StringVar()
listOfPM = {}
onlineList = Listbox(root,width = 30)
login_entry = Entry(textvariable=login)
canvas.create_window(170, 20, window=login_entry)
canvas.create_window(90, 20, window=Label(text="login"))
password_entry = Entry(textvariable=password)
canvas.create_window(170, 40, window=password_entry)
canvas.create_window(80, 40, window=Label(text="password"))
search_button = Button(text="Sign in", command=SignIn)
canvas.create_window(150, 70, window=search_button)
canvas.pack(side="right")
root.mainloop()



