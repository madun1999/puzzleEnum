import numpy as np
# import csv

class kakurasu:
    def __init__(self, weight):
        '''
        self.weight 
        Either be a tuple of two list which represent the coloum weight and the row weight
        or a matrix which represet the weight of each box

        self.length 
        The length of the side

        self.set
        set of puzzles with solutions
        '''
        self.weight = weight
        self.length = len(weight[0])
        self.sol = set()
    
    def genPorblem(self):
        '''
        a generator generate solutions
        '''
        ROW_MAX = 2**self.length - 1
        def addOne():
            for i in range(self.length):
                if ret[i] == ROW_MAX:
                    ret[i] = 0
                else:
                    ret[i] += 1
                    return True
            return False
        ret = [0] * self.length
        while True:
            if addOne():
                yield [[int(ch) for ch in '{0:0{width}b}'.format(row, width=self.length)] for row in ret]
            else:
                break
    
    def sol2prob(self, sol):
        temp = np.multiply(sol, self.weight)
        return (np.sum(temp, axis=0), np.sum(temp, axis=1))

if __name__ == '__main__':
    weight = [[1,1,2,2],[1,1,2,2],[2,2,1,1],[2,2,1,1]]
    test = kakurasu(weight)
    gen = test.genPorblem()
    with open("data.csv", "ab") as f:
        while True:
            f.write(b"\n")
            data = test.sol2prob(next(gen))
            np.savetxt(f, data, fmt='%i', delimiter=',')