from typing import List, Type
from graphics import * 
import random

class Agent:
    def __init__(self, id: int, features: List[int], num_traits, onlineness = 0, sioa = False) -> None:
        self.id = id
        self.features = features
        self.num_features = len(features)
        self.num_traits = num_traits
        self.onlineness = onlineness
        self.sioa = sioa

    def __str__(self):
        return f"ID: {self.id}, num_features: {self.num_features}, num_traits: {self.num_traits}, onlineness: {self.onlineness}, SIOA: {self.sioa}\n\tFeature vector: {self.features}\n"


    def compute_agent_color(self) -> str: 
        gb_val = max(0, int(255 * (1-self.onlineness)**3))
        return color_rgb(255, gb_val, gb_val)

    # this could be changed later
    def compute_similarity(self, neighbor) -> float:
        matches = 0
        for i in range(self.num_features):
            if (self.features[i] == neighbor.features[i]):
                matches+=1
        return matches/self.num_features

    def display(self, win: GraphWin, p1: Point, p2: Point) -> None:
        self.agent_rect = Rectangle(p1, p2)
        agent_color = self.compute_agent_color()
        self.agent_rect.setFill(agent_color)
        self.agent_rect.draw(win)

    # def updateDisp(self):
    #     new_color = self.compute_agent_color()
    #     self.agent_rect.setFill(new_color)

    # returns true if a change was made
    def interact(self, neighbor) -> bool:
        similarity = self.compute_similarity(neighbor)
        # print(f"Similarity: {similarity}")
        # cached_vec = [x for x in self.features]

        if (random.random() < similarity): 
            # randomly select feature to change
            while similarity != 1: # if they are identical there is nothing to change
                # print("running loop for agent with id", self.id, "and similiarity", similarity)
                poss_feature_idx = random.randint(0, self.num_features-1)
                neighbor_ft_val = neighbor.features[poss_feature_idx]
                # if this site is different change it
                if self.features[poss_feature_idx] != neighbor_ft_val:  
                    self.features[poss_feature_idx] = neighbor_ft_val
                    return True
            # self.updateDisp()
            # print(f"Updated {cached_vec} to {self.features}")
        return False
        