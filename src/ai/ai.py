import multiprocessing
import os
import pickle
import random

import neat
import numpy as np



from ai.learn import Learn

runs_per_net = 2



def replay_genome():
    # Load requried NEAT config
    local_dir = os.path.dirname(__file__)
    genome_path = os.path.join(local_dir,"winner")
    config_path = os.path.join(local_dir, 'config')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    print(genomes)
    for i in range(10):
        eval_genome(genome, config,True)


# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config,p = False):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []

    for runs in range(runs_per_net):
        while 1:
            try:
                env = Learn()
                break
            except:
                continue
        done = False
        while not done:

            action = net.activate(env.get_data())
            done = env.step(action)
            if p:
                print ('data',env.get_data(),'answer',action)
        fitness = env.end()
        fitnesses.append(fitness)
        print(fitness)
    return np.mean(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    print("starting")
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop =  neat.Checkpointer.restore_checkpoint('neat-checkpoint-899')#neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.Checkpointer(50,9999999999))
    print("start learning")
    pe = neat.ParallelEvaluator(6, eval_genome)
    winner = pop.run(pe.evaluate,1)
    



    # Save the winner.
    with open(os.path.join(local_dir,'winner'), 'wb') as f:
        pickle.dump(winner, f)

    print(winner)
    replay_genome()




if __name__ == '__main__':
    run()