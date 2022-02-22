import QuantLib as ql
import prettytable as pt

def test0():
    today = ql.Date(28, ql.July, 2020)
    ql.Settings.instance().evaluationDate = today

    settlementDays = 1
    faceAmount = 100.0

    effectiveDate = ql.Date(10, ql.March, 2020)
    terminationDate = ql.Date(10, ql.March, 2030)
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

    # for s in schedule:
    #     print(s)

    coupons = ql.DoubleVector(1)
    coupons[0] = 3.07 / 100.0
    accrualDayCounter = ql.Actual365Fixed()
    paymentConvention = ql.Unadjusted

    bond = ql.FixedRateBond(
        settlementDays,
        faceAmount,
        schedule,
        coupons,
        accrualDayCounter,
        paymentConvention)

    bondYield = 3.4124 / 100.0

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
    tab.add_row(['clean price', cleanPrice, 97.2211])
    tab.add_row(['dirty price', dirtyPrice, 98.4071])
    tab.add_row(['accrued amount', accruedAmount, 1.1859])
    tab.add_row(['duration', duration, 8.0771])
    tab.add_row(['convexity', convexity, 79.2206])
    tab.add_row(['bps', abs(bps), 0.0795])

    tab.float_format = '.4'

    print(tab)
