# Python setup
Hello there! This is a quick setup tutorial for beginers. If you already know how to get started, feel free to skip this part [here](@FlappyBird). <br/>
First of all, we need to install python, which is a easy process, to do so I recomend this [Video](https://www.youtube.com/watch?v=i-MuSAwgwCU).

## Module download
The zip file can be downloaded [here](https://github.com/joaoartursilveira/FlappybirdIA/archive/refs/heads/master.zip). 
Unzip wherever you prefer to house the module.

## Virtual environment
We need to create a virtual enviromnent, or 'venv', to install all dependencies and run the code. Follow the steps bellow:
1. Navigate to the chosen folder housing the module.
2. Write "cmd" (without quotation marks) on the file explorer and the command window will pop up.
3. Write "python -m venv venv" (without quotation marks) and it'll create the venv.
4. Activate the venv with "venv\scripts\activate"; the prefix (venv) will appear, showing the venv is active.
5. Write "pip install -r requirements.txt" (without quotation marks) to install all dependencies we need.

Surprisingly enough, that's it, we are ready to start the fun part, which is interating with the module.

# Flappy Bird
The game was created using pygame libary, which takes images as input and emulates them. <br/>
I splitted the module in two files: train_birds.py, which, the name suggests, is the traning part, and test_bird.py, which is the test part. <br/>
There's already a trained AI to play the game for you, but feel free to do as you wish.

## Training part
Here the NEAT python module generate a series of neural network to play the game. Every time all birds die without reaching the fitness threshold,
the game will reset and the best performing birds will pass on that network and NEAT will improve it. This process is repeated until we get our fitness threshold
or a bird reach a score of 80, then, with the useful pickle libary, the winning AI will be pickled and saved to be used in the test part.

## Test part
Loads the AI saved on the pickle file and play the game until you are tired of watching it. It's fun watching the bird jump, though.

## Create your own AI
Now that you already saw the bird in action, you can mess around with the config-feedforward.txt file to test new configurations. I recomend the module docs
[here](https://neat-python.readthedocs.io/en/latest/) as there is a lot of cool features to explore.
