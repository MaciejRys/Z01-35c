import openapi_client
from openapi_client.api import default_api
import tkinter as tk
configuration = openapi_client.Configuration(
    host = "http://localhost:5000"
)
userID = 0
chatText = []
root = tk.Tk()

def UpdateChat():
    apiInstance = default_api.DefaultApi(openapi_client.ApiClient(configuration))
    apiClient = apiInstance.get_user_id_get(userID)
    for x in (apiClient.to_dict())['messages']:
        chatText.append(str(x).strip())
    updateChat()

def SendTo():
    clientInstance = default_api.DefaultApi(openapi_client.ApiClient(configuration))
    recipientUserId = int(messageToUserEntry.get())
    message = messageText.get("1.0", "end")
    chatText.append("Your message: " + str(message).strip())
    updateChat()
    clientInstance.send_user_id_message_post(recipientUserId, message)
    messageText.delete("1.0", "end")

def updateChat():
    chatLabel['text'] = ""
    for text in chatText:
        chatLabel['text'] += text + "\n"

def FirstWindow(root):
    global idClientEntry

    root.geometry("150x100")
    idClientLabel = tk.Label(root, text="Podaj ID Clienta")
    idClientLabel.pack()

    idClientEntry = tk.Entry(root)
    idClientEntry.pack()

    idClientButton = tk.Button(root,text="Dalej",command=lambda: MessengerWindow(root))
    idClientButton.pack()

def MessengerWindow(root):
    global userID,chatLabel,messageText,messageToUserEntry

    userID = int(idClientEntry.get())
    root.destroy()
    root = tk.Tk()
    root.geometry("800x300")
    chatLabel = tk.Label(root,text=chatText,width=70,height=20,anchor="sw")
    chatLabel.grid(row=1,column=0)

    updateButton = tk.Button(root,text="Update",command=UpdateChat())
    updateButton.grid(row=1,column=1)

    messageText = tk.Text(root,width=15,height=5)
    messageText.grid(row=0,column=0)

    messageButton = tk.Button(root,text="Send",command=SendTo)
    messageButton.grid(row=0,column=3)

    clientNumber = tk.Label(root,text="Klient nr:" + str(userID))
    clientNumber.grid(row=1,column=2)

    messageToUserLabel = tk.Label(root,text="to user ")
    messageToUserLabel.grid(row=0,column=1)

    messageToUserEntry = tk.Entry(root)
    messageToUserEntry.grid(row=0,column=2)

if __name__ == "__main__":
    FirstWindow(root)
    root.mainloop()
    pass 