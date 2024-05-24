from manim import *

class Greetings(Scene):
    def construct(self):
        text = Text("Happy Birthday,")
        self.play(Write(text.set_color(PURPLE)))
        self.wait(1)
        text2 = Text("Thanku!").next_to(text, DOWN)
        self.play(Write(text2.set_color(PURPLE)))
        self.wait(1)
        self.play(FadeOut(text))
        self.play(FadeOut(text2))
        self.wait()

if __name__ == "__main__":
    scene = Greetings()
    scene.render()