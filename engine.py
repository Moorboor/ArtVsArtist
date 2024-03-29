class Value():

    def __init__(self,  value, parent=(), func=""):

        self.parent = parent
        self.value = value 
        self._backward = lambda: None
        self.func = func
        self.gradient = 0

    def __add__(self, other):

        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.value + other.value, parent=(self, other), func="+") 

        def _backward():
            self.gradient += out.gradient
            other.gradient += out.gradient
        
        out._backward = _backward
        return out

    def __mul__(self, other):
        
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.value * other.value, parent=(self, other), func="*")
        
        def _backward():
            self.gradient += self.value * out.value
            other.gradient += other.value * out.value
        
        out._backward = _backward 
        return out

    def __pow__(self, other):
        out = Value(self.value**other, parent=(self,), func="**")
        
        def _backward():
            self.gradient += (other*self.value**(other-1)) * out.gradient
        out._backward = _backward

        return out 

    def relu(self):
        out = Value(self.value if self.value > 0 else 0, (self,), "relu")

        def _backward():
            self.gradient += (self.value>0) * out.gradient
        out._backward = _backward
        return out


    def backward(self):
        
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for p in v.parent:
                    build_topo(p)
                topo.append(v) 

        build_topo(self)
        
        self.gradient = 1
        for v in reversed(topo):
            v._backward()

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other): # other - self
        return other + (-self)

    def __radd__(self, other): # other + self
        return self + other
    
    def __rmul__(self, other): # other * self
        return self * other
    

    

# a = Value(5)

# b = a + 5
# c = b + 6
# d = c - 4
# e = d.relu()
# f = e * 5
# g = f.relu()
# h = g - 3
# i = 5 - h