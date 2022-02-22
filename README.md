
# bond yield calculator
Wrap function from below links.
https://www.codearmo.com/python-tutorial/python-bond-yield-calculator

#usage:
    from helper.bond import bond_yield
    from collections import namedtuple
    price = 112.637

    # NOTICE: Bond yield and name is no longer an entry.
    Bond_Data = namedtuple("Bond_Data",
                           """ 
                           coupon_schedule, 
                           coupon_rate, 
                           coupon_freq, 
                           face,  
                           prev_coupon""")

    corp_5_2026_coupon_schedule = [(2022, 9, 1),
                                   (2023, 9, 1),
                                   (2024, 9, 1),
                                   (2025, 9, 1),
                                   (2026, 9, 1)]

    corp_5_2026 = Bond_Data(corp_5_2026_coupon_schedule,
                            0.05,
                            1,
                            100,
                            (2021, 9, 1))

    settlement_date = (2021, 9, 1)
    bond_yield(settlement_date, *corp_5_2026, price, precision = 12, show_stats = True)

OUTPUT: This function estimated the bond yield within 12 decimal places using a total of 4 guesses
The price difference at this yield is : 0.0
RESULT: 0.022958874083290805
