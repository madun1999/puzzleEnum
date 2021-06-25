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

if __name__ == '__main__':
    test = kakurasu([[0]*4 for _ in range(4)])
    gen = test.genPorblem()
    for i in range(10):
        print(next(gen))

