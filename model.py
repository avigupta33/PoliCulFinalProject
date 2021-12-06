from typing import List, Tuple
from agent import Agent
from border import Border
import collections

import random
from graphics import *

class Model:
    def __init__(self, id: int, num_rows: int, num_cols: int, 
    num_features: int, num_traits: int, wrap: bool = False, onlineness: float = 0, prop_agent_online: float = 0, agent_online_val: float = 0, sioa_descrips: List[Tuple[str, int]] = None, do_display: bool = True) -> None: 
        self.id = id
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.wrap = wrap
        self.num_features = num_features
        self.num_traits = num_traits
        self.onlineness = onlineness
        self.prop_agent_online = prop_agent_online
        self.agent_online_val = agent_online_val
        self.agents_online = (prop_agent_online != 0 and agent_online_val!=0)
        self.sioa_descrips = sioa_descrips
        self.do_display = do_display

        self.sioas = None
        if self.sioa_descrips is not None and len(self.sioa_descrips) != 0:
            self.initialize_SIOAs()


        self.borders = []
        self.agent_coords_to_borders = collections.defaultdict(list)
        self.online_agent_coords = {} # maps coords of all agents who are online to their onlineness values

        self.ordered_online_agent_coords = None
        self.online_weights = None

        self.agents = self.initialize_agents()
        self.neighbor_cache = {}
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.neighbor_cache[(i,j)] = self.get_neighbors((i, j))
        self.text = Text(Point((self.num_cols + 1)/2, 0.5), "")
        self.total_agent_onlineness = self.compute_total_agent_onlineness()
        self.total_sioa_onlineness = self.compute_total_SIOA_onlineness()

    def get_agent_onlineness_init_value(self):
        if random.random() < self.prop_agent_online:
            return self.agent_online_val
        else:
            return 0
    
    def compute_total_agent_onlineness(self):
        return sum(self.online_agent_coords.values())

    def compute_total_SIOA_onlineness(self):
        if self.sioas is not None:
            return sum(agent.onlineness for agent in self.sioas)
        else:
            return 0

    def initialize_SIOAs(self):
        if self.sioa_descrips is None:
            print("ERROR in initialize_SIOAs")
            return

        self.sioas = []

        id = 1001 + self.num_rows * self.num_cols
        for descrip in self.sioa_descrips:
            instruct, numToCreate = descrip # instruct = 'max' or 'min'

            for _ in range(numToCreate):

                feature_vec = []
                if instruct == "max":
                    feature_vec = [self.num_traits for _ in range(self.num_features)]
                elif instruct == "min":
                    feature_vec = [1 for _ in range(self.num_features)]

                else:
                    print("bad instruct string")

                agent = Agent(id = id, features = feature_vec, num_traits=self.num_traits, onlineness=1, sioa = True)
                id += 1
                self.sioas.append(agent)


    # create agents with random values for features and add to model
    def initialize_agents(self) -> List[List[Agent]]:
        agents = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]

        id = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                featureVec = random.choices(range(1, self.num_traits + 1), k = self.num_features)
                # print(f"init featureVec: {featureVec}")
                agent_onlineness = 0
                if self.agents_online:
                    agent_onlineness = self.get_agent_onlineness_init_value()
                agent = Agent(id, featureVec, self.num_traits, onlineness = agent_onlineness)
                if agent_onlineness > 0:
                    self.online_agent_coords[(row, col)] = agent_onlineness
                agents[row][col] = agent
                if col != 0: # if not leftmost, it needs a left border
                    left_border = Border(
                        (agent, agents[row][col-1]), 
                        Point(col + 1, row + 1),
                        Point(col + 1, row + 2)
                    )
                    self.borders.append(left_border)
                    self.agent_coords_to_borders[(row, col)].append(left_border)
                    self.agent_coords_to_borders[(row, col - 1)].append(left_border)
               
                if row != 0: # if not topmost, needs a top border
                    top_border = Border(
                        (agent, agents[row -1][col]), 
                        Point(col + 1, row + 1),
                        Point(col + 2, row + 1)
                    )
                    self.borders.append(top_border)
                    self.agent_coords_to_borders[(row, col)].append(top_border)
                    self.agent_coords_to_borders[(row - 1, col)].append(top_border)

                id += 1

        if self.wrap: # add wrap borders
            for col in range(self.num_cols):
                top_border = Border(
                        (agents[0][col], agents[self.num_rows -1][col]), 
                        Point(col + 1, 1),
                        Point(col + 2, 1)
                    )
                bottom_border = Border(
                        (agents[0][col], agents[self.num_rows -1][col]), 
                        Point(col + 1, self.num_rows + 1),
                        Point(col + 2, self.num_rows + 1)
                    )
                self.agent_coords_to_borders[(0, col)].append(top_border)
                self.agent_coords_to_borders[(0, col)].append(bottom_border)

                self.agent_coords_to_borders[(self.num_rows-1, col)].append(top_border)
                self.agent_coords_to_borders[(self.num_rows-1, col)].append(bottom_border)

                self.borders.append(top_border)
                self.borders.append(bottom_border)

            for row in range(self.num_rows):
                left_border = Border(
                        (agents[row][0], agents[row][self.num_cols - 1]), 
                        Point(1, row + 1),
                        Point(1, row + 2)
                    )
                right_border = Border(
                        (agents[row][0], agents[row][self.num_cols - 1]), 
                        Point(self.num_cols + 1, row + 1),
                        Point(self.num_cols + 1, row + 2)
                    )
                self.agent_coords_to_borders[(row, 0)].append(left_border)
                self.agent_coords_to_borders[(row, 0)].append(right_border)

                self.agent_coords_to_borders[(row, self.num_cols - 1)].append(left_border)
                self.agent_coords_to_borders[(row, self.num_cols - 1)].append(right_border)

                self.borders.append(left_border)
                self.borders.append(right_border)

        return agents

    def printAgents(self):
        print(f"Printing {len(self.agents)} agents for model.")
        for row in self.agents:
            for agent in row:
                print(agent)
    
    def export(self, filename):
        f = open(filename + ".txt", "w")
        params = vars(self)
        for key in params:
            if key not in ["borders", "agent_coords_to_borders", "agents", "neighbor_cache", "text", "sioas"]:
                f.write(f"{str(key)}:{str(params[key])}\n")
        for row_num in range(len(self.agents)):
            row = self.agents[row_num]
            for col_num in range(len(row)):
                agent = row[col_num]
                f.write(f"Row: {row_num} Col: {col_num}, " + str(agent))
        for sioa in self.sioas:
            f.write(str(sioa))
        f.close()


    def update_text(self, s: str) -> None:
        self.text.setText(s)
     
    def display(self, win: GraphWin) -> None:    
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                agent = self.agents[row][col]
                p1 = Point(col + 1, row + 1)
                p2 = Point(col + 2, row + 2)
                agent.display(win, p1, p2)
        for border in self.borders:
            border.display(win)
        self.text.draw(win)
        outer_rect = Rectangle(Point(1,1), Point(self.num_cols + 1, self.num_rows + 1))
        outer_rect.draw(win)

    def select_random_online_coords(self):
        if self.online_weights is None or self.ordered_online_agent_coords is None:
            self.online_weights = []
            self.ordered_online_agent_coords = []
            for coords in self.online_agent_coords:
                self.ordered_online_agent_coords.append(coords)
                self.online_weights.append(self.online_agent_coords[coords]/self.total_agent_onlineness)

        sioa_probability = self.total_sioa_onlineness/(self.total_agent_onlineness + self.total_sioa_onlineness)

        if random.random() < sioa_probability:  # format for SIOA return: ('sioa', idx)
            sioa_idx = random.randint(0, len(self.sioas) - 1)
            return ('sioa', sioa_idx)
        else:

            return random.choices(self.ordered_online_agent_coords, weights = self.online_weights, k = 1)[0]
    
    def select_random_coords(self) -> Tuple:
        rand_row = random.randint(0, self.num_rows - 1)
        rand_col = random.randint(0, self.num_cols - 1)
        return rand_row, rand_col

    # returns list of neighbors for agent denoted by row, col
    def get_neighbors(self, coords: Tuple[int, int]) -> List[Tuple]:
        row, col = coords
        neighbors = []
        if (row + 1 < self.num_rows):
            neighbors.append((row + 1, col))

            # if (col + 1 < self.num_cols):
            #     neighbors.append((row + 1, col + 1))
            # if (col - 1 >= 0):
            #     neighbors.append((row + 1, col - 1))

        if (col + 1 < self.num_cols):
            neighbors.append((row, col + 1))
        if (col - 1 >= 0):
            neighbors.append((row, col -1))
        
        if (row - 1 >= 0):
            neighbors.append((row - 1, col))

            # if (col + 1 < self.num_cols):
            #     neighbors.append((row - 1, col + 1))
            # if (col - 1 >= 0):
            #     neighbors.append((row - 1, col - 1))
        if self.wrap:  # add wrapped neighbors
            if row == 0:
                neighbors.append((self.num_rows -1, col))
                # if col - 1 >= 0:
                #     neighbors.append((self.num_rows -1, col - 1))
                # if col + 1 < self.num_cols:
                #     neighbors.append((self.num_rows -1, col + 1))
            elif row == self.num_rows - 1:
                neighbors.append((0, col))
                # if col - 1 >= 0:
                #     neighbors.append((0, col - 1))
                # if col + 1 < self.num_cols:
                #     neighbors.append((0, col + 1))
            if col == 0:
                neighbors.append((row, self.num_cols-1))
                # if row - 1 >= 0:
                #     neighbors.append((row - 1, self.num_cols-1))
                # if row + 1 < self.num_rows:
                #     neighbors.append((row + 1, self.num_cols-1))
            elif col == self.num_cols - 1:
                neighbors.append((row, 0))
                # if row - 1 >= 0:
                #     neighbors.append((row - 1, 0))
                # if row + 1 < self.num_rows:
                #     neighbors.append((row + 1, 0))

            # deal with corners which double wrap
            # if row == 0:
            #     if col == 0:
            #         neighbors.append((self.num_rows - 1, self.num_cols - 1))
            #     elif col == self.num_cols-1:
            #         neighbors.append((self.num_rows-1, 0))
            # elif row == self.num_rows - 1: 
            #     if col == 0:
            #         neighbors.append((0, self.num_cols - 1))
            #     if col == self.num_cols - 1:
            #         neighbors.append((0,0))
            
        return neighbors
    
    def get_agent_from_coords(self, coords: Tuple) -> Agent:
        return self.agents[coords[0]][coords[1]]

    def get_top_label(self) -> Text:
        return Text(Point((self.num_cols + 1)/2, self.num_rows + 1.5), 
        f"id: {self.id}, nF: {self.num_features}, nT: {self.num_traits}, PAO: {self.prop_agent_online}, AOV: {self.agent_online_val}, SIOAs: {self.sioa_descrips}")


    def interact(self) -> bool: # returns true iff a change was actually made
        agent_coords = self.select_random_coords()
        agent = self.get_agent_from_coords(agent_coords)
        sioa_interaction = False

        if self.agents_online and random.random() < agent.onlineness:
            assert self.onlineness == 0, "Bad onlineness params"
            while True:
                neighbor_coords = self.select_random_online_coords()
                if neighbor_coords[0] == 'sioa':
                    sioa_interaction = True
                    break

                elif neighbor_coords != agent_coords:
                    break
            # print(f"Online, {agent_coords} with {neighbor_coords}")

        elif self.onlineness != 0 and random.random() < self.onlineness:
            while True:
                neighbor_coords = self.select_random_coords()
                if  neighbor_coords != agent_coords:
                    break
            # print("Online")

        else:
            # neighbors = self.getNeighbors(agent_coords)
            neighbors = self.neighbor_cache[agent_coords]
            neighbor_coords = random.choice(neighbors)

        if sioa_interaction:
            neighbor = self.sioas[neighbor_coords[1]]
            # print(f"Interaction with SIOA at idx {neighbor_coords[1]}")
        else:  
            neighbor = self.get_agent_from_coords(neighbor_coords)

        # print(f"Agent at {agent_coords} selected to interact")
        # print(f"Neighbor at {neighbor_coords} selected to interact")

        # if sioa_interaction:
        #     print(f"Interacting with {str(neighbor)}")
        #     print(f"Before SIOA interaction: {agent.features}")
        # else:
        #     print(f"Before reg interaction: {agent.features}")

        ret_val = agent.interact(neighbor)

        # if sioa_interaction:
        #     print(f"After SIOA interaction: {agent.features}")
        # else:
        #     print(f"After reg interaction: {agent.features}")

        if self.do_display:

            agent_borders = self.agent_coords_to_borders[agent_coords]
            # print(border for border in agent_borders)
            for border in agent_borders:
                # print(border, 'updated')
                border.update_disp()
            # if ret_val and sioa_interaction:
            #     print(f"After SIOA interaction: {agent.features}")
        return ret_val

    def verify_neighbors(self) -> None:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                neighbors = self.get_neighbors((i,j))
                expected = 4
                if not self.wrap:
                    if i == 0 or i == self.num_rows - 1:
                        if j == 0 or j == self.num_cols - 1:
                            expected = 2
                        else:
                            expected = 3
                    elif j == 0 or j == self.num_cols - 1:
                        expected = 3
                    
                assert len(neighbors) == expected and len(set(neighbors)) == len(neighbors), f"Failed on ({i},{j}), which has neighbors {neighbors}. We expected {expected}."  

