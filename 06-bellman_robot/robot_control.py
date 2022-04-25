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
                
        # Init
        policy = numpy.zeros((env.rows, env.columns), dtype=int)
        utility = numpy.zeros((env.rows, env.columns))
        utility[tuple(env.destination)] = 1.0

        # Params
        utility_diff_max, utility_err_max, iter_max, iter, any_policy_changed = 1, 0.05, 200, 0, True

        # Value iteration algorithm
        while utility_diff_max > utility_err_max and iter <= iter_max and any_policy_changed:
            utility_diff_max = 0 # Maximum differance between old and new utility
            iter += 1 # Number of iterations
            any_policy_changed = False # Does any policy changed
            
            # For all cells except borders
            for i in range(1, env.rows - 1):
                for j in range(1, env.columns - 1):
                    # Ignore destination
                    if i == env.destination[0] and j == env.destination[1]: continue
                    
                    # Get best action - compute utility for all actions and neighbors
                    actions_utils = numpy.zeros(4)
                    for action in [env.NORTH, env.EAST, env.SOUTH, env.WEST]:  # for actions
                        action_util = 0
                        for (n_dir, (n_i, n_j)) in [(env.NORTH, (i - 1, j)), (env.EAST, (i, j + 1)), (env.SOUTH, (i + 1, j)), (env.WEST, (i, j - 1))]:  # for neighbors
                            n_prob = env.rotation_probability[(n_dir - action) % 4]
                            action_util += n_prob * utility[n_i, n_j] * env.safety_map[n_i, n_j]
                        actions_utils[action] = action_util

                    best_action = numpy.argmax(actions_utils) # Best action
                    best_action_util = actions_utils[best_action] # Best actions utility
                    
                    # Compute utility difference
                    utility_diff = abs(best_action_util - utility[i, j])
                    if utility_diff > utility_diff_max: utility_diff_max = utility_diff

                    # Update utility
                    utility[i, j] = best_action_util

                    # Does policy changed
                    any_policy_changed = any_policy_changed or policy[i, j] != best_action

                    # Update policy
                    policy[i, j] = best_action
        
        return utility, policy
