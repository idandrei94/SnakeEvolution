import numpy
from scipy.special import expit
import random



class neuralNetwork:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        self.lr = learningrate

        # create the weight matrices
        self.wih = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        self.activation_function = expit
        pass
    
    def train(self, inputs_list, targets_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T

        # hidden layer signals
        hidden_inputs = numpy.dot(self.wih, inputs)
        # signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # signals into the output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # signals emerging from the output layer
        final_outputs = self.activation_function(final_inputs)
        
        # calculating the error
        output_errors = targets - final_outputs
        hidden_errors = numpy.dot(self.who.T, output_errors)
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 -final_outputs)), numpy.transpose(hidden_outputs))
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), numpy.transpose(inputs))
        pass
    
    def query(self, inputs_list):
        inputs = numpy.array(inputs_list, ndmin=2).T
        hidden_inputs = numpy.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = numpy.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        return final_outputs

    def mate(self, other, mutation = 0.01):
        newborn = neuralNetwork(self.inodes, self.hnodes, self.onodes, self.lr)
        for i in range(self.hnodes):
            for j in range(self.inodes):
                dice = random.randint(0, 2)
                if dice == 2:
                    newborn.wih[i][j] = (self.wih[i][j] + other.wih[i][j]) / 1
                else:
                    newborn.wih[i][j] = self.wih[i][j] if dice == 0 else other.wih[i][j]
                dice = random.randint(0,100)
                if dice <= mutation * 100: # we have a mutation
                    newborn.wih[i][j] *= 1.5
                dice = random.randint(0,1) # do we also have an invert mutation?
                newborn.wih[i][j] = newborn.wih[i][j] if dice == 0 else -newborn.wih[i][j]

        for i in range(self.onodes):
            for j in range(self.hnodes):
                dice = random.randint(0, 2)
                if dice == 2:
                    newborn.who[i][j] = (self.who[i][j] + other.who[i][j]) / 2
                else:
                    newborn.who[i][j] = self.who[i][j] if dice == 0 else other.who[i][j]
                dice = random.randint(0,100)
                if dice <= mutation * 100: # we have a mutation
                    newborn.who[i][j] *= 1.5
                dice = random.randint(0,1) # do we also have an invert mutation?
                newborn.who[i][j] = newborn.who[i][j] if dice == 0 else -newborn.who[i][j]
                
        return newborn

    def save(self, filename):
        with open(filename,'w') as file:
          print(str(self.inodes), file=file)
          print(str(self.hnodes), file=file)
          print(str(self.onodes), file=file)
          print(str(self.lr), file=file)
          for i in range(self.hnodes):
              for j in range(self.inodes):
                print(str(self.wih[i][j]), file=file)
          for i in range(self.onodes):
              for j in range(self.hnodes):
                print(str(self.who[i][j]), file=file)
        file.close()
    
    def load(filename):
        with open(filename,'r') as file:
            brain = neuralNetwork(100, 200, 3, 1)
            brain.inodes = int(file.readline().strip())
            brain.hnodes = int(file.readline().strip())
            brain.onodes = int(file.readline().strip())
            brain.lr = float(file.readline().strip())
            for i in range(brain.hnodes):
              for j in range(brain.inodes):
                brain.wih[i][j] = float(file.readline().strip())
            for i in range(brain.onodes):
              for j in range(brain.hnodes):
                brain.who[i][j] = float(file.readline().strip())
        return brain