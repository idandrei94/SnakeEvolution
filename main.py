from board import Board
import n_net


def processBoard(board):
  while board.frame(display = True):
    None
  return board.score

#os.system('clear')
tests = 1
results = [None] * tests
brain = n_net.neuralNetwork.load('brain')
for i in range(tests):
   board = Board(10, 10, train = False, brain = brain)
   results[i] = processBoard(board)
   print('Calculation', int((1+i)*100/tests), '% complete')
   print("  Result:", results[i])
   brain = board.brain

brain.save('brain')

results = sorted(results)
print('Average score:', sum(results)/tests)
print()
results = list(reversed(results))
for i in range(len(results) if len(results) < 15 else 15):
  print('#', i, ': ', results[i])