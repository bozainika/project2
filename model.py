class Message:
    def __init__(self, sender, message):
        self.sender=sender
        self.message=message


class Room:
    def __init__(self, title, made_by):
        self.title=title
        self.made_by=made_by
        self.messages=[];

    def add_message(self,username,message):
        data=Message(username,message)
        self.messages.append(data)

    def get_messages(self):
        msg_list=[]
        for msg in self.messages:
            msg_list.append(msg.__dict__)
        return msg_list

