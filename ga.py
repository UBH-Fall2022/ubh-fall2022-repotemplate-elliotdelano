import numpy as np

# main algorithm file 
# controls the logic behind gentic algorithm
# runs generations 
# fitness functions
# crossing over

class member:
    def __init__(self, size):
        self.size = size
        self.map = np.random.randint(0,2, size=(self.size, self.size))
        self.fitness = 0

    #TODO: create two factory functions
    # one for crossing over
    @classmethod
    def cross_over(cls, par1, par2):
        return None
    # one for creating directly from map
    @classmethod
    def from_map(cls, map):
        return None

class ga:
    def __init__(self, mutation_rate = 0, pop_size = 25, m_size = 50, gen_stop = 100):
        self.m_size = m_size
        self.mutation_rate = mutation_rate
        self.pop_size = pop_size
        self.gen_stop = gen_stop

    #TODO: start function
    def start(self):
        self.new_population()
        self.run()

    #TODO: initialize population
    def new_population(self):
        self.population = [member(self.m_size) for i in range(self.pop_size)]

    #TODO: write fitness function
    def get_fitness(self):
        for m in self.population:
            m.fitness = ga.fitness(m.map)

    @staticmethod
    def fitness(map):
        return np.average(map)

    def order_pop(self):
        self.population.sort(key=lambda val: val.fitness)

    #TODO: cull population
    def cull_pop(self):
        self.population = self.population[-10:]

    #TODO: crossing over
    def repopulate(self):
        old_pop = self.population
        new_pop = [m for m in self.population]
        for i in range(self.pop_size - len(self.population)):
            new_pop.append(ga.cross_over(old_pop))
        self.population = new_pop

    @staticmethod
    def cross_over(pop):
        par1 = pop[np.random.randint(0, len(pop))]
        par2 = pop[np.random.randint(0, len(pop))]
        if par1 == par2:
            return ga.cross_over(pop)
        return member.cross_over(par1, par2)
        
    #TODO: recursive control function
    def run(self):
        while(not self.stop_condition()):
            self.get_fitness()
            self.order_pop()
            self.cull_pop()
            self.repopulate()

    #TODO: check for stop
    #TODO: stop conditional function
    def stop_condition(self):
        if self.curr_gen > self.gen_stop:
            return True
        return False

g = ga()
g.start()