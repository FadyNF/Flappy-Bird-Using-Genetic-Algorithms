import numpy as np
from Classes.bird import Bird
import random

class BirdGA:
    def __init__(self, population_size=10, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.intialize_population()
        
    def intialize_population(self):
        population = []
        
        for _ in range(self.population_size):
            position_y = random.uniform(100, 300)
            jump_force = random.uniform(-12, -5)
            gravity = random.uniform(0.1, 0.5)
            bird = Bird(100, position_y, jump_force, gravity)
            population.append(bird)
            
        return population
    
    def calculate_fitness(self, bird):
        return bird.get_fitness()
    
    def selection(self):
        """Tournament selection method"""
        tournament_size = 5
        selected = []
        
        for _ in range(self.population_size):
            tournament = random.sample(self.population, tournament_size)
            winner = max(tournament, key=self.calculate_fitness)
            selected.append(winner)
            
        return selected
    
    def crossover(self, parent1, parent2):
        """Uniform crossover method"""
        # Create offspring with mixed attributes
        offspring1_y = parent1.y if random.random() < 0.5 else parent2.y
        offspring1_jump_force = parent1.jump_force if random.random() < 0.5 else parent2.jump_force
        offspring1_gravity = parent1.gravity if random.random() < 0.5 else parent2.gravity

        offspring2_y = parent2.y if random.random() < 0.5 else parent1.y
        offspring2_jump_force = parent2.jump_force if random.random() < 0.5 else parent1.jump_force
        offspring2_gravity = parent2.gravity if random.random() < 0.5 else parent1.gravity

        offspring1 = Bird(100, offspring1_y, offspring1_jump_force, offspring1_gravity)
        offspring2 = Bird(100, offspring2_y, offspring2_jump_force, offspring2_gravity)
        
        return offspring1, offspring2

    def mutation(self, individual):
        """Mutation with controlled rate"""
        if random.random() < self.mutation_rate:
            attribute_to_mutate = random.choice(['y', 'jump_force', 'gravity'])

            if attribute_to_mutate == 'y':
                individual.y += random.uniform(-10, 10)
            elif attribute_to_mutate == 'jump_force':
                individual.jump_force += random.uniform(-2, 2)
            elif attribute_to_mutate == 'gravity':
                individual.gravity += random.uniform(-0.2, 0.2)

            # Ensure values stay within reasonable bounds
            individual.y = max(0, min(individual.y, 300))
            individual.jump_force = max(-15, min(individual.jump_force, -1))
            individual.gravity = max(0.1, min(individual.gravity, 1))

    def evolve(self):
        """Evolve the population"""
        # Calculate fitness for current population
        for bird in self.population:
            bird.increment_fitness()

        # Selection
        selected = self.selection()
        
        # Create next generation
        next_generation = []
        while len(next_generation) < self.population_size:
            # Select parents
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            
            # Crossover
            offspring1, offspring2 = self.crossover(parent1, parent2)
            
            # Mutation
            self.mutation(offspring1)
            self.mutation(offspring2)

            next_generation.extend([offspring1, offspring2])
        
        # Trim to exact population size
        self.population = next_generation[:self.population_size]