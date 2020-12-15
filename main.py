from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button, ButtonBehavior

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
            
        if self.player1.score == 10:
            self.player1.score = 0
            self.player2.score = 0
            self.createPopUp("Game Over","Player1 Wins")
            
            
        if self.player2.score == 10:
            self.player1.score = 0
            self.player2.score = 0
            self.createPopUp("Game Over", "PLayer2 Wins")

    def createPopUp(self,title,msg):
        box = BoxLayout(orientation = 'vertical', padding = (10))
        box.add_widget(Label(text = msg,font_size='15sp'))
        btn1 = Button(text = "Ok")
        box.add_widget(btn1)
        popup = Popup(title=title, title_size= (10),title_align = 'center', content = box,size_hint=(None, None), size=(400, 200), auto_dismiss = True)
        btn1.bind(on_press = popup.dismiss)
        popup.open()
                
            
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.player1.center_y += 50
        elif keycode[1] == 's':
            self.player1.center_y -= 50
        elif keycode[1] == 'up':
            self.player2.center_y += 50
        elif keycode[1] == 'down':
            self.player2.center_y -= 50
        return True

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game
    


if __name__ == '__main__':
    PongApp().run()