from agent import Agent
from typing import Tuple
from graphics import * 

class Border:
    def __init__(self, agents: Tuple[Agent, Agent], p1: Point, p2: Point) -> None:
        self.agents = agents
        self.p1 = p1
        self.p2 = p2

        self.similarity = self.compute_similarity()
        
    def compute_similarity(self):
        return self.agents[0].compute_similarity(self.agents[1])

    def update_similiarity(self):
        self.similarity = self.compute_similarity()

    def compute_line_color(self):
        self.update_similiarity()
        gray_val = int(255 * self.similarity)
        return color_rgb(gray_val, gray_val, gray_val)

    def display(self, win: GraphWin) -> None:
        self.line_obj = Line(self.p1, self.p2)
        line_color = self.compute_line_color()
        self.line_obj.setFill(line_color)
        # self.line_obj.setOutline(line_color)
        self.line_obj.setWidth(10)
        self.line_obj.draw(win)

    def update_disp(self):
        new_color = self.compute_line_color()
        self.line_obj.setFill(new_color)
        # self.line_obj.setOutline(new_color)

    def __str__(self):
        return f"Border from {self.p1} to {self.p2} with similarity {self.similarity}"
    
