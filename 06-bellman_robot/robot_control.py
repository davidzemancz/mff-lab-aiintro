import numpy, scipy, networkx # You can use everything from these libraries if you find them usefull.
import scipy.sparse as sparse # Calling scipy.sparse.csc_matrix does not work on Recodex, so call sparse.csc_matrix(...) instead
import scipy.sparse.linalg as linalg # Also, call linalg.spsolve

"""
    TODO: Improve the strategy controlling the robot.
    A recommended approach is implementing the function RobotControl.precompute_probability_policy.
    You can adopt this file as you like but you have to keep the interface so that your player properly works on recodex; i.e.
        * RobotControl.__init__ is called in for every environment (test).
        * RobotControl.get_command is called to obtain command for movement on a given position.
    Furthermore, get_survivability and get_policy is used by tests in the file probability_test.py.
"""

class RobotControl:
    def __init__(self, environment):
        self.env = environment
        self.survivability,self.policy = self.precompute_probability_policy()

    # Returns a matrix of maximal probabilities of reaching the station from every cell
    def get_survivability(self):
        return self.survivability

    # Returns a matrix of commands for every cell
    def get_policy(self):
        return self.policy

    # Returns command for movement from the current position.
    # This function is called quite a lot of times, so it is recommended to avoid any heavy computation here.
    def get_command(self, current):
        return self.policy[tuple(current)]

    # Place all your precomputation here.
    def precompute_probability_policy(self):
        # ----- attrs -----
        # env.destination - Position of the station
        # env.safety_map - The matrix of probalities that our robot successfully enter each cell
        # env.rotation_probability - Distribution of actual movement relative to the given command.
        # ----- methods -----
        # env.get_safety(position) - Probability of successfully entrance to a given cell.
        # env.get_danger(position) - Probability of lossing the robot when entering a given cell.

        return self.precompute_probability_policy_value_update()
        #return self.precompute_probability_policy_trivial()

    # Returns a trivial control strategy which just heads directly toward the station ignoring all dangers and movement imperfectness
    def precompute_probability_policy_trivial(self):
        env = self.env
        survivability = numpy.zeros((env.rows, env.columns)) # No probability is computed
        policy = numpy.zeros((env.rows, env.columns), dtype=int)
        for i in range(env.rows):
            for j in range(env.columns):
                if i > env.destination[0]:
                    policy[i,j] = env.NORTH
                elif i < env.destination[0]:
                    policy[i,j] = env.SOUTH
                elif j < env.destination[1]:
                    policy[i,j] = env.EAST
                elif j > env.destination[1]:
                    policy[i,j] = env.WEST
        return survivability, policy

    def precompute_probability_policy_value_update(self):
        env = self.env
                
        # Implementation using value update
        # Bellman's equation U(s) = R(s) + \gamma * max_a \sum_r P(r|s,a) U(r)
        # Where     
        #   R(s) = env.safety_map[s]
        #   P(r|s,a) = P(r|a) = P(a|r)P(r)/P(a)
        #   Where
        #       P(r) = 1/|states|
        #       P(a) = 1/4
        #       P(a|r) = env.rotation_probability[direction]

        # Value-iteration algorithm
        utility = None
        #utility_updated = numpy.random.rand(env.rows, env.columns)
        #utility_updated[0,...], utility_updated[...,0], utility_updated[-1,...], utility_updated[...,-1] = 0, 0, 0, 0
        utility_updated = numpy.zeros((env.rows, env.columns))
        gamma, delta, epsilon = 0.5, 0, 0.01
        map_size = (1 / ((env.rows - 2) * (env.columns - 2)))
        
        while delta < epsilon * (1 - gamma) / gamma:
            utility = utility_updated.copy()
            delta = 0
            for i in range(1, env.rows - 1):
                for j in range(1, env.columns - 1):
                    # Get utils of actions
                    actions_utils = numpy.zeros(4)
                    for action in [env.FORWARD, env.RIGHT, env.BACKWARD, env.LEFT]:
                        action_util = 0
                        for n_i, n_j in self.get_map_neighbors((i, j)):
                            action_util += (((env.rotation_probability[action]*map_size)/0.25) * utility[n_i, n_j])
                        actions_utils[action] = action_util

                    # Get max utility
                    actions_utils_max = numpy.amax(actions_utils)
                    
                    # Update
                    utility_updated[i, j] = self.get_reward((i, j)) + gamma * actions_utils_max
                    if utility_updated[i, j] - utility[i, j] > delta:
                        delta = utility_updated[i, j] - utility[i, j]

        survivability = utility_updated
        
        # Create policy
        policy = numpy.zeros((env.rows, env.columns), dtype=int)
        for i in range(1, env.rows - 1):
            for j in range(1, env.columns - 1):
                # Get neighbour with max utility
                n_utils = numpy.zeros(4)
                for (n, (n_i, n_j)) in enumerate(self.get_map_neighbors((i, j))):
                    n_utils[n] = survivability[n_i, n_j]
                n_max = numpy.argmax(n_utils)

                # Set policy
                if n_max == 0:
                    policy[i,j] = env.SOUTH
                elif n_max == 1:
                    policy[i,j] = env.NORTH
                elif n_max == 2:
                    policy[i,j] = env.EAST
                elif n_max == 3:
                    policy[i,j] = env.WEST
        
        return survivability, policy

    def get_reward(self, position):
        rel_dist_x = abs(position[0] - self.env.destination[0]) / self.env.safety_map.shape[0]
        rel_dist_y = abs(position[1] - self.env.destination[1]) / self.env.safety_map.shape[1]
        return 1 * (self.env.get_safety(position) - ((rel_dist_x + rel_dist_y)))

    def get_map_neighbors(self, position):
        neighbors = []
        if position[0] + 1 < self.env.rows: neighbors.append((position[0] + 1, position[1])) # SOUTH
        if position[0] - 1 >= 0: neighbors.append((position[0] - 1, position[1])) # NORTH
        if position[1] + 1 < self.env.columns: neighbors.append((position[0], position[1] + 1)) # EAST
        if position[1] - 1 >= 0: neighbors.append((position[0], position[1] - 1)) # WEST
        return numpy.array(neighbors)
        
