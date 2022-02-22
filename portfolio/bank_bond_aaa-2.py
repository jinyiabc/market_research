import pandas as pd
from datetime import datetime, date
import QuantLib as ql

def date_manipulate(x):
    x = datetime.strptime(x, '%m月%d日')
    return x


if __name__ == '__main__':
    """
    Assumption: Yield Curve do not change during holding period.
    """

    commercial_bank_chinabond = pd.read_csv('../resource/金融债上清所0127.csv',
                                                parse_dates=["Coupon Date"],
                                                date_parser=date_manipulate,
                                                )
    bond_data = commercial_bank_chinabond.iloc[0]
    """
证券代码                                                   091501005.IB
证券简称                                                      15中国信达债05
收盘价\n[交易日期] 2022-01-27\n[债券价格类型] 收益率\n[单位] 元                 3.2717
收盘价\n[交易日期] 2022-01-27\n[债券价格类型] 净价\n[单位] 元                104.4932
收盘价\n[交易日期] 2022-01-27\n[债券价格类型] 全价\n[单位] 元                106.0685
报价买入收益率(最优)\n[交易日期] 2022-01-27\n[单位] %                          NaN
剩余期限(年)\n[日期] 最新\n[单位] 年                                     3.6411
债券初始面值\n[单位] 元                                                100.0
最新债项评级                                                          AAA
到期日期                                                     2025-09-24
利率类型                                                           固定利率
计息方式                                                             单利
利率说明                                                          4.60%
每年付息次数                                                            1
Coupon Date                                     1900-09-24 00:00:00
债券期限(年)\n[单位] 年                                                10.0
债券期限(文字)                                                         10
计息基准                                                        ACT/ACT
付息日说明                                               每年9月24日付息,节假日顺延
债券期限(年)\n[单位] 年.1                                              10.0
发行总额\n[单位] (100M)元                              10,000,000,000.0000
    """

    # today = date.today()
    # coupon_date = bond_icbc['Coupon Date (Y)\r\n[N] 1']
    # maturity_date = bond_icbc['Maturity Date']
    # bond_b_coupon_schedule = pd.date_range(start=settlement_date, end=maturity_date, freq='y')
    # settlement_date = (2022, 1, 27)
    # horizon_date = (2023, 1, 27)
    coupon_rate = 0.0460
    # coupon_freq = 1
    # prev_coupon = (2021, 6, 30)

    # Global settings.

    settlement_date = ql.Date(27, 1, 2022)
    ql.Settings.instance().evaluationDate = ql.Date(27, 1, 2022)

    # generate schedule
    issue_date = ql.Date(24, 9, 2015)
    maturity_date = ql.Date(24, 9, 2025)
    tenor = ql.Period(ql.Annual)
    calendar = ql.China()
    business_convention = ql.Following
    date_generation = ql.DateGeneration.Forward
    month_end = False
    schedule = ql.Schedule(issue_date, maturity_date, tenor,
                           calendar, business_convention,
                           business_convention, date_generation,
                           month_end)
    settlementDays = 1
    dc = ql.Actual365Fixed()
    fixed_leg = ql.FixedRateLeg(schedule, dc, [100], [coupon_rate])
    bond = ql.Bond(settlementDays, ql.TARGET(), issue_date, fixed_leg)

    # YIELD = 0.032717
    # dirty_price = bond.dirtyPrice(YIELD, ql.Actual365Fixed(), ql.Compounded, ql.Annual)   # dirtyPrice(yield, dayCount, compounding, frequency)
    # accrual_amount = bond.accruedAmount(settlement_date)
    # clean_price = bond.cleanPrice(YIELD, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    #
    # print(dirty_price, clean_price, accrual_amount)
    # assert dirty_price == 106.0685  # 106.08082921441382
    # assert clean_price == 104.4932   # 104.49288400893438
    # assert accrual_amount == 1.5754    #

    # 上海清算所商业银行债收益率曲线(AAA) 1-27
    spot_dates = [ql.Date(27, 1, 2022),
                  ql.Date(27, 2, 2022),
                  ql.Date(27, 4, 2022),
                  ql.Date(27, 7, 2022),
                  ql.Date(27, 10, 2022),
                  ql.Date(27, 1, 2023),
                  ql.Date(27, 1, 2024),
                  ql.Date(27, 1, 2025),
                  ql.Date(27, 1, 2026),
                  ql.Date(27, 1, 2027),
                  ql.Date(27, 1, 2028),
                  ql.Date(27, 1, 2029),
                  ql.Date(27, 1, 2030),
                  ql.Date(27, 1, 2031),
                  ql.Date(27, 1, 2032),
                  ]
    spot_rates = [
        # 上海清算所国债收益率曲线(AAA) 1 - 27
        # 1.5982 / 100,
        # 1.6706 / 100,
        # 1.8043 / 100,
        # 1.9323 / 100,
        # 1.981 / 100,
        # 2.0144 / 100,
        # 2.184 / 100,
        # 2.263 / 100,
        # 2.3959 / 100,
        # 2.4873 / 100,
        # 2.5735 / 100,
        # 2.6836 / 100,
        # 2.7345 / 100,
        # 2.7516 / 100,
        # 2.7633 / 100,
        # 上海清算所商业银行债收益率曲线(AAA) 1 - 27
        1.95 / 100,
        2.4198 / 100,
        2.4292 / 100,
        2.4599 / 100,
        2.4892 / 100,
        2.5 / 100,
        2.6465 / 100,
        2.7481 / 100,
        2.9432 / 100,
        3.148 / 100,
        3.2909 / 100,
        3.4466 / 100,
        3.5317 / 100,
        3.5748 / 100,
        3.6285 / 100,
    ]
    day_count = ql.Actual360()
    interpolation = ql.Linear()
    compounding = ql.Compounded
    compounding_frequency = ql.Annual
    spot_curves = []

    spot_curves.append(ql.ZeroCurve(spot_dates, spot_rates, day_count, calendar, ))
    spot_curves.append(ql.LogLinearZeroCurve(spot_dates, spot_rates, day_count, calendar, ))
    spot_curves.append(ql.CubicZeroCurve(spot_dates, spot_rates, day_count, calendar, ))
    spot_curves.append(ql.NaturalCubicZeroCurve(spot_dates, spot_rates, day_count, calendar, ))
    spot_curves.append(ql.LogCubicZeroCurve(spot_dates, spot_rates, day_count, calendar, ))
    spot_curves.append(ql.MonotonicCubicZeroCurve(spot_dates, spot_rates, day_count, calendar, ))
    for spot_curve in spot_curves:
        spot_curve_handle = ql.YieldTermStructureHandle(spot_curve)
        bond_engine = ql.DiscountingBondEngine(spot_curve_handle)
        bond.setPricingEngine(bond_engine)
        bond.cleanPrice();print(bond.cleanPrice())
        # bond.NPV(); print(bond.NPV())
        # bond.accruedAmount(); print(bond.accruedAmount())
        # bond.dirtyPrice();print(bond.dirtyPrice())