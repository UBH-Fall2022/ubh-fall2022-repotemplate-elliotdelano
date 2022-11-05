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
    @staticmethod
    def cross_over(par1, par2):
        map_a = par1.map.flatten()
        map_b = par2.map.flatten()
        centromere = np.random.choice(range(len(map_a)), 10, replace=False)
        centromere.sort()
        centromere = np.insert(centromere, 0, 0)
        map = []
        for i in range(len(centromere)):
            if np.random.rand() > 0.5:
                mini = map_a[centromere[i]:centromere[i+1] if i < len(centromere) - 1 else len(map_a)]
                for i in mini:
                    map.append(i if np.random.rand() > ga.mutation_rate else np.random.randint(0, 2))
            else:
                mini = map_b[centromere[i]:centromere[i+1] if i < len(centromere) - 1 else len(map_b)]
                for i in mini:
                    map.append(i if np.random.rand() > ga.mutation_rate else np.random.randint(0, 2))
        map = np.reshape(map, (par1.size, par1.size))
        return member.from_map(map)
    # one for creating directly from map
    @classmethod
    def from_map(cls, map):
        ob = cls.__new__(cls)
        ob.map = map
        ob.size = len(map)
        ob.fitness = 0
        return ob

class ga:
    mutation_rate = 0.
    def __init__(self, mutation_rate = 0, pop_size = 25, m_size = 50, gen_stop = 100):
        self.m_size = m_size
        ga.mutation_rate = mutation_rate
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
        self.curr_gen = 0
        while(not self.stop_condition()):
            self.get_fitness()
            self.order_pop()
            print(f'Best of gen {self.curr_gen}:')
            print(self.population[len(self.population)-1].map)
            print()
            self.cull_pop()
            self.repopulate()
            self.curr_gen += 1
        self.get_fitness()
        self.order_pop()
        return self.population[len(self.population)-1]



    #TODO: check for stop
    #TODO: stop conditional function
    def stop_condition(self):
        if self.curr_gen > self.gen_stop:
            return True
        return False

# g = ga(m_size=10, mutation_rate=0.02)
# g.start()

# par1 = member(10)
# par2 = member(10)
# child = member.cross_over(par1, par2)
# print(child.map)