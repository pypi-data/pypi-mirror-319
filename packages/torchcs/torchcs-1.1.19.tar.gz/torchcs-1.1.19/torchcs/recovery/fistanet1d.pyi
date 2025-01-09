def initialize_weights(self):
    ...

class BasicBlock1d(th.nn.Module):
    ...

    def __init__(self, cin=1, chi=32):
        ...

    def forward(self, x, PhiTPhi, PhiTy, mu, thresh):
        ...

class FISTAnetCore(th.nn.Module):
    ...

    def __init__(self, Phi, nlay=6, cin=1, chi=32):
        ...

    def forward(self, x0, y):
        ...

class FISTAnet1d(object):
    r"""ISTAnet for compressed reconstruction

    Parameters
    ----------
    cin : int, optional
        the number of channels of input signal, by default 1
    lr : float, optional
        learning rate, by default 0.1
    seed : int or None, optional
        random seed for weight initialization, by default None (not set)
    device : str, optional
        computation device, ``'cuda:x'`` or ``'cpu'`` by default ``'cpu'``
    """        

    def __init__(self, Phi, nlay=3, cin=1, chi=32, lr=0.1, seed=None, device='cpu'):
        ...

    def train(self, Ytrain, Xtrain, Yvalid, Xvalid, bs, nepoch):
        r"""train

        Parameters
        ----------
        Ytrain : tensor
            input for training, :math:`N\times C\times L`
        Xtrain : tensor
            target for training
        Yvalid : tensor
            input for validation
        Xvalid : tensor
            target for validation
        bs : int
            batch size
        nepoch : int
            the number of epochs
        """        

    def test(self, Y, bs):
        r"""test

        Parameters
        ----------
        Y :  tensor
             input for testing, :math:`N\times C\times L`

        bs :  int
             batch size

        Returns
        -------
         tensor
             recovered signals
        """        

    def save(self, modelfile):
        r"""save network model to a file

        Parameters
        ----------
        modelfile :  str
             model file path
        """        

    def load(self, modelfile):
        r"""load network model from a file

        Parameters
        ----------
        modelfile :  str
             model file path
        """        


