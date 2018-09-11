import itertools
import argparse
import random
random.seed()
parser = argparse.ArgumentParser(description='Generate a random knapsack problem with some given spearman correlation between the value and weights')
parser.add_argument('NumItems', type=int, help='The number of items')
parser.add_argument('SpearmanCorr', type=float, help='The spearman correlation')
parser.add_argument('--verbose', action='store_true', default=False)
args = parser.parse_args()
def ordering_spearman(ranks):
    d_squared = sum([(ranks[i] - i)**2 for i in range(0, len(ranks))])
    n = len(ranks)
    return 1 - 6*(d_squared/(1.0*n*(n**2 - 1)))


class Ordering:
    #items are ordered by attribute X, and the ranks of the resulting list are stored in ranks. Ranks are indexed from 0.
    def __init__(self, ranks, target_rho, verbose):
        self.ranks = ranks
        self.target_rho = target_rho
        self.verbose = verbose
        self.objective = lambda ranks: (target_rho - ordering_spearman(ranks))**2
    def swap_ranks(self, index_one, index_two):
        x = self.ranks[index_one]
        self.ranks[index_one] = self.ranks[index_two]
        self.ranks[index_two] = x
    def find_best_swap(self):
        original_objective = self.objective(self.ranks)
        best_objective = original_objective
        best_swap = False
        
        for i, j in itertools.combinations(range(0, len(self.ranks)), 2):
            new_objective = self.objective(self.ranks[0:i] + [self.ranks[j]] + self.ranks[(1 + i):j] + [self.ranks[i]] + self.ranks[(j + 1)::])
            if new_objective < best_objective:
                best_objective = new_objective
                best_swap = (i, j)        
        return best_swap
    def optimize(self):
        keep_going = True
        while keep_going:
            best_swap =  self.find_best_swap()
            if best_swap:
                if self.verbose:
                    print('Current order: ' + str(self.ranks))
                    print('old spearman: ' + str(self.compute_spearman()))
                self.swap_ranks(best_swap[0], best_swap[1])
                if self.verbose:
                    print('swapping: ' + str(best_swap))
                    print('new order: ' + str(self.ranks))
                    print('new spearman: ' + str(self.compute_spearman()))
            else:
                keep_going = False
    def compute_spearman(self):
        return ordering_spearman(self.ranks)


    
def create_knapsack_problem(num_items, target_rho, verbose):
    initial = list(range(0, num_items))
    random.shuffle(initial)
    ordering = Ordering(initial, target_rho, verbose)
    ordering.optimize()
    ranks = ordering.ranks
    value = random.randint(1, 10)
    random_value_increase = lambda: random.randint(1, 5)
    weight = random.randint(15, 30)
    random_weight_increase = lambda: random.randint(3,10)
    values = [value]
    weights = [weight]
    for i in range(0, num_items):
        value += random_value_increase()
        values.append(value)
        weight += random_weight_increase()
        weights.append(weight)
    ks = []
    j = 0
    for i in ranks:
        ks.append((values[j], weights[i]))
        j += 1
    return ks

results = create_knapsack_problem(args.NumItems, args.SpearmanCorr, args.verbose)
for value, weight in results:
    print('\t' + str(value) + '\t' + str(weight))


