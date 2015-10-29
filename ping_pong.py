__author__ = 'Vitaha'
from livewires import games, color

#screen initiation
games.init(screen_width = 640, screen_height = 640, fps = 50)
sound = games.load_sound('ping_pong_8bit_plop.wav')

class Rocket(games.Sprite):
    """ping-pong rocket"""
    image = games.load_image('rocket.bmp')
    score = 0

    #score number when need to change difficulty
    cycle = 20

    def __init__(self, ball):
        """rocket constructor"""
        super(Rocket, self).__init__(image = Rocket.image,
                                  x = games.mouse.x,
                                  bottom = games.screen.height)

        #game score initiation
        self.score = games.Text(value = Rocket.score,
                                size = 25,
                                color = color.black,
                                top = 5,
                                right = games.screen.width - 10)
        games.screen.add(self.score)
        self.ball = ball

    def update(self):
        """gorizontal moving of rocket"""
        self.x = games.mouse.x
        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width

        #checking for ball catch
        self.check_catch()

        #change difficulty
        self.difficulty()

    def check_catch(self):
        """checking catch"""
        for ball in self.overlapping_sprites:
            if ball.bottom <= self.top + 1:
                Rocket.score += 10
                self.score.value = Rocket.score
                self.score.right = games.screen.width - 10
                ball.handle_catch()

    def difficulty(self):
        """difficulty change"""
        #creatre second ball
        if Rocket.cycle == 120 and Rocket.score == 120:
            Ball.speed = 0.5
            self.ball.speed_up()
            the_ball1 = Ball(x = 20, y = 20)
            games.screen.add(the_ball1)
            Rocket.cycle += 20

        #just speedUp
        elif Rocket.score/Rocket.cycle == 1:
            self.ball.speed_up()
            Rocket.cycle += 20

class Ball(games.Sprite):
    """flying ball"""
    image = games.load_image('ball.bmp')
    speed = 1

    def __init__(self, x = games.screen.width/2, y = games.screen.height/2):
        super(Ball, self).__init__(image = Ball.image,
                                    x = x, y = y,
                                    dx = Ball.speed,
                                    dy = Ball.speed)

    def update(self):
        """check for ball position and change speed"""
        if self.right > games.screen.width:
            self.dx = -self.dx
            sound.play()
        if self.left < 0:
            self.dx = -self.dx
            sound.play()
        if self.top < 0:
            self.dy = -self.dy
            sound.play()
        if self.bottom > games.screen.height:
            self.end_game()
            self.destroy()

    def handle_catch(self):
        """redirect handeled ball"""
        self.dy = - self.dy
        sound.play()

    def speed_up(self):
        """ball speed up"""
        Ball.speed += 0.5
        if self.dx > 0:
            self.dx = Ball.speed
        else:
            self.dx = - Ball.speed
        if self.dy > 0:
            self.dy = Ball.speed
        else:
            self.dy = - Ball.speed

    def end_game(self):
        """ending game"""
        end_message = games.Message(value = 'GAME OVER',
                                    size = 90,
                                    color = color.black,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 5 * games.screen.fps,
                                    after_death = games.screen.quit)
        score_message = games.Message(value = 'Score: ' + str(Rocket.score),
                                    size = 50,
                                    color = color.black,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2 + 100,
                                    lifetime = 5 * games.screen.fps)
        games.screen.add(end_message)
        games.screen.add(score_message)






def main():
    """main thred"""
    #init background
    wall_image = games.load_image('background1.jpg', transparent = False)
    games.screen.background = wall_image

    #init ball and rocket
    the_ball = Ball()
    games.screen.add(the_ball)
    the_rocket = Rocket(the_ball)
    games.screen.add(the_rocket)

    games.mouse.is_visible = False
    games.screen.event_grab = True
    games.screen.mainloop()

main()