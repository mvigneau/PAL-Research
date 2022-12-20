### Mathieu Vigneault
### 03-23-2020
### Here is my genetic algorithm it eventually finds the answer
### but it is a bit too long at my taste, might be due to selection
### process not strict enough ... will fix it soon

from random import *
from Learning_Data import *
from graphics import *
import statistics 
from time import sleep
import matplotlib.pyplot as plt


## Initialize population & Fitness Score ##
def init_population(population_size, chromosome_size):
	population_list = []
	for i in range(population_size):
		chromosome = []
		for j in range(chromosome_size):

			number = int(round(random(),0))
			chromosome.append(number)

		population_list.append(chromosome) 
	
	return population_list

def findFitness(movement, repetition, current_position, current_answer, count):

	actual_t = current_position[1][0]
	expected_t = current_answer[1][0]

	T_Range = 7 * count
	T_Diff = round(abs(actual_t - expected_t),2)
	if(T_Diff == 0):
		T_Score = 0
	else:
		T_Score = (T_Diff / T_Range) * 100

	actual_f = current_position[1][1]
	expected_f = current_answer[1][1]
	F_Range = 10 * count
	F_Diff = round(abs(actual_f - expected_f),2)
	#print(actual_f, expected_f)

	if(F_Diff == 0):
		F_Score = 0
	else:
		F_Score = (F_Diff / F_Range) * 100
	
	#print(F_Score)

	actual_h = current_position[1][2]
	expected_h = current_answer[1][2]
	H_Range = 30 * count
	if (actual_h < 0):
		actual_h = 360 - abs(actual_h%360)
	
	if(abs(expected_h - actual_h) > 180):
		H_diff = 360 - abs(expected_h - actual_h)
	else:
		H_diff = abs(expected_h - actual_h)
	
	H_diff = H_diff * 100 / 360

	if(H_diff == 0):
		H_Score = 0
	else:
		H_Score = (H_diff / H_Range) * 100

	# print(current_position, current_answer)
	#print(T_Score, F_Score, H_Score)
	#average_score = sum()
	tot_score = round((T_Score + F_Score + H_Score),2)
	return tot_score

def hillClimbing(movement, repetition, setValues, j):

	count2 = 1
	current_position = [0, [0, 0, 0]]
	current_answer = [0, [0, 0, 0]]
	badGene = []

	if(j == 2 or j == 5 or j == 8 or j == 11):
		if(repetition == 0):
			add = [0, 0, 90]
		else:
			add = [0, 0, (90)]
	else:
		if(repetition == 0):
			add = [0, 30.48, 0]
		else:
			add = [0, (30.48), 0]

	#print(setValues, repetition)

	add[0] = add[0] / 16
	add[1] = add[1] / 16
	add[2] = add[2] / 16

	for rep in range(repetition):
		current_position[1][0] += setValues[0]
		current_position[1][1] += setValues[1]
		current_position[1][2] += setValues[2]
		current_position[1][0] = round(current_position[1][0],2)
		current_position[1][1] = round(current_position[1][1],2)
		current_position[1][2] = round(current_position[1][2],2)
		current_answer[1][0] = current_answer[1][0] + add[0] 
		current_answer[1][1] = current_answer[1][1] + add[1] 
		current_answer[1][2] = current_answer[1][2] + add[2] 

	current_position[1][0] = current_position[1][0] / 16
	current_position[1][1] = current_position[1][1] / 16
	current_position[1][2] = current_position[1][2] / 16

	score = findFitness(current_position, current_answer, current_position, current_answer, count2)
	if(score >= 225):
		array = [setValues[0], setValues[1], setValues[2]]
		badGene.append(array)

	count2 += 1
	
	return badGene

def reorganize(i,j, population_list, movement, repetition, setValues):

	if(repetition == 0):
		index1 = population_list[i].index(population_list[i][j])
		index2 = population_list[i].index(population_list[i][j+1])

		population_list[i].pop(index2)
		population_list[i].pop(index1)
		j += 1

	return population_list, j

def fitness(population_list, inputData, answer, chromosome_size, population_size):

	fitness_list = []
	for i in range(population_size):
		fitness_score = 0
		current_position = [0, [0, 0, 0]]
		current_answer = [0, [0, 0, 0]]
		count = 1
		for j in range(chromosome_size//8):

			movement = population_list[i][j]
			repetition = population_list[i][j+1]
			setValues = inputData[movement][1]
			#print(movement, repetition, setValues)
			
			##################### Hill Climbing Function -- Gets rid of unwanted genes ################################
			if(i % 2 == 0):
				bad = hillClimbing(movement, repetition, setValues, j)
				for k in range(len(bad)):
					if(setValues[0] == bad[k][0] and setValues[1] == bad[k][1] and setValues[2] == bad[k][2]):
						move = randrange(0,16)
						rep = randrange(16)
						setValues[0] = inputData[move][1][0]
						setValues[1] = inputData[move][1][1]
						setValues[2] = inputData[move][1][2]
			
			############################################################################################################
			
			############## Reorganize // Clean up Chromosome -- Gets rid of genes with 0 repetition ####################
			# if(i % 10 == 0):
			# 	population_list, j = reorganize(i, j, population_list, movement, repetition, setValues)

			############################################################################################################

			if(j == 2 or j == 5 or j == 8 or j == 11):
				if(repetition == 0):
					add = [0, 0, 90]
				else:
					add = [0, 0, (90)]
			else:
				if(repetition == 0):
					add = [0, 30.48, 0]
				else:
					add = [0, (30.48), 0]

			#print(setValues, repetition)

			add[0] = add[0] / 16
			add[1] = add[1] / 16
			add[2] = add[2] / 16

			for rep in range(repetition):
				current_position[1][0] += setValues[0]
				current_position[1][1] += setValues[1]
				current_position[1][2] += setValues[2]
				current_position[1][0] = round(current_position[1][0],2)
				current_position[1][1] = round(current_position[1][1],2)
				current_position[1][2] = round(current_position[1][2],2)
				current_answer[1][0] = current_answer[1][0] + add[0] 
				current_answer[1][1] = current_answer[1][1] + add[1] 
				current_answer[1][2] = current_answer[1][2] + add[2] 

			current_position[1][0] = current_position[1][0] / 16
			current_position[1][1] = current_position[1][1] / 16
			current_position[1][2] = current_position[1][2] / 16

			#print(current_position, current_answer)
			score = findFitness(current_position, current_answer, current_position, current_answer, count)
			fitness_score += score

			count += 1
			#print(fitness_score)

		fitness_list.append(fitness_score)
		#print(fitness_score)
	#print(fitness_list)

	return fitness_list

## Define another fitness funcion since the first one is too strict.
#def fitness2( ):

## Selection Process based on the fitness of the individuals ##
## Higher fitness has a higher chance of reproducing to the next generation ##  
def select(population, fitness_list):
	
	## Calculate Sum of Total Fitness of Entire Population ##
	total = 0 
	for i in range(len(fitness_list)):
		total += fitness_list[i]

	#print(total)

	# new_fitness = []
	# for i in range(len(fitness_list)):
	# 	new_fit = total - float(fitness_list[i])
	# 	new_fitness.append(new_fit)

	# total2 = 0
	# for i in range(len(fitness_list)):
	# 	total2 += new_fitness[i]
	# print(total2)

	## Calculate Probability to Select Each Individual ##
	probability_list = []
	for j in range(len(fitness_list)):
		prob = ((-1*(float(fitness_list[j])) / total) / len(population))
		probability_list.append(prob)
	#print(probability_list)
	#print(sum(probability_list))

	## Repeat these step until you fill up entire new population ##
	new_population = []
	for popsize in range(len(population)):
		## Select A Chromosome ##
		selection = choices(population, probability_list)
	
		## Add Selected Chromosome to New Population ##
		new_population.append(selection[0])

	return new_population

## Selection Process based on the fitness of the individuals ##
## Higher fitness has a higher chance of reproducing to the next generation ##  
def select2(population, fitness_list):
	
	fitness_list2 = []
	for i in range(len(fitness_list)):
		fitness_list2.append(fitness_list[i])

	fitness_list2.sort()
	#print(fitness_list)
	#print(fitness_list2)
	prob_list = []
	for i in range(len(fitness_list2)):
		prob_list.append(len(fitness_list2) - (i))
	#print(prob_list)

	## Calculate Sum of Total Fitness of Entire Population ##
	total = 0 
	for i in range(len(fitness_list2)):
		total += prob_list[i]

	#print(total)

	## Calculate Probability to Select Each Individual ##
	probability_list = []
	for j in range(len(fitness_list)):
		value = fitness_list2.index(fitness_list[j])
		prob = prob_list[value] / total
		probability_list.append(prob)
	#print(probability_list)
	#print(sum(probability_list))

	## Repeat these step until you fill up entire new population ##
	new_population = []
	for popsize in range(len(population)):
		## Select A Chromosome ##
		selection = choices(population, probability_list)
	
		## Add Selected Chromosome to New Population ##
		new_population.append(selection[0])

	return new_population



def crossover(new_population, chromosome_size, population_size, crossover_prob):
	#print(new_population)
	storage = []
	for half in range((len(new_population)//2)):
		random_number = randint(1, 100)
		if random_number <= (crossover_prob * 100):
			parent1 = randrange(0, len(new_population))
			parent2 = randrange(0, len(new_population))
			while(parent1 == parent2):
				parent2 = randrange(0, len(new_population))
			chrom = randrange(0,2)
			spot = randrange(0,chromosome_size)
			#print(chrom, spot, parent1, parent2)

			if chrom == 0:
				chromosome1_part1 = new_population[parent1][:spot]
				chromosome1_part2 = new_population[parent2][spot:]
				chromosome2_part1 = new_population[parent2][:spot]
				chromosome2_part2 = new_population[parent1][spot:]
			else:
				chromosome1_part1 = new_population[parent2][:spot]
				chromosome1_part2 = new_population[parent1][spot:]
				chromosome2_part1 = new_population[parent1][:spot]
				chromosome2_part2 = new_population[parent2][spot:]

			chromosome1 = chromosome1_part1 + chromosome1_part2
			chromosome2 = chromosome2_part1 + chromosome2_part2
			
			if(parent1 < parent2):
				new_population.pop(parent1)
				new_population.pop(parent2-1)
			else:
				new_population.pop(parent2)
				new_population.pop(parent1-1)

			storage.append(chromosome1)
			storage.append(chromosome2)

	for num in range(len(storage)):
		#print(storage[num])
		new_population.append(storage[num])

	return new_population

def mutate(new_population, chromosome_size, mutation_prob):
	
	for i in range(len(new_population)):
		for j in range(chromosome_size):
			random_number = randint(1, 100)
			if random_number <= (mutation_prob * 100):
				#print(i,j)
				#print(new_population[i][0][j])
				if new_population[i][j] == 0:
					new_population[i][j] = 1
				else:
					new_population[i][j] = 0
				#print(new_population[i][0][j])
	#print(new_population)
	return new_population 

def transform(gene, jump):
	value = 0
	gene.reverse()
	for i in range(len(gene)):
		if (gene[i] == 1):
			value += (jump * (2**(i)))
	return value



def main():

	## Importation of Data from Robot Possible Movements ##
	inputData = [[0, [4.20, 0.18, 29.90]], 
	[1, [5.22, 2.57, 21.17]], 
	[2, [5.19, 2.96, 11.68]], 
	[3, [6.18, 3.05, 6.15]],
	[4, [5.58, 5.13, 3.79]],
	[5, [4.36, 7.20, 2.86]], 
	[6, [3.18, 8.10, 1.94]],
	[7, [0.78, 9.37, 1.18]],
	[8, [0.78, 9.37, 1.18]], 
	[9, [-1.68, 7.69, -1.23]],
	[10, [-2.75, 7.31, -1.71]],
	[11, [-4.52, 5.78, -3.42]], 
	[12, [-4.66, 4.81, -6.26]], 
	[13, [-4.90, 3.64, -10.48]], 
	[14, [-5.05, 2.25, -22.47]],
	[15, [-4.83, 0.04, -29.71]]]

	## Answer ##
	#answer()
	answer = [[0, [0.00, 0.00, 0.00]],
	[1, [0.00, 30.48, 0.00]], 
	[2, [0.00, 60.96, 0.00]], 
	[3, [0.00, 60.96, 90.00]], 
	[4, [0.00, 91.44, 90.00]],
	[5, [0.00, 121.92, 90.00]],
	[6, [0.00, 121.92, 180.00]], 
	[7, [0.00, 152.20, 180.00]],
	[8, [0.00, 182.88, 180.00]],
	[9, [0.00, 182.88, 270.00]], 
	[10, [0.00, 213.36, 270.00]],
	[11, [0.00, 243.84, 270.00]],
	[12, [0.00, 243.84, 0.00]]]

	## Basic Settings For GA Learning ##
	population_size = 100
	crossover_prob = 0.7
	mutation_prob = 0.01
	chromosome_size = 96
	generation = 200
	first_time = True

	## Graph Parameters ##
	middle = Point(400,400)
	multiplier = 4
	start = Point(0,0)
	answer_start = Point(0,0)


	### Initiate a population ###
	population = init_population(population_size, chromosome_size)
	
	for gen in range(generation):
		gene_list = []
		#print("pop", population)
		for pop in range(population_size):
			current_chromosome = population[pop]
			#print(current_chromosome)
			gene = []
			for move in range(chromosome_size//8):
				M_start = move * 8 
				M_end = move * 8 + 4
				Movement = current_chromosome[M_start:M_end]
				Repetition = current_chromosome[M_end:(M_end+4)]
				Movement_Value = transform(Movement, 1)
				Repetition_Value = transform(Repetition, 1)
				gene.append(Movement_Value)
				gene.append(Repetition_Value)

			gene_list.append(gene)

		#print(gene_list)

		fitness_list = fitness(gene_list, inputData, answer, chromosome_size, population_size)

		print("Generation:", gen)
		print("Agent Fitness:")
		print(fitness_list)
		print("Average Fitness:", statistics.mean(fitness_list))
		print("Best Fitness:", min(fitness_list))

		## Finding the optimal chromosome to output it in data file ##
		string_maxChromosome = ""
		for chrom_max in range(chromosome_size):
			string_maxChromosome = string_maxChromosome + str(population[fitness_list.index(min(fitness_list))][chrom_max])

		## Formatting entire population in a big string to register it in excel file ##
		string_population = ""
		for pop in range(population_size):
			for pop_chrom in range(chromosome_size):
				string_population = string_population + str(population[pop][pop_chrom])
				if(pop != (population_size-1)):
					string_population = string_population + ","

		## Formatting entire population's fitness in a big string to register it in excel file##
		string_fitness = ""
		for fit in range(len(fitness_list)):
			string_fitness = string_fitness + str(fitness_list[fit])
			if(fit != (len(fitness_list)-1)):
				string_fitness = string_fitness + ","

		## Output Data into Excel File ##
		titles = ["Generation", "Average Fitness", "Best Fitness","Population Size", "Chromosome Size", "Crossover Probability", "Mutation Probability", "Best Chromosome", "Entire Population Chromosome", "Entire Population Fitness"]
		data = [gen, statistics.mean(fitness_list), min(fitness_list), population_size, chromosome_size, crossover_prob, mutation_prob, string_maxChromosome, string_population, string_fitness]
		first_time = Save_Data("Training_Data.xls", 0, titles, data, first_time)
		
		## Select Next Generation -- Apply Crossover & Mutation ##
		new_population = select2(population, fitness_list)
		#print("new", new_population)
		new_population = crossover(new_population, chromosome_size, population_size, crossover_prob)
		#print("crossover", new_population)
		new_population = mutate(new_population, chromosome_size, mutation_prob)
		#print("mutate", new_population)
		population = new_population
		#print("population", population)


		# if(pop == (population_size-1) and (gen % 10) == 0):
		### Upload Graphic window ###
		win = GraphWin("PAL Research", 800, 800)

		best = fitness_list.index(min(fitness_list))
		current_position = [0, [0, 0, 0]]
		current_answer = [0, [0,0,0]]
		first_loop = True
		start = Point(400+(30.48*4),400+(30.48*4))
		answer_start = Point(400+(30.48*4),400+(30.48*4))
		answer_line_list = []
		line_list = []

		for j in range(chromosome_size//8):

			movement = gene_list[best][j]
			repetition = gene_list[best][j+1]
			setValues = inputData[movement][1]
			#print(movement, repetition, setValues)

			if(j == 2 or j == 5 or j == 8 or j == 11):
				if(repetition == 0):
					add = [0, 0, 90]
				else:
					add = [0, 0, (90)]
			else:
				if(repetition == 0):
					add = [0, 30.48, 0]
				else:
					add = [0, (30.48), 0]

			#print(setValues, repetition)

			add[0] = add[0] / 16
			add[1] = add[1] / 16
			add[2] = add[2] / 16

			for rep in range(repetition):
				current_position[1][0] += setValues[0]
				current_position[1][1] += setValues[1]
				current_position[1][2] += setValues[2]
				current_position[1][0] = round(current_position[1][0],2)
				current_position[1][1] = round(current_position[1][1],2)
				current_position[1][2] = round(current_position[1][2],2)
				current_answer[1][0] = current_answer[1][0] + add[0] 
				current_answer[1][1] = current_answer[1][1] + add[1] 
				current_answer[1][2] = current_answer[1][2] + add[2] 

			current_position[1][0] = current_position[1][0] / 16
			current_position[1][1] = current_position[1][1] / 16
			current_position[1][2] = current_position[1][2] / 16
			
			for m in range(16):

				if(j < 2):
					answer_start = answer_start
					answer_end = Point(answer_start.getX() + add[0]*4, answer_start.getY() - add[1]*4)
					start = start
					end = Point(start.getX() + (current_position[1][0]*4), start.getY() - (current_position[1][1]*4))

				if(j >= 2 and j < 5):
					answer_start = answer_start
					answer_end = Point(answer_start.getX() - add[1]*4, answer_start.getY() - add[0]*4)
					start = start
					end = Point(start.getX() - (current_position[1][1]*4), start.getY() - (current_position[1][0]*4))

				if(j >= 5 and j < 8):
					answer_start = answer_start
					answer_end = Point(answer_start.getX() + add[0]*4, answer_start.getY() + add[1]*4)
					start = start
					end = Point(start.getX() + (current_position[1][0]*4), start.getY() + (current_position[1][1]*4))

				if(j >= 8 and j <= 12):
					answer_start = answer_start
					answer_end = Point(answer_start.getX() + add[1]*4, answer_start.getY() - add[0]*4)
					start = start
					end = Point(start.getX() + (current_position[1][1]*4), start.getY() - (current_position[1][0]*4))

				line = Line(start, end)
				line.setFill("red")
				line.setWidth(10)
				line_list.append(line)

				answer_line = Line(answer_start, answer_end)
				answer_line.setWidth(10)
				answer_line_list.append(answer_line)

				start = end
				answer_start = answer_end

			for n in range(len(answer_line_list)):
				answer_line_list[n].draw(win)
			
			for o in range(len(line_list)):
				line_list[o].draw(win)
				sleep(0.1)

			sleep(1)
			win.close()


main()
