"""
Author: Dion Reji
"""

import numpy as np
import matplotlib.pyplot as plt

# Define the DTMC
num_states = 13
states = list(range(num_states))
# print(states)

"""
Transition probability matrix for coin toss simulating dice
States from 7 to 12 represents the dice
"""

prob_matrix = np.array([
    [0, 0.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0.5, 0.5, 0, 0, 0, 0, 0, 0],
    [0, 0.5, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0],
    [0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
])


"""
Transition probability matrix for message protocol
"""

# prob_matrix = np.array([
#     [0, 1, 0, 0],
#     [0, 0, 0.1, 0.9],
#     [0, 1, 0, 0],
#     [1, 0, 0, 0]
# ])

def DFS(graph, start, visited):
        visited[start] = True
        for i in range(len(graph)):
            if (graph[start][i] > 0 and
                    (not visited[i])):
                # print(i)
                DFS(graph, i, visited)


def find_reachable_from_all(graph):

    n = len(graph)
    reachable_from_each = np.zeros((n,n))

    for start_node in range(n):
        visited = [False] * n
        DFS(graph, start_node,visited)
        for i in range(n):
          if visited[i]:
            reachable_from_each[start_node][i] = 1

    return reachable_from_each

def find_pre_states(G,num_states, prob_matrix):
  pre_states = []
  reachable = find_reachable_from_all(prob_matrix)
  # print(reachable[4][7])

  # reachable[i][j] is 1 iff you can reach j from i
  for i in range(num_states):
    if i in G:
      continue

    if any(reachable[i][state] for state in G):
            pre_states.append(i)

  return pre_states


###############################

G = set([7])
# print(find_pre_states(G,num_states, prob_matrix))

pre = find_pre_states(G,num_states, prob_matrix)
# print("Pre-set")
pre_len = len(pre)

A = np.zeros((pre_len,pre_len))
b = np.zeros((pre_len,1))

for i in range(pre_len):
  b[i] = sum(prob_matrix[pre[i]][j] for j in G)
  for j in range(pre_len):
    A[i][j] = prob_matrix[pre[i]][pre[j]]

print(b)
print(A)

x = np.zeros((pre_len,1))
y = np.matmul(A,x) + b

epsilon = 0.00001
vals = []
num_epochs = 100

# Power Method
# while np.max(np.abs(x-y)) > epsilon:
for _ in range(num_epochs):
  vals.append(x.copy())
  x = y
  y = np.matmul(A,x) + b


print(x)
print(vals)

# # Solving the system of equations
# I = np.eye(pre_len)
# z = np.linalg.solve(I-A,b)
# print(z)

# print(f"Probability of eventually reaching the states, G: {G}")
# for i in range(num_states):
#   if i in G:
#     print(f"x({i}) = 1")
#   if i in pre:
#     print(f"x({i}) = {x[pre.index(i)]}")
#   else:
#     print(f"x({i}) = 0")

# num_steps = len(vals)
# vals_array = np.array(vals).squeeze(axis=-1)

# plt.figure(figsize=(10, 6))
# colors = plt.cm.tab10(range(pre_len))
# for i in range(pre_len):
#     plt.plot(range(num_steps), vals_array[:, i], marker='o', linestyle='-', color=colors[i], label=f'x({pre[i]})')

# plt.xlabel('Iteration Step Number')
# plt.ylabel('Value')
# plt.title('Convergence of All Entries in x vs Iteration Steps')
# plt.legend()
# plt.grid(True)
# plt.show()