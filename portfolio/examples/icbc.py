# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

#     INFORMATION
#             Symbol                                                                            1105001.IB
#             Short Name                                                                ICBC 5.56% B310630
#             Close (D)\r\n[Trade Date] Last Closing Day\r\n[Price Type] Dirty Price              103.1889
#             Bid Yield (Optimal)\r\n[Trade Date] Last Closing Day\r\n[Unit] %                         NaN
#             Initial Face Value                                                                     100.0
#             Latest Bond Rating                                                                       AAA
#             Maturity Date                                                                     2031-06-30
#             Coupon Type                                                            Fixed Interest Rate
#             Interest Accrual Method                                                 Simple interest
#             Coupon Description                                                    5.56%
#             Coupon Frequency                                                        1
#             Coupon Date (Y)\r\n[N] 1                                             6月30日
#             Bond Term (Year)\r\n[Unit] Yearly                                    20.0
#             Maturities (Text)                                                     15+5
#             Interest Reference                                                     ACT/ACT
#             Coupon Date Description           Pay interest on June 30 every year, and postpo...
#             Bond Term (Year)\r\n[Unit] Yearly.1                                     20.0
#             Issue Amount\r\n[Unit] (100M)                                           380.0
#             Remaing Maturity                                                         9.41
#     """

# + tags=[]
import QuantLib as ql
import prettytable as pt

today = ql.Date(27, ql.January , 2022)
ql.Settings.instance().evaluationDate = today

settlementDays = 1
faceAmount = 100.0

# +
effectiveDate = ql.Date(30, ql.June, 2011)
terminationDate = ql.Date(30, ql.June, 2031)
tenor = ql.Period(1, ql.Years)
calendar = ql.China(ql.China.IB)
convention = ql.Unadjusted
terminationDateConvention = convention
rule = ql.DateGeneration.Backward
endOfMonth = False

schedule = ql.Schedule(
    effectiveDate,
    terminationDate,
    tenor,
    calendar,
    convention,
    terminationDateConvention,
    rule,
    endOfMonth)

for s in schedule:
    print(s)

coupons = ql.DoubleVector(1)
coupons[0] = 5.56 / 100.0
accrualDayCounter = ql.ActualActual(
    ql.ActualActual.Bond, schedule)
paymentConvention = ql.Unadjusted

bond = ql.FixedRateBond(
    settlementDays,
    faceAmount,
    schedule,
    coupons,
    accrualDayCounter,
    paymentConvention)

# +
bondYield = 4.0910 / 100.0

compounding = ql.Compounded
frequency = ql.Annual

termStructure = ql.YieldTermStructureHandle(
    ql.FlatForward(
        settlementDays,
        calendar,
        bondYield,
        accrualDayCounter,
        compounding,
        frequency))

engine = ql.DiscountingBondEngine(termStructure)
bond.setPricingEngine(engine)

# + tags=[]
cleanPrice = bond.cleanPrice()
dirtyPrice = bond.dirtyPrice()
accruedAmount = bond.accruedAmount()

duration = ql.BondFunctions.duration(
    bond,
    bondYield,
    accrualDayCounter,
    compounding,
    frequency)

convexity = ql.BondFunctions.convexity(
    bond,
    bondYield,
    accrualDayCounter,
    compounding,
    frequency)

bps = ql.BondFunctions.basisPointValue(
    bond,
    bondYield,
    accrualDayCounter,
    compounding,
    frequency)

tab = pt.PrettyTable(['item', 'QuantLib', 'ShClearing'])
tab.add_row(['clean price', cleanPrice, 111.2672])
tab.add_row(['dirty price', dirtyPrice, 114.4813])
tab.add_row(['accrued amount', accruedAmount, 3.2141])
tab.add_row(['duration', duration, 3.9367])
tab.add_row(['convexity', convexity, 20.9452])
tab.add_row(['bps', abs(bps), 0.0451])

tab.float_format = '.4'

print(tab)

# -


