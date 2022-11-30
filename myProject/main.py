import kivy
from kivymd.app import  MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty,DictProperty,OptionProperty,BooleanProperty
from kivy.lang.builder import Builder
from demo.demo import profiles

Builder.load_file('story.kv')
Builder.load_file('avatar.kv')
Builder.load_file('chat_screen.kv')
Builder.load_file('chat_list_item.kv')
Builder.load_file('text_feild.kv')
Builder.load_file('chat_bubble.kv')

Window.size=(360,600)
class WindowManager(ScreenManager):
    ''' aSDD'''
class MessageScreen(Screen):
    '''ASDASF'''
class ChatBubble(MDBoxLayout):
    profile = DictProperty()
    msg = StringProperty()
    time = StringProperty()
    sender = StringProperty()
    isRead = OptionProperty('waiting', options=['read', 'delivered', 'waiting'])
class StoryWithImage(MDBoxLayout):
    text = StringProperty()
    source=StringProperty()
class ChatListItem(MDCard):
    mssg = StringProperty()
    friend_avatar =StringProperty()
    timestamp= StringProperty()
    profile= DictProperty()
    isRead=OptionProperty(None,options=['delivered','read','new','waiting'])
    friend_name=StringProperty()

class ChatScreen(Screen):
    text=StringProperty()
    image=StringProperty()
    active=BooleanProperty()


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style='Dark'
        self.theme_cls.primary_palette='Red'
        self.theme_cls.accent_palette='Teal'
        self.theme_cls_accent_hue='400'
        self.title='CHAT_BOT'
        screens=[
            MessageScreen(name="message"),
            ChatScreen(name="chat_screen")
        ]
        self.wm=WindowManager(transition= FadeTransition())
        for S in screens:
            self.wm.add_widget(S)
        self.story_builder()
        self.chat_list_builder()
        return self.wm
    def story_builder(self):
        for profile in profiles:
            self.story=StoryWithImage()
            self.story.text=profile['name']
            self.story.source=profile['image']
            self.wm.screens[0].ids['story_layout'].add_widget(self.story)
    def chat_list_builder(self):
        for profile in profiles:
            for mg in profile['msg']:
                self.chatitem=ChatListItem()
                self.chatitem.profile=profile
                self.chatitem.friend_name=profile["name"]
                self.chatitem.friend_avatar=profile["image"]
                lastmessage, time, isRead, sender = mg.split(';')
                self.chatitem.mssg = lastmessage
                self.chatitem.timestamp = time
                self.chatitem.isRead = isRead
                self.chatitem.sender = sender
            self.wm.screens[0].ids['chatlist'].add_widget(self.chatitem)
    def change_screen(self,screen):
        self.wm.current=screen
    def create_chat(self,profile):
        self.chat_screen=ChatScreen()
        self.chat_screen.text=profile['name']
        self.chat_screen.image=profile['image']
        self.chat_screen.active=profile['active']
        self.msg_builder(profile,self.chat_screen)
        self.wm.switch_to(self.chat_screen)
    def msg_builder(self,profiles,screen):
        for mg in profiles['msg']:
            if mg!='':
                message,time,isRead,sender=mg.split(';')
                self.chatmsg=ChatBubble() 
                self.chatmsg.msg = message
                self.chatmsg.time = time
                self.chatmsg.isRead = isRead
                self.chatmsg.sender = sender
                screen.ids['msgList'].add_widget(self.chatmsg) 

if __name__=="__main__":
    MainApp().run()