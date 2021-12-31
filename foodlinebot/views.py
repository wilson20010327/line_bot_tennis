from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,ImageSendMessage
from foodlinebot.models import *

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
message=[]
win_target=3
from transitions.extensions import GraphMachine
import random
@csrf_exempt
def callback(request):
    
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                mtext=event.message.text
            else:
                mtext="sticker"
            uid=event.source.user_id
            profile=line_bot_api.get_profile(uid)
            name=profile.display_name
            pic_url=profile.picture_url
            error_message=[]
            temp=True
            
            #清空data base
            #User_Info.objects.all().delete()
            if User_Info.objects.filter(uid=uid).exists()==False:
                User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext,state="Init",win=0,lose=0)
                message.append(TextSendMessage(text='遊戲註冊完畢'))
                message.append(creat_tmp_message("Tennis game","Detail for Introduction\nStart for start the game","detail","start","排行榜"))
                
            elif User_Info.objects.filter(uid=uid).exists()==True:
                
                error_message.append(TextSendMessage(text='你現在不能執行這個指令喔'))
                
                user_info = User_Info.objects.filter(uid=uid)
                
                for user in user_info:
                    #import fsm with diffrent state 
                    machine = TocMachine(states=states,transitions=transitions,initial=user.state,auto_transitions=False,show_conditions=True,)
                    
                    #info = 'UID=%s\nNAME=%s\n大頭貼=%s'%(user.uid,user.name,user.pic_url)
                    #message.append(TextSendMessage(text=info))
                    error_m="Look carefully yours state is "+user.state
                    error_message.append(TextSendMessage(text=error_m))
                    if (user.state==states[0]):
                        User_Info.objects.filter(uid=uid).update(lose=0)
                        User_Info.objects.filter(uid=uid).update(win=0)

                        temp=machine.start(event)
                        
                    elif ("score" in event.message.text.lower()):
                        win=user.win
                        lose=user.lose
                        message.append(TextSendMessage(text="Recent Score\nWin : "+str(win)+"\nLose : "+str(lose)))
                    elif (user.state==states[2]):
                        temp=machine.user_serve(event)
                        if(temp==False):
                            reply_text(event.reply_token,error_message)
                    elif (user.state==states[8] or user.state==states[9]):
                        temp=machine.user_defense(event)
                        if(temp==False):
                            reply_text(event.reply_token,error_message)
                    if (machine.state==states[10] ):
                        lose=user.lose
                        lose=lose+1
                        temp=machine.check_lose(lose)
                        print(lose)
                        User_Info.objects.filter(uid=uid).update(lose=lose)
                        
                    if (machine.state==states[6]):
                        win=user.win
                        win=win+1
                        temp=machine.check_win(win)
                        print(win)
                        if win>=win_target:
                            Score_Info.objects.create(name=name,win=win,lose=user.lose)
                        User_Info.objects.filter(uid=uid).update(win=win)
                        
                    
                    User_Info.objects.filter(uid=uid).update(state=machine.state)
            
            #line_bot_api.reply_message(event.reply_token,message)
            if temp==True:
                reply_text(event.reply_token,message)
            if(temp==False):
                reply_text(event.reply_token,error_message)
            message.clear()            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def reply_text(token,message):
    line_bot_api.reply_message(token,message)
def creat_tmp_message(title,detail,act1,act2,act3):
    temp=TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            title=title,
            text=detail,
            actions=[
                MessageTemplateAction(
                    label=act1,
                    text=act1
                ),
                MessageTemplateAction(
                    label=act2,
                    text=act2
                ),
                MessageTemplateAction(
                    label=act3,
                    text=act3
                )
            ]
        )
    )
    return temp

states=["Init", "Instruction", "U_serve","U_right","U_left","L_serve","Win","W_end","L_right","L_left","Lose","L_end","Score_list"]
transitions=[
        {
            "trigger": "start",
            "source": "Init",
            "dest": "Instruction",
            "conditions": "read_detail",
        },
        {
            "trigger": "start",
            "source": "Init",
            "dest": "Score_list",
            "conditions": "score_read",
        },
        {
            "trigger": "start",
            "source": "Init",
            "dest": "U_serve",
            "conditions": "start_game",
        },
        {
            "trigger": "user_serve",
            "source": "U_serve",
            "dest": "U_right",
            "conditions": "User_serve_to_right",
        },
        {
            "trigger": "user_serve",
            "source": "U_serve",
            "dest": "U_left",
            "conditions": "User_serve_to_left",
        },
        {
            "trigger": "line_defense_right",
            "source": "U_right",
            "dest": "L_serve",    
        },
        {
            "trigger": "line_defense_left",
            "source": "U_right",
            "dest": "Win", 
        },
        {
            "trigger": "line_defense_right",
            "source": "U_left",
            "dest": "Win",    
        },
        {
            "trigger": "line_defense_left",
            "source": "U_left",
            "dest": "L_serve", 
        },
        {
            "trigger": "line_serve_right",
            "source": "L_serve",
            "dest": "L_right",
        },
        {
            "trigger": "line_serve_left",
            "source": "L_serve",
            "dest": "L_left",
        },
        {
            "trigger": "check_win",
            "source": "Win",
            "dest": "W_end",
            "conditions": "win_bigger_15",
        },
        {
            "trigger": "check_win",
            "source": "Win",
            "dest": "U_serve",
            "conditions": "win_smaller_15",
        },
        {
            "trigger": "user_defense",
            "source": "L_right",
            "dest": "U_serve",
            "conditions": "user_defense_right",
        },
        {
           "trigger": "user_defense",
            "source": "L_right",
            "dest": "Lose",
            "conditions": "user_defense_left",
        },
        {
            "trigger": "user_defense",
            "source": "L_left",
            "dest": "U_serve",
            "conditions": "user_defense_left",
        },
        {
           "trigger": "user_defense",
            "source": "L_left",
            "dest": "Lose",
            "conditions": "user_defense_right",
        },
         {
            "trigger": "check_lose",
            "source": "Lose",
            "dest": "L_end",
            "conditions": "lose_bigger_15",
        },
        {
             "trigger": "check_lose",
            "source": "Lose",
            "dest": "L_serve",
            "conditions": "lose_smaller_15",
        },
        {"trigger": "go_back", "source":["W_end", "L_end","Instruction","Score_list"], "dest": "Init"},
        
    ]


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def on_enter_Init(self, event=0):
        print("Init")
        #reply_token = event.reply_token
        message.append(creat_tmp_message("Tennis game","Detail for Introduction\nStart for start the game\n","detail","start","排行榜"))

    def start_game(self, event):
        text = event.message.text
        return "start" in text.lower()  

    def score_read(self, event):
        text = event.message.text
        return "排行榜" in text      
    def on_enter_Score_list(self,event=0):
        score_list=Score_Info.objects.all()
        #print(score_list)
        score_name="排行榜(時間排序)"
        for u in score_list:
            print(u)
            score_name=score_name+'\n'+str(u)+" win : "+str(u.win)+" lose : "+str(u.lose)
        message.append(TextSendMessage(text=score_name))
        self.go_back()

    def on_enter_U_serve(self, event=0):
        print("I'm serving")
        #reply_token = event.reply_token
        message.append(TextSendMessage(text="I'm serving") )
        #message.append(creat_tmp_message("Tennis game","Type :\nDetail for Introduction\nStart for start the game","detail","start","排行榜"))
        message.append(creat_tmp_message("Serving","Choose the side to serve","Left","Right","Score"))

    def read_detail(self, event):
        text = event.message.text
        return "detail" in text.lower()
        
    def on_enter_Instruction(self, event=0):
        print("I'm reading")
        #reply_token = event.reply_token
        message.append(TextSendMessage(text="This is a Tennis game\nPlay with line bot\nYou can choose \n\tRight\n\t  or \n\tLeft \nWhen you are serving or defensing") )
        self.go_back()

    def User_serve_to_left(self, event):
        text = event.message.text
        return "left" in text.lower()
        

    def on_enter_U_left(self, event=0):
        print("I'm serving left")
        #reply_token = event.reply_token
        message.append(TextSendMessage(text="I'm entering left") )
        temp=random.randint(0,1)
        if(temp==0):
            self.line_defense_right()
        else:
            self.line_defense_left()

    def User_serve_to_right(self, event):
        text = event.message.text
        return "right" in text.lower()
       

    def on_enter_U_right(self, event=0):
        print("I'm serving right")
        #reply_token = event.reply_token
        message.append(TextSendMessage(text="I'm entering right") )
        temp=random.randint(0,1)
        if(temp==0):
            self.line_defense_right()
        else:
            self.line_defense_left()

    def on_enter_Win(self):
        print("I get the score")
        #reply_token = event.reply_token
        message.append(TextSendMessage(text="I get the score") )

    def win_smaller_15(self, win):
        return win<win_target
    def win_bigger_15(self, win):
        return win>=win_target

    def on_enter_W_end(self,event=0):
        print("I win the game")
        #reply_token = event.reply_token
        pic = 'https://blog.english4u.net/images/blog/20200303031955.jpg'
        message.append(TextSendMessage(text="I win the game") )
        message.append(ImageSendMessage(original_content_url=pic,preview_image_url=pic))
        self.go_back()

    def on_enter_L_serve(self,lose=0):
        print("Bot is serving")
        #reply_token = event.reply_token
        message.append(TextSendMessage(text="Bot is serving") )
        temp=random.randint(0,1)
        if(temp==0):
            self.line_serve_right()
        else:
            self.line_serve_left()

    def on_enter_L_right(self):
        print("Bot is serving to right")
        #reply_token = event.reply_token
        message.append(TextSendMessage(text="Bot is serving to right") )
        message.append(creat_tmp_message("Bot is serving","Please defensing\nChoose the side to defense","Left","Right","Score"))

    def on_enter_L_left(self):
        print("Bot is serving to left")
        #reply_token = event.reply_token
        message.append(TextSendMessage(text="Bot is serving to left") )
        message.append(creat_tmp_message("Bot is serving","Please defensing\nChoose the side to defense","Left","Right","Score"))

    def user_defense_left(self,event):
        text = event.message.text
        return "left" in text.lower()
       
    def user_defense_right(self,event):
        text = event.message.text
        return "right" in text.lower()
        

    def on_enter_Lose(self, event=0):
        print("I lose  the score")
        #reply_token = event.reply_token
        message.append(TextSendMessage(text="I lose  the score") )

    def lose_smaller_15(self, lose):
        return lose<win_target
    def lose_bigger_15(self, lose):
        return lose>=win_target

    def on_enter_L_end(self,event=0):
        print("I lose the game")
        #reply_token = event.reply_token
        message.append(TextSendMessage(text="I lose the game") )
        pic = 'https://previews.123rf.com/images/lkeskinen/lkeskinen1709/lkeskinen170908913/86154548-you-lose-rubber-stamp.jpg'
        message.append(ImageSendMessage(original_content_url=pic,preview_image_url=pic))
        self.go_back()

    def on_exit_temp_left(self):
        print("Leaving state2")

