def buniform(shape, dtype='float32', device='cpu'):
    r"""generates binary-uniform subsampling matrix

    Generates M-by-N binary-uniform observation matrix.

    Parameters
    ----------
    shape : list or tuple
        shape of Gauss observation matrix [M, N]
    dtype : str, optional
        torch's data type, such as ``'float32'``, ``'bool'``, by default ``'float32'``
    device : str, optional
        generates data on the specified device, supported are ``'cpu'``, ``'cuda:x'``, where, `x` is the cuda device's id.

    Returns
    -------
    th.Tensor
        binary-uniform subsampling observation matrix :math:`\bm A`.
 
    Examples
    ---------

    .. image:: ./_static/BuniformMatrix.png
       :scale: 98 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::
        
        import torchbox as tb

        imgfile = tb.data_path('optical') + 'LenaGRAY128.png'
        X = tb.imread(imgfile)* 1.

        Phi = tb.buniform(shape=(64, 128))
        print(Phi.shape)

        Y = Phi @ X

        plt = tb.imshow([X, Phi, Y], titles=['Full', 'Subsampling matrix', 'Subsampled'])
        plt.show()

    """

def brandom(shape, seed=None, dtype='float32', device='cpu'):
    r"""generates binary-random subsampling matrix

    Generates M-by-N binary-random observation matrix which have uniform distribution elements.

    Parameters
    ----------
    shape : list or tuple
        shape of Gauss observation matrix [M, N]
    seed : int or None, optional
        the seed for random number generator, by default None
    dtype : str, optional
        torch's data type, such as ``'float32'``, ``'bool'``, by default ``'float32'``
    device : str, optional
        generates data on the specified device, supported are ``'cpu'``, ``'cuda:x'``, where, `x` is the cuda device's id.

    Returns
    -------
    th.Tensor
        binary-random subsampling observation matrix :math:`\bm A`.
 
    Examples
    ---------

    .. image:: ./_static/BrandomMatrix.png
       :scale: 98 %
       :align: center

    The results shown in the above figure can be obtained by the following codes.

    ::
        
        import torchbox as tb

        imgfile = tb.data_path('optical') + 'LenaGRAY128.png'
        X = tb.imread(imgfile)* 1.

        Phi = tb.brandom(shape=(64, 128))
        print(Phi.shape)

        Y = Phi @ X

        plt = tb.imshow([X, Phi, Y], titles=['Full', 'Subsampling matrix', 'Subsampled'])
        plt.show()

    """

def bbernoulli(shape, seed=None, dtype='float32', device='cpu'):
    r"""generates binary-bernoulli subsampling matrix

    Generates M-by-N binary-random observation matrix which have bernoulli distribution elements.

    Parameters
    ----------
    shape : list or tuple
        shape of Gauss observation matrix [M, N]
    seed : int or None, optional
        the seed for random number generator, by default None
    dtype : str, optional
        torch's data type, such as ``'float32'``, ``'bool'``, by default ``'float32'``
    device : str, optional
        generates data on the specified device, supported are ``'cpu'``, ``'cuda:x'``, where, `x` is the cuda device's id.

    Returns
    -------
    th.Tensor
        binary-random subsampling observation matrix :math:`\bm A`.
 
    """


