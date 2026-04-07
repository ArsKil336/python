from md import *  # noqa: F403
from random import randint
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label   
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

k=4
Window.size = (250*k, 200*k)
Window.clearcolor = (255/255, 186/255, 3/225, 1)
Window.title = "Конвертер"

class MyApp(App):
    def __init__(self):
        super().__init__()
        self.label = Label(text='Привет, Kivy!')
        self.miles = Label(text='Мили')
        self.metres = Label(text='Метры')
        self.santimetres = Label(text='Сантиметры')
        self.input_data = TextInput(hint_text='Введите значение (км)', multiline=False, text='0')
        self.input_data.bind(text=self.on_text)
        self.last_data=''
    def on_text(self, *args):
        data=self.input_data.text
        if data.isnumeric():
            self.miles.text='Мили: '+str(tryToInt(float(data)*0.62))
            self.metres.text='Метры: '+str(tryToInt(float(data)*1000))
            self.santimetres.text='Сантиметры: '+str(tryToInt(float(data)*100000))
            self.last_data=str(tryToInt(float(data)))
        elif data=='':
            self.miles.text='Мили: 0'
            self.metres.text='Метры: 0'
            self.santimetres.text='Сантиметры: 0'
        else:
            self.input_data.text=self.last_data
    def btn_pressed(self, *args):
        self.label.color = (randint(0,225)/225, randint(0,225)/225, randint(0,225)/225, 1)
    def build(self):
        box=BoxLayout(orientation='vertical')
        box.add_widget(self.label)
        box.add_widget(self.input_data)
        box.add_widget(self.miles)
        box.add_widget(self.metres)
        box.add_widget(self.santimetres)
        return box

if __name__ == '__main__':
    MyApp().run()