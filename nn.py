from engine import Value
import random


class Module():

    def zero_grad(self):
        for p in self.parameters:
            p.gradient = 0

    def parameters(self):
        return []


class Neuron(Module):

    def __init__(self, nin, nonlin=True):
        self.b = Value(0)
        self.w = [Value(random.uniform(-1,1)) for _ in range(nin)]
        self.nonlin = nonlin

    def __call__(self, x):
        res = sum((wi*xi for wi, xi in zip(self.w, x)), self.b)
        return res.relu() if self.nonlin else res
        
    def parameters(self):
        return self.w + [self.b]
    

class Layer(Module):

    def __init__(self, nin, nout, **kwargs):
        self.neurons = [Neuron(nin, **kwargs) for _ in range(nout)]

    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out)==1 else out
    
    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]

class MLP(Module):

    def __init__(self, nin, nouts):
        sz = [nin] + nouts 
        self.layers = [Layer(sz[i], sz[i+1], nonlin=i!=len(nouts)-1) for i in range(len(nouts))]

    def __call__(self, x):
        for l in self.layers:
            x = l(x)
        return x
    
    def parameters(self):
        return [p for l in self.layers for p in l.parameters()]
    

# mlp = MLP(2, [5, 2, 1])

# res = mlp([17, 12])