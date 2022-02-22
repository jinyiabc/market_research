import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as pl

# sum of squared errors of decision variables
def ObjectiveFunction(x, args):
    return np.sum(np.power(np.diff(x), 2) * args[0])

# zero coupon bond pricing function
def ZeroCouponBond(x, args):
    # return difference between calculated and market price
    return ((1 / (1 + x[args[3]])**args[2]) - args[0]) * args[1]

# zero coupon bond pricing functions as constraints
# args: market price, scaling factor, maturity, index number for rate array
zeroPrices = ({'type': 'eq', 'fun': ZeroCouponBond, 'args': [[0.998801438274071, 1000000.0, 1.0, 0]]},
            {'type': 'eq', 'fun': ZeroCouponBond, 'args': [[0.996210802629012, 1000000.0, 2.0, 1]]},
            {'type': 'eq', 'fun': ZeroCouponBond, 'args': [[0.991943543964159, 1000000.0, 3.0, 2]]},
            {'type': 'eq', 'fun': ZeroCouponBond, 'args': [[0.981028206597786, 1000000.0, 4.0, 3]]},
            {'type': 'eq', 'fun': ZeroCouponBond, 'args': [[0.962851266220459, 1000000.0, 5.0, 4]]},
            {'type': 'eq', 'fun': ZeroCouponBond, 'args': [[0.946534719794057, 1000000.0, 6.0, 5]]},
            {'type': 'eq', 'fun': ZeroCouponBond, 'args': [[0.924997530805076, 1000000.0, 7.0, 6]]},
            {'type': 'eq', 'fun': ZeroCouponBond, 'args': [[0.912584111300984, 1000000.0, 8.0, 7]]},
            {'type': 'eq', 'fun': ZeroCouponBond, 'args': [[0.892632531026722, 1000000.0, 9.0, 8]]},
            {'type': 'eq', 'fun': ZeroCouponBond, 'args': [[0.877098137542374, 1000000.0, 10.0, 9]]})

# initial guesses for ten zero-coupon rates
initialGuess = np.full(10, 0.005)
model = opt.minimize(ObjectiveFunction, initialGuess, args = ([1000000.0]), method = 'SLSQP', constraints = zeroPrices)

# print selected model results
print('Success: ' + str(model.success))
print('Message: ' + str(model.message))
print('Number of iterations: ' + str(model.nit))
print('Objective function (sum of squared errors): ' + str(model.fun))
print('Changing variables (zero-coupon rates): ' + str(model.x * 100))
pl.plot(model.x)
pl.show()