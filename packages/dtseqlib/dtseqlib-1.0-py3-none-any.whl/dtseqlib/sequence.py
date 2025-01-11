class Sequence:
    def __init__(self, seq=None):
        self.seq = seq or []
    
    def __repr__(self):
        return f"Sequence({self.seq})"
    
    def append(self, name=None, count=0):
        self.seq.append([name, count])
    
    def insert(self, name=None, count=0, index=0):
        self.seq.insert(index, [name, count])
    
    def delete(self, index=0):
        del self.seq[index]
    
    def clip(self, indexes=[-1, 0]):
        del self.seq[indexes[0]:indexes[1]+1]
    
    def get(self):
        return self.seq

    def scan(self, index=0):
        return self.seq[index]
    
    def multiple_scan(self, indexes=[-1, 0]):
        return self.seq[indexes[0]:indexes[1]+1]
    def scan_cbn(self, name=None):
        names = []
        for block in self.seq:
            if block[0] == name:
                names.append(block[1])
        return names
    
    def scan_nbc(self, count=0):
        array = []
        for block in self.seq:
            if block[1] == count:
                array.append(block[0])
        return array
    
    def get_bwn(self, name=None):
        blocks = []
        for block in self.seq:
            if block[0] == name:
                blocks.append(block)
        return blocks
   
    def get_bwc(self, count=0):
        blocks = []
        for block in self.seq:
            if block[1] == count:
                blocks.append(block)
        return blocks
    
    def to_list(self):
        array = []
        for block in self.seq:
            for _ in range(block[1]):
                array.append(block[0])
        return array
   
    def __len__(self):
        return len(self.seq)
