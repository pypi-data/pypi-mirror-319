MAPPING_NUMBER_LETTER_TO_INT = {
    '0':  0, '1':  1, '2':  2, '3':  3, '4':  4, '5':  5, 
    '6':  6, '7':  7, '8':  8, '9':  9, 'a': 10, 'b': 11, 
    'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 
    'i': 18, 'j': 19, 'k': 20, 'l': 21, 'm': 22, 'n': 23, 
    'o': 24, 'p': 25, 'q': 26, 'r': 27, 's': 28, 't': 29, 
    'u': 30, 'v': 31, 'w': 32, 'x': 33, 'y': 34, 'z': 35, 
}


class IndexUsingNumber:
    def __init__(self, start='0', step=1, max_index=int(1E10)):
        self.index_iterable = range(max_index+1)
        
        self.index = self.index_iterable.index(int(start))
        self.step = step
    
    def get_index(self):
        return str(self.index_iterable[self.index])
    
    def go_next(self):
        self.index += self.step
        
        if (self.index<0) or (self.index>len(self.index_iterable)-1):
            self.index = len(self.index_iterable) - 1
            
            raise IndexError(
                'utils.IndexUsingNumberLetter.go_next: (self.index<0) or (self.index>len(self.index_iterable)-1), go to self.index == -1'
            )
    
    def go_previous(self):
        self.index -= self.step
        
        if (self.index<0) or (self.index>len(self.index_iterable)-1):
            self.index = 0
            
            raise IndexError(
                'utils.IndexUsingNumberLetter.go_previous: (self.index<0) or (self.index>len(self.index_iterable)-1), go to self.index == 0'
            )


class IndexUsingNumberLetter:
    def __init__(self, start='0', step=1):
        self.index_iterable = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.index_iterable += ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
        self.index_iterable += ['n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        
        self.index = self.index_iterable.index(start)
        self.step = step
        
    def get_index(self):
        return str(self.index_iterable[self.index])
    
    def go_next(self):
        self.index += self.step
        
        if (self.index<0) or (self.index>len(self.index_iterable)-1):
            self.index = len(self.index_iterable) - 1
            
            raise IndexError(
                'utils.IndexUsingNumberLetter.go_next: (self.index<0) or (self.index>len(self.index_iterable)-1), go to self.index == -1'
            )
    
    def go_previous(self):
        self.index -= self.step
        
        if (self.index<0) or (self.index>len(self.index_iterable)-1):
            self.index = 0
            
            raise IndexError(
                'utils.IndexUsingNumberLetter.go_previous: (self.index<0) or (self.index>len(self.index_iterable)-1), go to self.index == 0'
            )
