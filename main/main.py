import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.properties import BooleanProperty,NumericProperty
from kivy.vector import Vector
from random import random,sample,randint
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

kivy.require('1.9.0')

def math():
    #global score
    num1 = randint(1,20)
    num2 = randint(1,20)
    global symbol 
    symbol = randint(1,5)

    if symbol == 1:
        question = str(num1) + " + " + str(num2)
        answer = num1 + num2
        return question,answer

    elif symbol == 2:
        question = str(num1) + " - " + str(num2)
        answer = num1 - num2
        return question, answer
    
    elif symbol == 3:
        question = str(num1) + " x " + str(num2)
        answer = num1 * num2
        return question,answer
    
    elif symbol == 4:
        question = str(num1) + " / " + str(num2)
        answer = round((num1 / num2),1)
        return question,answer
    elif symbol == 5:
        question = str(num1) + " % " + str(num2)
        answer = num1 % num2
        return question,answer


class SB(Label):
    
    ans=NumericProperty(None)

    def on_touch_down(self, touch):

        self.wrong = SoundLoader.load("../audio/wrong.mp3")
        self.correct = SoundLoader.load("../audio/correct.mp3")
        
        if not self.parent.clicked:
            
            if self.collide_point(*touch.pos):
                touch.grab(self)
                anim=Animation(center_x=self.center_x,size=(150,150),d=0.2)
                anim+=Animation(center_x=self.center_x,size=(100,100),d=0.2)
                anim.start(self)
                
                if str(self.ans)==self.text and symbol == 4:
                    self.parent.score +=10
                    self.correct.play()
                elif str(self.ans)==self.text and symbol == 5:
                    self.parent.score += 6
                    self.correct.play()
                elif str(self.ans)==self.text and symbol == 3:
                    self.parent.score += 8
                    self.correct.play()
                elif str(self.ans)==self.text and symbol == 2:
                    self.parent.score += 4
                    self.correct.play()
                elif str(self.ans)==self.text and symbol == 1:
                    self.parent.score += 2
                    self.correct.play()

                else:
                    self.parent.score = 0
                    self.wrong.play()

                self.parent.clicked=True

class MyGame(RelativeLayout):
    
    wid_array=[]
    runing = BooleanProperty(True)
    clicked=BooleanProperty(False)
    score=NumericProperty(0)

    def on_kv_post(self, obj):
        self.wid_array=[]
        Clock.schedule_once(self.init2,)

    def on_score(self,obj,value):
        self.ids.sid.text=str(value)

    def init2(self,dt):
        self.ids.sid.text=str(self.score)
        self.wid_array=[]
        self.number_list=[]
        a,b=math()
        self.ans_list=[b+randint(1,10),b,b-randint(1,10)]
        print(self.ans_list)
        self.ans_list=sample(self.ans_list,len(self.ans_list))
        print(self.ans_list)
        print(self.ids)
        self.ids.qid.text=str(a)

        delta = -200
        for i in range(3):
            x=self.center_x + delta

            self.mywid=SB(bold=1,center_x=x,center_y=50,text=str(self.ans_list[i]),size_hint=(None,None),ans=b)
            self.wid_array.append(self.mywid)
            self.add_widget(self.mywid)
            delta+=200

        Clock.schedule_interval(self.game_loop, 1/33)

    def game_loop(self,dt):
        if self.runing:
            print(self.score)
            print('in game loop',dt)
            for i in self.wid_array:
                (i.center_x,i.center_y)=Vector(0,5)+(i.center_x,i.center_y)
                if i.center_y>self.height:
                    a,b=math()
                    self.ans_list=[b+randint(1,10),b,b-randint(1,10)]
                    self.ans_list=sample(self.ans_list,len(self.ans_list))
                    for j in range(3):
                        self.wid_array[j].text=str(self.ans_list[j])
                        self.wid_array[j].ans=b
                        self.ids.qid.text=str(a)

                    i.center_y=-100
                    self.clicked=False
    
    def _update_rect(self,*arg):
        delta = -200
        if len(self.wid_array)>0:
            for i in range(3):
                x = self.center_x + delta 
                self.wid_array[i].center_x = x
                delta += 200
    
    on_size = _update_rect
    on_os = _update_rect

class MyApp(App):
    def build(self):
        return MyGame()
    
MyApp().run()