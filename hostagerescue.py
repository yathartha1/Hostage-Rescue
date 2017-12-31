from random import choice
class rooms:
    def __init__(self ,contents=None, left=None, right=None, front=None):
        self.contents=contents
        self.right=right
        self.left=left
        self.front=front
    def getContents(self):
        return self.contents
    def getLeft(self):
        return self.left
    def getRight(self):
        return self.right
    def getFront(self):
        return self.front
    def setNext(self,left,right,front):
        self.left=left
        self.right=right
        self.front=front
    def updateValue(self,contents):
        self.contents=contents

room=[rooms(str(i)) for i in range(12)]
room[0].setNext(room[1],None,room[4])
room[1].setNext(None,room[5],room[2])
room[2].setNext(None,room[6],room[3])
room[3].setNext(None,None,room[7])
room[4].setNext(room[5],None,room[8])
room[5].setNext(room[1],room[9],room[6])
room[6].setNext(room[2],room[10],None)
room[7].setNext(None,room[6],room[11])
room[8].setNext(room[9],None,None)
room[9].setNext(room[5],None,room[10])
room[10].setNext(room[6],None,room[11])
room[11].setNext(room[7],room[10],None)
types = {
    0:"Living Room",
    1:"Garage",
    2:"Washroom",
    3:"Lawn",
    4:"Kitchen",
    5:"Bedroom one",
    6:"Bedroom two",
    7:"Study Room",
    8:"Game Room",
    9:"Bedroom three",
    10:"Movie Room",
    11:"Gym"
}
sound=""
sound1=""
counter = 0
value=0
r1=0
r2=0
r3=0
health=2
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event,context)
    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)

 
def on_launch(event, context):
    """ Called when the user launches the skill without specifying what they
    want
    """
    return welcome(event, context)

def intent_router(event, context):
    intent = event['request']['intent']['name']
    if intent == "Enter":
        return game_intent(event, context)
    if intent == "Open":
        return open1(event, context)
    if intent == "Cancel":
        return cancel_intent(event, context)
    if intent == "Stop":
        return stop_intent()
    if intent == "AMAZON.HelpIntent":
        return help_intent(event, context)
    else:
        return error(event, context)
 
 
# --------------- Functions that control the skill's behavior ------------------
 
 
def get_welcome_response(title, body):
 
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet)

def statement(title, body):
 
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet)

def statement1(title, body):
 
    speechlet = {}
    speechlet['outputSpeech'] = build_SSML(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet)

def end(title, body):
    global board
    speechlet = {}
    speechlet['outputSpeech'] = build_SSML(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)

def welcome(event, context):
    global sound
    global sound1
    sound1=""
    sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Drive.mp3'/>"
    wel1 = "Welcome to the Hostage Rescue game. " \
        "Two terrorists have taken shelter in a house and have kept an old woman as hostage. " \
        "It is your job to find that hostage and rescue her. "
    wel2="You have reached the house. " \
        "Just say enter the house. "
    return statement1("welcome", wel1+sound+wel2)
    
def error(event, context):
    er="I could not get that, please say it again."
    return statement("error",er)
 
def game_intent(event, context):
    global sound
    global room
    global counter
    global health
    global r1
    global r2
    global r3
    counter=0
    health=2
    t1=[8, 9]
    t2=[2, 3, 6, 7]
    h=[10, 11]
    r1=choice(t1)
    r2=choice(t2)
    r3=choice(h)

    for i in range(12):
        room[i]=rooms(str(i))
    room[0].setNext(room[1],None,room[4])
    room[1].setNext(None,room[5],room[2])
    room[2].setNext(None,room[6],room[3])
    room[3].setNext(None,None,room[7])
    room[4].setNext(room[5],None,room[8])
    room[5].setNext(room[1],room[9],room[6])
    room[6].setNext(room[2],room[10],None)
    room[7].setNext(None,room[6],room[11])
    room[8].setNext(room[9],None,None)
    room[9].setNext(room[5],None,room[10])
    room[10].setNext(room[6],None,room[11])
    room[11].setNext(room[7],room[10],None)

    room[r1].updateValue("t1")
    room[r2].updateValue("t2")
    room[r3].updateValue("h")
    game = "You have entered the Living Room. " \
            "There is pin drop silence. " \
            "There are two doorways, one in the front and one to your left. " \
            "Just select a direction to enter. " 
    return statement1("game_intent", game)

def stop_intent():
    term = "The game has stopped. " \
            "See you later. "
    return end("stop", term)
    
def cancel_intent(event, context):
    term = "The game has stopped. " \
            "See you later. "
    return end("stop", term)
    
def help_intent(event, context):
    term = "To select a doorway, just say the direction of the doorway like front, left and right. " \
            "If you want to exit the game, just say stop or cancel " 
    return statement("help", term) 

def open1(event, context):
    global counter
    pos = event['request']['intent']['slots']['Direction']['value']
    if pos not in ['left', 'front', 'right']:
        return error(event,context)
    elif counter == 0:
        return move1(pos)
    else:
        return move(pos)

def move1(pos):
    global room
    global types
    global counter
    global value
    global sound
    if pos == 'left':
        value=room[1]
        if room[2].getContents()=="t2":
            sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
            term1="You have entered the "+types.get(1)+". " \
                 "You can hear some sound from the front room. "
            term2="There is a doorway in your front. " \
                 "Just select the direction to enter. "
            counter=counter+1
            return statement1("left", term1+sound+term2)
        else:
            term="You have entered the "+types.get(1)+". " \
                 "There is no sound around. " \
                 "There is a doorway in your front. " \
                 "Just select the direction to enter. "
            counter=counter+1
            return statement1("left", term)
    elif pos == 'front':
        value=room[4]
        if room[8].getContents()=="t1":
            sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
            term1="You have entered the "+types.get(4)+". " \
                 "You can hear some sound from the front room. "
            term2="There are two doorways, one in the front and one to your left. " \
                  "Just select the direction to enter. "
            counter=counter+1
            return statement1("front", term1+sound+term2)
        else:
            term="You have entered the "+types.get(4)+". " \
                 "There is no sound around. " \
                 "There are two doorways, one in the front and one to your left. " \
                 "Just select the direction to enter. "
            counter=counter+1
            return statement1("front", term)
    else:
        term="There is no doorway there, please select a valid direction. "
        counter=0
        return statement1("wrong direction", term)

def move(pos):
    global value
    global room
    global types
    global health
    global r1
    global r2
    global r3
    global sound
    global sound1
    doorwayleft=0
    doorwayright=0
    doorwayfront=0
    someleft=0
    someright=0
    somefront=0
    char1=""
    char2=""
    char3="There is no sound around. "
    char4=""
    if pos == 'left' and value.getLeft()!=None:
        value=value.getLeft()
        if value.getContents()=="t1":
            value.updateValue(str(r1))
            if health==2:
                health=health-1
                char1="You have entered the "+types.get(int(r1))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char4="You came out to be victorious but lost half of your health. "
                if value.getLeft()!=None:
                    doorwayleft=1
                    someleft=checkleft()
                    if someleft==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your left. "

                if value.getRight()!=None:
                    doorwayright=1
                    someright=checkright()
                    if someright==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your right. "

                if value.getFront()!=None:
                    doorwayfront=1
                    somefront=checkfront()
                    if somefront==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room in front of you. "

                if doorwayleft==1:
                    char2="There is a doorway to your left. "\
                            "Just select a direction to enter. "
                if doorwayright==1:
                    char2="There is a doorway to your right. "\
                            "Just select a direction to enter. "
                if doorwayfront==1:
                    char2="There is a doorway to your front. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayright==1:
                    char2="There are two doorways, one to your left and one to your right. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayfront==1:
                    char2="There are two doorways, one to your left and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1:
                    char2="There are two doorways, one to your right and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1 and doorwayleft==1:
                    char2="There are three doorways, one to your left, one to your right and one in front of you. "\
                            "Just select a direction to enter. "
                return statement1("left", char1+sound+char4+char3+sound1+char2)  
            elif health==1:
                health=health-1
                char1="You have entered the "+types.get(int(r1))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char2="But unfortunately you died. "\
                      "The game is over. "
                return end("Lost", char1+sound+char2)
        elif value.getContents()=="t2":
            value.updateValue(str(r2))
            if health==2:
                health=health-1
                char1="You have entered the "+types.get(int(r2))+". " \
                    "There is a terrorist there, you both fought a hard battle. "
                sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char4="You came out to be victorious but lost half of your health. "
                if value.getLeft()!=None:
                    doorwayleft=1
                    someleft=checkleft()
                    if someleft==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your left. "

                if value.getRight()!=None:
                    doorwayright=1
                    someright=checkright()
                    if someright==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your right. "

                if value.getFront()!=None:
                    doorwayfront=1
                    somefront=checkfront()
                    if somefront==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room in front of you. "

                if doorwayleft==1:
                    char2="There is a doorway to your left. "\
                            "Just select a direction to enter. "
                if doorwayright==1:
                    char2="There is a doorway to your right. "\
                            "Just select a direction to enter. "
                if doorwayfront==1:
                    char2="There is a doorway to your front. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayright==1:
                    char2="There are two doorways, one to your left and one to your right. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayfront==1:
                    char2="There are two doorways, one to your left and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1:
                    char2="There are two doorways, one to your right and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1 and doorwayleft==1:
                    char2="There are three doorways, one to your left, one to your right and one in front of you. "\
                            "Just select a direction to enter. "
                return statement1("left", char1+sound+char4+char3+sound1+char2)
            elif health==1:
                health=health-1
                char1="You have entered the "+types.get(int(r2))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char2="But unfortunately you died. "\
                      "The game is over. "
                return end("Lost", char1+sound+char2)  
        elif value.getContents()=="h":
            char1="You have entered the "+types.get(int(r3))+". " \
                  "You found the hostage. "\
                  "She is tied to a chair. "\
                  "You untied her and rescued her through the backdoor. " \
                  "Congratulations, You won the game ."
            sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Win.mp3'/>"
            return end("Won", char1+sound)
        else:
            char1="You have entered the "+types.get(int(value.getContents()))+". "
            if value.getLeft()!=None:
                doorwayleft=1
                someleft=checkleft()
                if someleft==1:
                    sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                    char3="You can hear some sound from the room on your left. "

            if value.getRight()!=None:
                doorwayright=1
                someright=checkright()
                if someright==1:
                    sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                    char3="You can hear some sound from the room on your right. "

            if value.getFront()!=None:
                doorwayfront=1
                somefront=checkfront()
                if somefront==1:
                    sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                    char3="You can hear some sound from the room in front of you. "

            if doorwayleft==1:
                char2="There is a doorway to your left. "\
                        "Just select a direction to enter. "
            if doorwayright==1:
                char2="There is a doorway to your right. "\
                        "Just select a direction to enter. "
            if doorwayfront==1:
                char2="There is a doorway to your front. "\
                        "Just select a direction to enter. "
            if doorwayleft==1 and doorwayright==1:
                char2="There are two doorways, one to your left and one to your right. "\
                        "Just select a direction to enter. "
            if doorwayleft==1 and doorwayfront==1:
                char2="There are two doorways, one to your left and one to your front. "\
                        "Just select a direction to enter. "
            if doorwayright==1 and doorwayfront==1:
                char2="There are two doorways, one to your right and one to your front. "\
                        "Just select a direction to enter. "
            if doorwayright==1 and doorwayfront==1 and doorwayleft==1:
                char2="There are three doorways, one to your left, one to your right and one in front of you. "\
                        "Just select a direction to enter. "
            return statement1("left", char1+sound1+char3+char2)        

    elif pos == 'front' and value.getFront()!=None:
        value=value.getFront()
        if value.getContents()=="t1":
            value.updateValue(str(r1))
            if health==2:
                health=health-1
                char1="You have entered the "+types.get(int(r1))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char4="You came out to be victorious but lost half of your health. "
                if value.getLeft()!=None:
                    doorwayleft=1
                    someleft=checkleft()
                    if someleft==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your left. "

                if value.getRight()!=None:
                    doorwayright=1
                    someright=checkright()
                    if someright==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your right. "

                if value.getFront()!=None:
                    doorwayfront=1
                    somefront=checkfront()
                    if somefront==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room in front of you. "

                if doorwayleft==1:
                    char2="There is a doorway to your left. "\
                            "Just select a direction to enter. "
                if doorwayright==1:
                    char2="There is a doorway to your right. "\
                            "Just select a direction to enter. "
                if doorwayfront==1:
                    char2="There is a doorway to your front. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayright==1:
                    char2="There are two doorways, one to your left and one to your right. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayfront==1:
                    char2="There are two doorways, one to your left and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1:
                    char2="There are two doorways, one to your right and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1 and doorwayleft==1:
                    char2="There are three doorways, one to your left, one to your right and one in front of you. "\
                            "Just select a direction to enter. "
                return statement1("left", char1+sound+char4+char3+sound1+char2)  
            elif health==1:
                health=health-1
                char1="You have entered the "+types.get(int(r1))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char2="But unfortunately you died. "\
                      "The game is over. "
                return end("Lost", char1+sound1+char2)
        elif value.getContents()=="t2":
            value.updateValue(str(r2))
            if health==2:
                health=health-1
                char1="You have entered the "+types.get(int(r2))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char4="You came out to be victorious but lost half of your health. "
                if value.getLeft()!=None:
                    doorwayleft=1
                    someleft=checkleft()
                    if someleft==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your left. "

                if value.getRight()!=None:
                    doorwayright=1
                    someright=checkright()
                    if someright==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your right. "

                if value.getFront()!=None:
                    doorwayfront=1
                    somefront=checkfront()
                    if somefront==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room in front of you. "

                if doorwayleft==1:
                    char2="There is a doorway to your left. "\
                            "Just select a direction to enter. "
                if doorwayright==1:
                    char2="There is a doorway to your right. "\
                            "Just select a direction to enter. "
                if doorwayfront==1:
                    char2="There is a doorway to your front. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayright==1:
                    char2="There are two doorways, one to your left and one to your right. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayfront==1:
                    char2="There are two doorways, one to your left and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1:
                    char2="There are two doorways, one to your right and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1 and doorwayleft==1:
                    char2="There are three doorways, one to your left, one to your right and one in front of you. "\
                            "Just select a direction to enter. "
                return statement1("left", char1+sound+char4+char3+sound1+char2)
            elif health==1:
                health=health-1
                char1="You have entered the "+types.get(int(r2))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char2="But unfortunately you died. "\
                      "The game is over. "
                return end("Lost", char1+sound1+char2)  
        elif value.getContents()=="h":
            char1="You have entered the "+types.get(int(r3))+". " \
                  "You found the hostage. "\
                  "She is tied to a chair. "\
                  "You untied her and rescued her through the backdoor. " \
                  "Congratulations, You won the game ."
            sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Win.mp3'/>"
            return end("Won", char1+sound)
        else:
            char1="You have entered the "+types.get(int(value.getContents()))+". "
            if value.getLeft()!=None:
                doorwayleft=1
                someleft=checkleft()
                if someleft==1:
                    sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                    char3="You can hear some sound from the room on your left. "

            if value.getRight()!=None:
                doorwayright=1
                someright=checkright()
                if someright==1:
                    sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                    char3="You can hear some sound from the room on your right. "

            if value.getFront()!=None:
                doorwayfront=1
                somefront=checkfront()
                if somefront==1:
                    sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                    char3="You can hear some sound from the room in front of you. "

            if doorwayleft==1:
                char2="There is a doorway to your left. "\
                        "Just select a direction to enter. "
            if doorwayright==1:
                char2="There is a doorway to your right. "\
                        "Just select a direction to enter. "
            if doorwayfront==1:
                char2="There is a doorway to your front. "\
                        "Just select a direction to enter. "
            if doorwayleft==1 and doorwayright==1:
                char2="There are two doorways, one to your left and one to your right. "\
                        "Just select a direction to enter. "
            if doorwayleft==1 and doorwayfront==1:
                char2="There are two doorways, one to your left and one to your front. "\
                        "Just select a direction to enter. "
            if doorwayright==1 and doorwayfront==1:
                char2="There are two doorways, one to your right and one to your front. "\
                        "Just select a direction to enter. "
            if doorwayright==1 and doorwayfront==1 and doorwayleft==1:
                char2="There are three doorways, one to your left, one to your right and one in front of you. "\
                        "Just select a direction to enter. "
            return statement1("left", char1+sound1+char3+char2)

    elif pos == 'right' and value.getRight()!=None:
        value=value.getRight()
        if value.getContents()=="t1":
            value.updateValue(str(r1))
            if health==2:
                health=health-1
                char1="You have entered the "+types.get(int(r1))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char4="You came out to be victorious but lost half of your health. "
                if value.getLeft()!=None:
                    doorwayleft=1
                    someleft=checkleft()
                    if someleft==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your left. "

                if value.getRight()!=None:
                    doorwayright=1
                    someright=checkright()
                    if someright==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your right. "

                if value.getFront()!=None:
                    doorwayfront=1
                    somefront=checkfront()
                    if somefront==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room in front of you. "

                if doorwayleft==1:
                    char2="There is a doorway to your left. "\
                            "Just select a direction to enter. "
                if doorwayright==1:
                    char2="There is a doorway to your right. "\
                            "Just select a direction to enter. "
                if doorwayfront==1:
                    char2="There is a doorway to your front. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayright==1:
                    char2="There are two doorways, one to your left and one to your right. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayfront==1:
                    char2="There are two doorways, one to your left and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1:
                    char2="There are two doorways, one to your right and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1 and doorwayleft==1:
                    char2="There are three doorways, one to your left, one to your right and one in front of you. "\
                            "Just select a direction to enter. "
                return statement1("left", char1+sound+char4+char3+sound1+char2)  
            elif health==1:
                health=health-1
                char1="You have entered the "+types.get(int(r1))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char2="But unfortunately you died. "\
                      "The game is over. "
                return end("Lost", char1+sound1+char2)
        elif value.getContents()=="t2":
            value.updateValue(str(r2))
            if health==2:
                health=health-1
                char1="You have entered the "+types.get(int(r2))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char4="You came out to be victorious but lost half of your health. "
                if value.getLeft()!=None:
                    doorwayleft=1
                    someleft=checkleft()
                    if someleft==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your left. "

                if value.getRight()!=None:
                    doorwayright=1
                    someright=checkright()
                    if someright==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room on your right. "

                if value.getFront()!=None:
                    doorwayfront=1
                    somefront=checkfront()
                    if somefront==1:
                        sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                        char3="You can hear some sound from the room in front of you. "

                if doorwayleft==1:
                    char2="There is a doorway to your left. "\
                            "Just select a direction to enter. "
                if doorwayright==1:
                    char2="There is a doorway to your right. "\
                            "Just select a direction to enter. "
                if doorwayfront==1:
                    char2="There is a doorway to your front. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayright==1:
                    char2="There are two doorways, one to your left and one to your right. "\
                            "Just select a direction to enter. "
                if doorwayleft==1 and doorwayfront==1:
                    char2="There are two doorways, one to your left and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1:
                    char2="There are two doorways, one to your right and one to your front. "\
                            "Just select a direction to enter. "
                if doorwayright==1 and doorwayfront==1 and doorwayleft==1:
                    char2="There are three doorways, one to your left, one to your right and one in front of you. "\
                            "Just select a direction to enter. "
                return statement1("left", char1+sound+char4+char3+sound1+char2)
            elif health==1:
                health=health-1
                char1="You have entered the "+types.get(int(r2))+". " \
                  "There is a terrorist there, you both fought a hard battle. "
                sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Shoot.mp3'/>"
                char2="But unfortunately you died. "\
                      "The game is over. "
                return end("Lost", char1+sound1+char2)  
        elif value.getContents()=="h":
            char1="You have entered the "+types.get(int(r3))+". " \
                  "You found the hostage. "\
                  "She is tied to a chair. "\
                  "You untied her and rescued her through the backdoor. " \
                  "Congratulations, You won the game ."
            sound="<audio src='https://s3.amazonaws.com/hostagerescuesound/Win.mp3'/>"
            return end("Won", char1+sound)
        else:
            char1="You have entered the "+types.get(int(value.getContents()))+". "
            if value.getLeft()!=None:
                doorwayleft=1
                someleft=checkleft()
                if someleft==1:
                    sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                    char3="You can hear some sound from the room on your left. "

            if value.getRight()!=None:
                doorwayright=1
                someright=checkright()
                if someright==1:
                    sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                    char3="You can hear some sound from the room on your right. "

            if value.getFront()!=None:
                doorwayfront=1
                somefront=checkfront()
                if somefront==1:
                    sound1="<audio src='https://s3.amazonaws.com/hostagerescuesound/Footsteps.mp3'/>"
                    char3="You can hear some sound from the room in front of you. "

            if doorwayleft==1:
                char2="There is a doorway to your left. "\
                        "Just select a direction to enter. "
            if doorwayright==1:
                char2="There is a doorway to your right. "\
                        "Just select a direction to enter. "
            if doorwayfront==1:
                char2="There is a doorway to your front. "\
                        "Just select a direction to enter. "
            if doorwayleft==1 and doorwayright==1:
                char2="There are two doorways, one to your left and one to your right. "\
                        "Just select a direction to enter. "
            if doorwayleft==1 and doorwayfront==1:
                char2="There are two doorways, one to your left and one to your front. "\
                        "Just select a direction to enter. "
            if doorwayright==1 and doorwayfront==1:
                char2="There are two doorways, one to your right and one to your front. "\
                        "Just select a direction to enter. "
            if doorwayright==1 and doorwayfront==1 and doorwayleft==1:
                char2="There are three doorways, one to your left, one to your right and one in front of you. "\
                        "Just select a direction to enter. "
            return statement1("left", char1+sound1+char3+char2)
    else:
        term="There is no doorway there, please select a valid direction. "
        return statement1("wrong direction", term)

def checkleft():
    global value
    someleft=0
    if value.getLeft().getContents()=="t1" or value.getLeft().getContents=="t2" or value.getLeft().getContents()=="h":
        someleft=1
    return someleft

def checkright():
    global value
    someright=0
    if value.getRight().getContents()=="t1" or value.getRight().getContents=="t2" or value.getRight().getContents()=="h":
        someright=1
    return someright

def checkfront():
    global value
    somefront=0
    if value.getFront().getContents()=="t1" or value.getFront().getContents=="t2" or value.getFront().getContents()=="h":
        somefront=1
    return somefront
 
# --------------- Helpers that build all of the responses ----------------------

def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

def build_SSML(body):
    global sound
    speech = {}
    speech['type'] = 'SSML'
    speech['ssml'] = "<speak>"+ body + "</speak>"
    return speech
    
def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card 
 
def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response