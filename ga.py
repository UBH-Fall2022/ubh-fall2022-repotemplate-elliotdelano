import numpy

# main algorithm file 
# controls the logic behind gentic algorithm
# runs generations 
# fitness functions
# crossing over

class ga:
    def __init__(self, size = 50, mutation_rate = 0, pop_size = 25, gen_stop = 100):
        self.size = size
        self.mutation_rate = mutation_rate
        self.pop_size = pop_size
        self.gen_stop = gen_stop

    #TODO: start function
    def start(self):
        self.population = self.new_population()
        self.run()

    #TODO: initialize population

    #TODO: write fitness function

    #TODO: cull population

    #TODO: crossing over

    #TODO: recursive control function

    #TODO: check for stop

    #TODO: stop conditional function