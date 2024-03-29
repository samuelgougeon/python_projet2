"""Module pour afficher la fenêtre graphique"""
import turtle
import quoridor


class QuoridorX(quoridor.Quoridor):
    """Extension de la classe Quoridor pour créer une fenêtre graphique"""
    def afficher(self):
        """Pour créer la fenêtre graphique"""
        wn = turtle.Screen()
        wn.setup(464, 564)
        le = turtle.Turtle()
        le.penup()
        le.goto(0, 254)
        le.write('Légende: bleu={}, rouge={}'.format(self.joueurs[0], self.joueurs[1]),
                 True, 'center', font=('Cambria', 14))
        damier = turtle.Turtle()
        damier.shape('square')
        damier.shapesize(2)
        damier.color('grey')
        damier.penup()
        damier.speed(0)
        ho = turtle.Turtle()
        ho.shape('square')
        ho.shapesize(0.3, 4.4)
        ho.color('black')
        ho.penup()
        ho.speed(0)
        ve = turtle.Turtle()
        ve.shape('square')
        ve.shapesize(4.4, 0.3)
        ve.color('black')
        ve.penup()
        ve.speed(0)
        j1 = turtle.Turtle()
        j1.shape('circle')
        j1.color('blue')
        j1.penup()
        j2 = turtle.Turtle()
        j2.shape('circle')
        j2.color('red')
        j2.penup()
        for i in self.murs['horizontaux']:
            ho.goto(i[0]*48 - 216, i[1]*48 - 264)
            ho.stamp()
        for i in self.murs['verticaux']:
            ve.goto(i[0]*48 - 264, i[1]*48 - 216)
            ve.stamp() 
        for y in range(9):
            for x in range(9):
                screen_x = -192 + (x*48)
                screen_y = 192 - (y*48)
                damier.goto(screen_x, screen_y)
                damier.stamp()
        j1.goto((self.joueurs[0]['pos'][0])*48 - 240, (self.joueurs[0]['pos'][1])*48 - 240)
        j2.goto((self.joueurs[1]['pos'][0])*48 - 240, (self.joueurs[1]['pos'][1])*48 - 240)
        wn.mainloop()

