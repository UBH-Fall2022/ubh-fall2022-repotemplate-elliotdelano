import numpy as np
from numba import jit, cuda

# main algorithm file 
# controls the logic behind gentic algorithm
# runs generations 
# fitness functions
# crossing over

@jit(target_backend='cuda')
def flood_score(y,x, m, type):
    flooded = {}
    queue = []
    queue.append((y,x))
    total = 0
    while(len(queue)>0):
        y, x = queue.pop()
        total+=1
        flooded[str(y)+str(x)] = 1
        if y + 1 < len(m):
            if m[y+1][x] == type:
                if str(y+1)+str(x) not in flooded:
                    queue.append((y+1, x))
        if y - 1 > -1:
            if m[y-1][x] == type:
                if str(y-1)+str(x) not in flooded:
                    queue.append((y-1, x))
        if x + 1 < len(m):
            if m[y][x+1] == type:
                if str(y)+str(x+1) not in flooded:
                    queue.append((y, x+1))
        if x - 1 > -1:
            if m[y][x-1] == type:
                if str(y)+str(x-1) not in flooded:
                    queue.append((y, x-1))
    return total

@jit(target_backend='cuda')
def find_flood_score(map):
    flood_score = []
    flooded = {}
    for y_in in range(len(map)):
        for x_in, v in enumerate(map[y_in]):
            if v != 1: continue
            if str(y_in)+str(x_in) in flooded: continue
            flooded[str(y_in)+str(x_in)] = 1
            total = 0
            queue = []
            queue.append((y_in,x_in))
            while(len(queue)>0):
                y, x = queue.pop()
                total+=1
                flooded[str(y)+str(x)] = 1
                if y + 1 < len(map):
                    if map[y+1][x] == 1:
                        if str(y+1)+str(x) not in flooded:
                            queue.append((y+1, x))
                if y - 1 > -1:
                    if map[y-1][x] == 1:
                        if str(y-1)+str(x) not in flooded:
                            queue.append((y-1, x))
                if x + 1 < len(map):
                    if map[y][x+1] == 1:
                        if str(y)+str(x+1) not in flooded:
                            queue.append((y, x+1))
                if x - 1 > -1:
                    if map[y][x-1] == 1:
                        if str(y)+str(x-1) not in flooded:
                            queue.append((y, x-1))
            flood_score.append(total)
    return sum(flood_score)/len(flood_score)

class member:
    def __init__(self, size):
        self.size = size
        self.map = np.random.randint(0,3, size=(self.size, self.size))
        self.fitness = 0

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
    def __init__(self, mutation_rate = 0, pop_size = 25, m_size = 50, gen_stop = 100, call_back=lambda arg: None):
        self.m_size = m_size
        ga.mutation_rate = mutation_rate
        self.pop_size = pop_size
        self.gen_stop = gen_stop
        self.call_back = call_back
        self.curr_gen = 0
        self.ftn_track = []

    def start(self):
        self.new_population()
        return self.run()

    def new_population(self):
        self.population = [member(self.m_size) for i in range(self.pop_size)]

    def get_fitness(self):
        for m in self.population:
            m.fitness = ga.fitness(m.map)
    
   
    # 
    @staticmethod
    @jit(target_backend='cuda')
    def fitness(map):
        water_score = 0
        land_score = 0
        desert_score = 0

        # print(map)
        max_size = len(map)

        # flood_score = find_flood_score(map)
        ##############################
        ##############################
        flood_score = []
        flooded = {}
        for y_in in range(len(map)):
            for x_in, v in enumerate(map[y_in]):
                if v != 1: continue
                if str(y_in)+str(x_in) in flooded: continue
                flooded[str(y_in)+str(x_in)] = 1
                total = 0
                queue = []
                queue.append((y_in,x_in))
                while(len(queue)>0):
                    y, x = queue.pop()
                    total+=1
                    flooded[str(y)+str(x)] = 1
                    if y + 1 < len(map):
                        if map[y+1][x] == 1:
                            if str(y+1)+str(x) not in flooded:
                                queue.append((y+1, x))
                    if y - 1 > -1:
                        if map[y-1][x] == 1:
                            if str(y-1)+str(x) not in flooded:
                                queue.append((y-1, x))
                    if x + 1 < len(map):
                        if map[y][x+1] == 1:
                            if str(y)+str(x+1) not in flooded:
                                queue.append((y, x+1))
                    if x - 1 > -1:
                        if map[y][x-1] == 1:
                            if str(y)+str(x-1) not in flooded:
                                queue.append((y, x-1))
                flood_score.append(total)
        flood_score = sum(flood_score) / len(flood_score)
        ##################################
        ##################################
        wc = 0.01
        lc = 0.01
        for y in range(len(map)):
            for x, v in enumerate(map[y]):
                if v == 0:
                    total = 0
                    radius = 3
                    for i in range(-radius, radius):
                        for j in range(-radius, radius):
                            new_y = y + i if y + i < max_size else 0 - i
                            new_x = x + j if x + j < max_size else 0 - j
                            total += 1 if map[new_y][new_x] == 0 else 0
                    land_score += total / (radius**2)
                    lc += 1
                elif v== 1:
                    total = 0
                    # print(map[y][x])  
                    radius = 5
                    for i in range(-radius, radius):
                        for j in range(-radius, radius):    
                            if -3 < j < 3 or -3 < i < 3: continue
                            new_y = y + i if y + i < max_size else 0 - i
                            new_x = x + j if x + j < max_size else 0 - j
                            total += 0 if map[new_y][new_x] == 1 else 3
                            water_score += total / radius**2
                    wc+=1
                elif v== 2:
                    total = 0
                    # print(map[y][x])  
                    radius = 1
                    for i in range(-radius, radius):
                        for j in range(-radius, radius):
                            new_y = y + i if y + i < max_size else 0 - i
                            new_x = x + j if x + j < max_size else 0 - j
                            total += 3 if map[new_y][new_x] == 2 else 1 if map[new_y][new_x] == 0 else -10
                    desert_score += total / (radius**2)
                    lc += 1

                


        # return (water_score + flood_score) / 2 + land_score / 2
        # return flood_score + water_score / max_size**2 + land_score / max_size**2
        # return ((land_score) + (desert_score))*(0.666 / (lc/(max_size**2))) + (water_score)*(0.333 / wc/(max_size**2))
        # return (max_size**2 - wc) + flood_score + water_score + land_score
        return (max_size**2 - wc)*5 + flood_score / land_score + water_score + desert_score*2

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
        self.ftn_track = []
        while(not self.stop_condition()):
            self.get_fitness()
            self.order_pop()
            print(f'Best of gen {self.curr_gen}:')
            print(f'fitness - {self.population[len(self.population)-1].fitness}')
            self.ftn_track.append(self.population[len(self.population)-1].fitness)
            # print(self.population[len(self.population)-1].map)
            # print()
            self.call_back(self.population[len(self.population)-1])
            self.cull_pop()
            self.repopulate()
            self.curr_gen += 1
        self.get_fitness()
        self.order_pop()
        return self.population[len(self.population)-1]

    def stop_condition(self):
        if self.curr_gen > self.gen_stop:
            return True
        if len(self.ftn_track) > 25:
            if abs(self.ftn_track[-10] - self.ftn_track[len(self.ftn_track)-1]) / abs((self.ftn_track[-10] + self.ftn_track[len(self.ftn_track)-1]) / 2) < 0.000000005:
                return True
        return False

# g = ga(m_size=25, mutation_rate=0.02)
# g.start()

# par1 = member(10)
# par2 = member(10)
# child = member.cross_over(par1, par2)
# print(child.map)

# m = member(10)
# print(flood_score(5,5, m.map, 1))
# print(m.map)