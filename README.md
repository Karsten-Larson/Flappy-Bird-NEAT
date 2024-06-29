# Flappy Bird NEAT

This project uses the [NeuroEvolution of Augmenting Topologies (NEAT) algorithm](https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies) to train Intelligence Agents (IA) to play the game of Flappy Bird. IAs go through numerous rounds of training to determine how they will respond in the future (this is covered in further detail later). This project relies on the Python NEAT library, `neat-python`.

This project is heavily influenced by Danny Zhu's [Medium Post](https://medium.com/analytics-vidhya/how-i-built-an-ai-to-play-flappy-bird-81b672b66521) and Tech with Tim's [Flappy Bird Playlist](https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2). I utilized many of their ideas and implemented a greater object-oriented approach in the overall design of the project.

## Usage

### Installation

To install all required dependencies run:

```
pip install -r requirements.txt
```

### Running

To find the best NEAT Flappy Bird object, the file `src/neat_game.py` must be run first.

```
python3 src/neat_game.py
```

After viewing the best bird file execute `src/test_neat_game.py`.

```
python3 src/test_neat_game.py
```

### Modifications

To modify any game conditions or NEAT configuration the `src/settings.py` and `src/neat-config.cfg` files can be edited respectively.
