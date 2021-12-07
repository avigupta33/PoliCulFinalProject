# from time import sleep
from model import Model
from graphics import *
from PIL import Image
from experiment import Experiment
import os

TK_SILENCE_DEPRECATION=1

def extract_image(filename):
    fig = Image.open(filename + ".eps")
    image_png= filename + '.png'
    fig.save(image_png, lossless = True)  

def display_model(model: Model):
    win = GraphWin(width = 500, height = 500) # create a window

    win.setCoords(0, 0, model.num_rows + 2, model.num_cols + 2) # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)

    label = model.get_top_label()
    label.draw(win)
            
    model.display(win)
    return win

if __name__ == "__main__":
    experiment_list = [
        Experiment(max_frames = 1000000, num_trials = 5, num_features = 15, num_traits = 15, prop_agent_online=pao/10, agent_online_val=aov/10, min_sioa_cnt=1, max_sioa_cnt=1) for pao in range(11) for aov in range(11)
    ]

    for experiment in experiment_list:
        models = experiment.generate_models()
        cat_string = experiment.get_cat_string()

        for model in models:
            for folder in ["images", "exports"]:
                if not os.path.exists(folder + "/"+cat_string):
                    os.makedirs(folder + "/" + cat_string)

            filename = f"{cat_string}/id{model.id}_{cat_string}"
       
            if model.do_display:
                win = display_model(model)
            
            pt_counter = 0
            frame_counter = 0
        
            while pt_counter < experiment.patience and frame_counter < experiment.max_frames:
                changed = model.interact()
                frame_counter += 1
                if changed:
                    pt_counter = 0
                else:
                    pt_counter += 1
                model.update_text(f"Frame: {frame_counter}")
                if model.do_display:
                    if win.checkKey() == 'q':        
                        break

            if not model.do_display:
                win = display_model(model)
            
            win.postscript(file = f"images/{filename}.eps")
            extract_image("images/" + filename)
            model.export("exports/" + filename)
            # model.printAgents()
            win.close()