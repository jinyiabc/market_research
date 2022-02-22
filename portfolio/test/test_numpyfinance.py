import numpy_financial as npf
import numpy as np

def test_irr():
    irr = npf.irr([-250000, 100000, 150000, 200000, 250000, 300000]) # internal rate of return.
    print(irr)
    pass

def test_npv():
    from numpy_financial import npv, irr
    x = np.array([-250000, 100000, 150000, 200000, 250000, 300000])
    r = irr(x)
    print(r)
    pass