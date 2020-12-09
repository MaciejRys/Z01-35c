# region Import
from __future__ import print_function
import openapi_client
from openapi_client import UserSendMessages1
from openapi_client.rest import ApiException
from tkinter import *


configuration = openapi_client.Configuration(
    host="http://127.0.0.1:5000/api"
)

def GetMessageByUserId(login):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        apiMessageInstance = openapi_client.MessagesApi(api_client)
        apiUserInstance = openapi_client.UsersApi(api_client)
        include = 'include_example'  # str | Message relationships to include (csv) (optional)
        fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
        varargs = login  # str | GetMessagesByUserName arguments (optional)
        userId = apiUserInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs).meta.result.result
        include = 'include_example'  # str | Message relationships to include (csv) (optional)
        fields_message = 'writer_user,recipient_user,text,send_time'  # str | Message fields to include (csv) (optional) (default to 'writer_user,recipient_user,text,send_time')
        varargs = userId  # str | GetMessagesByUserName arguments (optional)

        api_response = apiMessageInstance.get_messages_by_user_id0(include=include, fields_message=fields_message, varargs=varargs)
        return api_response.meta.result


def AuthenticationStatus(login, password):
    with openapi_client.ApiClient() as api_client:
        api_instance = openapi_client.UsersApi(api_client)
        include = 'include_example'  # str | User relationships to include (csv) (optional)
        fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
        varargs = login + " " + password  # str | GetAuthenticationStatus arguments (optional)

        api_response = api_instance.get_authentication_status0(include=include, fields_user=fields_user, varargs=varargs)
        if api_response.meta.result.result == 'success':
            return True
        return False

def Logout(login):
    with openapi_client.ApiClient() as api_client:
        api_instance = openapi_client.UsersApi(api_client)
        include = 'include_example'  # str | User relationships to include (csv) (optional)
        fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
        varargs = login  # str | GetAuthenticationStatus arguments (optional)

        api_response = api_instance.logout0(include=include, fields_user=fields_user, varargs=varargs)
        if api_response.meta.result.result == 'success':
            root.destroy()
            return True
        root.destroy()
        return False


def AddUser(login, password):
    with openapi_client.ApiClient() as api_client:
        api_instance = openapi_client.UsersApi(api_client)
        include = 'include_example'  # str | User relationships to include (csv) (optional)
        fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
        varargs = login + " " + password  # str | GetAuthenticationStatus arguments (optional)

        api_response = api_instance.add_user0(include=include, fields_user=fields_user, varargs=varargs)
        if api_response.meta.result.result == 'success':
            return True
        return False

def SendMessageInPm(toLogin, myLogin, message, messageContentPM, textPM):
    message_detail_ = f'me: {message} \n'
    textPM.insert(END, message_detail_)
    messageContentPM.set("")

    # Create an instance of the API class
    apiInstance = openapi_client.UsersApi(openapi_client.ApiClient())
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = myLogin  # str | GetMessagesByUserName arguments (optional)
    myId = int(apiInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs).meta.result.result)

    varargs = toLogin  # str | GetMessagesByUserName arguments (optional)
    toId = int(apiInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs).meta.result.result)

    UserSendMessages = UserSendMessages1(method="SendMessage")
    UserSendMessages.args = {"fromId": myId, "toId": toId,
                             "message": message, "pm" : True}
    post_user_send_message = openapi_client.PostUserSendMessages(UserSendMessages)  # PostUserSendMail |

    try:
        apiInstance.invoke_user_send_messages0(post_user_send_message)
    except ApiException as e:
        print("Exception when calling UsersApi->invoke_user_send_mail0: %s\n" % e)


def SendMessageToServer(fromLogin, toLogin, message):
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        apiInstance = openapi_client.UsersApi(api_client)
        include = 'include_example'  # str | Message relationships to include (csv) (optional)
        fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
        varargs = fromLogin  # str | GetMessagesByUserName arguments (optional)
        fromId = apiInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs)

        include = 'include_example'  # str | Message relationships to include (csv) (optional)
        fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
        varargs = toLogin  # str | GetMessagesByUserName arguments (optional)
        toId = apiInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs)

        UserSendMessages = UserSendMessages1(method="SendMessage")
        UserSendMessages.args = {"fromId": int(fromId.meta.result.result), "toId": int(toId.meta.result.result),
                             "message": message, "pm" : False}
        post_user_send_message = openapi_client.PostUserSendMessages(UserSendMessages)  # PostUserSendMail |

        try:
            apiInstance.invoke_user_send_messages0(post_user_send_message)
        except ApiException as e:
            print("Exception when calling UsersApi->invoke_user_send_mail0: %s\n" % e)


# endregion
def SendMessage():
    SendMessageToServer(login.get(), recipientName.get(), messageContent.get())
    message_detail_ = f'me to {recipientName.get()}:{messageContent.get()} \n'
    text.insert(END, message_detail_)
    messageContent.set("")

def GetOnlineUsers():
    # Create an instance of the API class
    onlineList.delete(0, 'end')
    apiUserInstance = openapi_client.UsersApi(openapi_client.ApiClient())
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = ""  # str | GetMessagesByUserName arguments (optional)
    users = apiUserInstance.get_all_online_users0(include=include, fields_user=fields_user, varargs=varargs).meta.result.users
    for i in range(len(users)):
        onlineList.insert(i, users[i])
    root.after(5000, GetOnlineUsers)

def GetMessages():
    messages = GetMessageByUserId(login.get())
    apiInstance = openapi_client.UsersApi(openapi_client.ApiClient())
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    if len(messages.id) != 0:
        for i in range(len(messages.id)):
            varargs = messages.from_id[i] # str | GetMessagesByUserName arguments (optional)
            fromlogin = apiInstance.get_login_by_id0(include=include, fields_user=fields_user, varargs=varargs).meta.result.result
            message_detail_ = f'{fromlogin} to me:{messages.message[i]} \n'
            text.insert(END, message_detail_)
    root.after(1000, GetMessages)

def GetMessagesInPm(toLogin, textPM):
    apiMessageInstance = openapi_client.MessagesApi(openapi_client.ApiClient())
    apiUserInstance = openapi_client.UsersApi(openapi_client.ApiClient())
    include = 'include_example'  # str | Message relationships to include (csv) (optional)
    fields_user = 'name'  # str | User fields to include (csv) (optional) (default to 'name')
    varargs = login.get()  # str | GetMessagesByUserName arguments (optional)
    toId = apiUserInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs).meta.result.result
    varargs = toLogin # str | GetMessagesByUserName arguments (optional)
    fromId = apiUserInstance.get_id_by_login0(include=include, fields_user=fields_user, varargs=varargs).meta.result.result
    fields_message = 'writer_user,recipient_user,text,send_time'  # str | Message fields to include (csv) (optional) (default to 'writer_user,recipient_user,text,send_time')
    varargs = toId + " " +  fromId  # str | GetMessagesByUserName arguments (optional)
    messages = apiMessageInstance.get_messages_in_pm0(include=include, fields_message=fields_message, varargs=varargs).meta.result
    if len(messages.id) != 0:
        for i in range(len(messages.id)):
            message_detail_ = f'{toLogin}: {messages.message[i]} \n'
            textPM.insert(END, message_detail_)
    textPM.after(1000, GetMessagesInPm, toLogin, textPM)


def startPrivateChatWindow(toLogin):
    PMWindow = Toplevel(root)
    PMWindow.title("Private chat " + login.get() + " with " + toLogin)
    canvasPM = Canvas(PMWindow,  width=300, height=250)

    textPM = Text(PMWindow, height=10)
    textPM.pack(side="left")
    scroll_y = Scrollbar(PMWindow, orient="vertical", command=textPM.yview)
    scroll_y.pack(side="left", expand=True, fill="y")
    textPM.configure(yscrollcommand=scroll_y.set)

    labelPM = Label(PMWindow, text="Message:")
    canvasPM.create_window(100, 85, window=labelPM)
    messageContentPM = StringVar()
    messageEntryPM = Entry(PMWindow, textvariable=messageContentPM)
    canvasPM.create_window(200, 85, window=messageEntryPM)
    send_buttonPM = Button(PMWindow, text="Send", command= lambda:SendMessageInPm(toLogin, login.get(), messageContentPM.get(), messageContentPM, textPM))
    canvasPM.create_window(200, 115, window=send_buttonPM)
    canvasPM.pack(side="right")
    labelPM2 = Label(PMWindow,text="praivate chat with :")
    canvasPM.create_window(150, 135, window=labelPM2)
    labelRecipient = Label(PMWindow, text=toLogin)
    canvasPM.create_window(220, 135, window=labelRecipient)
    textPM.after(1000, GetMessagesInPm, toLogin, textPM)

def AddUserWindow():
    UserWindow = Toplevel(root)
    canvasUserWindow = Canvas(UserWindow,  width=300, height=200)
    canvasUserWindow.create_window(170, 20, window= Entry(UserWindow, textvariable=newLogin))
    canvasUserWindow.create_window(90,20, window = Label(UserWindow, text = "login"))
    newPassword_entry = Entry(UserWindow, textvariable=newPassword)
    canvasUserWindow.create_window(170, 40, window=newPassword_entry)
    canvasUserWindow.create_window(80,40, window = Label(UserWindow, text = "password"))
    search_button = Button(UserWindow, text="Add user", command= lambda: AddUser(newLogin.get(), newPassword.get()))
    canvasUserWindow.create_window(150, 70, window=search_button)
    canvasUserWindow.pack(side="right")

def SignIn():
    if AuthenticationStatus(login.get(), password.get()):
        root.after(1000, GetMessages)
        root.after(1000, GetOnlineUsers)
        canvas.delete("all")
        root.title(login.get())
        text.pack(side="left")

        scroll_y = Scrollbar(root, orient="vertical", command=text.yview)
        scroll_y.pack(side="left", expand=True, fill="y")

        text.configure(yscrollcommand=scroll_y.set)

        canvas.config(width=500, height=250)

        label6 = Label(text=f'Login:{login.get()}')
        canvas.create_window(50, 25, window=label6)

        recipientNameEntry = Entry(textvariable=recipientName)
        label = Label(text="Recipient login:")
        canvas.create_window(50, 55, window=label)
        canvas.create_window(170, 55, window=recipientNameEntry)

        label = Label(text="Message:")
        canvas.create_window(50, 85, window=label)
        messageEntry = Entry(textvariable=messageContent)
        canvas.create_window(170, 85, window=messageEntry)
        send_button = Button(text="Send", command=SendMessage)
        canvas.create_window(150, 115, window=send_button)
        addUserWindowButton = Button(text="Add User", command=AddUserWindow)
        canvas.create_window(150, 145, window=addUserWindowButton)
        logoutButton = Button(text="Logout", command=lambda: Logout(login.get()))
        canvas.create_window(150, 175, window=logoutButton)
        canvas.create_window(300, 100, window=onlineList)
        startPWWindowButton = Button(text="start private chat", command=lambda: startPrivateChatWindow(onlineList.get(ANCHOR)))
        canvas.create_window(300, 200, window=startPWWindowButton)
        GetOnlineUsers()


    else:
        label = Label(text="This user doesnt exist.")
        canvas.create_window(150, 100, window=label)



root = Tk()
root.title("Messenger")

text = Text(root, height=15)

canvas = Canvas(width=300, height=200)
login = StringVar()
password = StringVar()
newLogin = StringVar()
newPassword = StringVar()
recipientName = StringVar()
messageContent = StringVar()
chatHistory = StringVar()
onlineList = Listbox()
login_entry = Entry(textvariable=login)
canvas.create_window(170, 20, window=login_entry)
canvas.create_window(90,20, window = Label(text = "login"))
password_entry = Entry(textvariable=password)
canvas.create_window(170, 40, window=password_entry)
canvas.create_window(80,40, window = Label(text = "password"))
search_button = Button(text="Sign in", command=SignIn)
canvas.create_window(150, 70, window=search_button)

canvas.pack(side="right")

root.mainloop()
