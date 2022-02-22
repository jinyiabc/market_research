import pandas as pd
# from QuantLib import Date, DateVector
from matplotlib.dates import MonthLocator, YearLocator, DateFormatter
from matplotlib.ticker import FuncFormatter
from datetime import date
import pylab
import QuantLib as ql
import unittest
from helper.parametrizedtestcase import ParametrizedTestCase
from pandas import DataFrame

default_plot_size=(12,8)

def plot(figsize=None):
    f = pylab.figure(figsize=figsize or default_plot_size)
    ax = f.add_subplot(1,1,1)

    for side in ['top', 'right']:
        ax.spines[side].set_visible(False)
    ax.xaxis.grid(True, 'major', color=(0.9, 0.9, 0.9))
    ax.yaxis.grid(True, 'major', color=(0.9, 0.9, 0.9))

    return f, ax

def highlight_x_axis(ax):
    ax.axhline(0.0, linewidth=1, color=(0.5,0.5,0.5))

def to_datetime(d):
    return date(d.year(), d.month(), d.dayOfMonth())

def format_rate(r, digits=2):
    format = '%.' + str(digits) + 'f %%'
    return format % (r*100.0)

def rate_formatter(digits=2):
    return FuncFormatter(lambda r,pos: format_rate(r,digits))

def date_formatter():
    return DateFormatter("%b '%y")

def locator(span):
    if span < 400:
        return MonthLocator()
    elif 400 <= span < 800:
        return MonthLocator(bymonth=[1,4,7,10])
    elif 800 <= span < 3700:
        return YearLocator()
    else:
        return YearLocator(5)
    
def plot_curve(ax,dates,rates,ymin=None,ymax=None,digits=2,
               format_rates=False):
    span = dates[-1] - dates[0]
    dates = [ to_datetime(d) for d in dates ]
    for (rs, style) in rates:
        ax.plot_date(dates, rs, style)
    ax.set_xlim(min(dates),max(dates))
    ax.xaxis.set_major_locator(locator(span))
    ax.xaxis.set_major_formatter(date_formatter())
    ax.autoscale_view()
    ax.set_ylim(ymin,ymax)
    if format_rates:
        ax.yaxis.set_major_formatter(rate_formatter(digits))

def get_spot_rates(
        yieldcurve, day_count,
        calendar=ql.UnitedStates(), months=121):
    spots = []
    tenors = []
    ref_date = yieldcurve.referenceDate()
    print(ref_date)
    calc_date = ref_date
    for month in range(0, months):
        yrs = month/12.0
        d = calendar.advance(ref_date, ql.Period(month, ql.Months))
        compounding = ql.Compounded
        freq = ql.Annual
        zero_rate = yieldcurve.zeroRate(yrs, compounding, freq)
        tenors.append(yrs)
        eq_rate = zero_rate.equivalentRate(
            day_count,compounding,freq,calc_date,d).rate()
        spots.append(100*eq_rate)
    return DataFrame(list(zip(tenors, spots)),
                     columns=["Maturities","Curve"],
                     index=['']*len(tenors))

def run_test(param=None):
    print("testing QuantLib " + ql.__version__)
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(DayCountersTest, param=param))
    unittest.TextTestRunner(verbosity=2).run(suite)
    
class DayCountersTest(ParametrizedTestCase):
    def test_calendar(self):
        "Testing daycounters"
        calendar = ql.UnitedStates()
        ql.Business252(calendar)

    def test_datacounting(self):
        dates = list(self.param)
        df = pd.DataFrame()
        df['start date'] = dates[:-1]
        df['end date'] = dates[1:]
        df['days'] = df['end date'] - df['start date']

        print(df)

    def testChinaSSE(self):
        print("Testing China Shanghai Stock Exchange holiday list...")

        expectedHol = ql.DateVector()

        # China Shanghai Securities Exchange holiday list in the year 2021
        expectedHol.push_back(ql.Date(1, ql.January, 2021))
        expectedHol.push_back(ql.Date(11, ql.February, 2021))
        expectedHol.push_back(ql.Date(12, ql.February, 2021))
        expectedHol.push_back(ql.Date(15, ql.February, 2021))
        expectedHol.push_back(ql.Date(16, ql.February, 2021))
        expectedHol.push_back(ql.Date(17, ql.February, 2021))
        expectedHol.push_back(ql.Date(5, ql.April, 2021))
        expectedHol.push_back(ql.Date(3, ql.May, 2021))
        expectedHol.push_back(ql.Date(4, ql.May, 2021))
        expectedHol.push_back(ql.Date(5, ql.May, 2021))
        expectedHol.push_back(ql.Date(14, ql.June, 2021))
        expectedHol.push_back(ql.Date(20, ql.September, 2021))
        expectedHol.push_back(ql.Date(21, ql.September, 2021))
        expectedHol.push_back(ql.Date(1, ql.October, 2021))
        expectedHol.push_back(ql.Date(4, ql.October, 2021))
        expectedHol.push_back(ql.Date(5, ql.October, 2021))
        expectedHol.push_back(ql.Date(6, ql.October, 2021))
        expectedHol.push_back(ql.Date(7, ql.October, 2021))

        c = ql.China(ql.China.SSE)
        hol = c.holidayList(ql.Date(1, ql.January, 2021), ql.Date(31, ql.December, 2021))

        for i in range(min(len(hol), len(expectedHol))):
            self.assertFalse(hol[i] != expectedHol[i])

        self.assertFalse(len(hol) != len(expectedHol))

    def testChinaIB(self):
        print("Testing China Inter Bank working weekends list...")

        expectedWorkingWeekEnds = ql.DateVector()

        # China Inter Bank working weekends list in the year 2021
        expectedWorkingWeekEnds.push_back(ql.Date(7, ql.February, 2021))
        expectedWorkingWeekEnds.push_back(ql.Date(20, ql.February, 2021))
        expectedWorkingWeekEnds.push_back(ql.Date(25, ql.April, 2021))
        expectedWorkingWeekEnds.push_back(ql.Date(8, ql.May, 2021))
        expectedWorkingWeekEnds.push_back(ql.Date(18, ql.September, 2021))
        expectedWorkingWeekEnds.push_back(ql.Date(26, ql.September, 2021))
        expectedWorkingWeekEnds.push_back(ql.Date(9, ql.October, 2021))

        c = ql.China(ql.China.IB)
        start = ql.Date(1, ql.January, 2021)
        end = ql.Date(31, ql.December, 2021)

        k = 0

        while start <= end:
            if c.isBusinessDay(start) and c.isWeekend(start.weekday()):
                self.assertFalse(expectedWorkingWeekEnds[k] != start)
                k += 1

            start += ql.Period(1, ql.Days)

        self.assertFalse(k != (len(expectedWorkingWeekEnds)))

    def testBusinessDaysBetween(self):
        print("Testing calculation of business days between dates...")

        testDates = ql.DateVector()
        testDates.push_back(ql.Date(1, ql.February, 2002))  # isBusinessDay = true
        testDates.push_back(ql.Date(4, ql.February, 2002))  # isBusinessDay = true
        testDates.push_back(ql.Date(16, ql.May, 2003))  # isBusinessDay = true
        testDates.push_back(ql.Date(17, ql.December, 2003))  # isBusinessDay = true
        testDates.push_back(ql.Date(17, ql.December, 2004))  # isBusinessDay = true
        testDates.push_back(ql.Date(19, ql.December, 2005))  # isBusinessDay = true
        testDates.push_back(ql.Date(2, ql.January, 2006))  # isBusinessDay = true
        testDates.push_back(ql.Date(13, ql.March, 2006))  # isBusinessDay = true
        testDates.push_back(ql.Date(15, ql.May, 2006))  # isBusinessDay = true
        testDates.push_back(ql.Date(17, ql.March, 2006))  # isBusinessDay = true
        testDates.push_back(ql.Date(15, ql.May, 2006))  # isBusinessDay = true
        testDates.push_back(ql.Date(26, ql.July, 2006))  # isBusinessDay = true
        testDates.push_back(ql.Date(26, ql.July, 2006))  # isBusinessDay = true
        testDates.push_back(ql.Date(27, ql.July, 2006))  # isBusinessDay = true
        testDates.push_back(ql.Date(29, ql.July, 2006))  # isBusinessDay = false
        testDates.push_back(ql.Date(29, ql.July, 2006))  # isBusinessDay = false

        # default params: from date included, to excluded
        expected = [
            1, 321, 152, 251, 252, 10, 48, 42, -38, 38, 51, 0, 1, 2, 0]

        # exclude from, include to
        expected_include_to = [
            1, 321, 152, 251, 252, 10, 48, 42, -38, 38, 51, 0, 1, 1, 0]

        # include both from and to
        expected_include_all = [
            2, 322, 153, 252, 253, 11, 49, 43, -39, 39, 52, 1, 2, 2, 0]

        # exclude both from and to
        expected_exclude_all = [
            0, 320, 151, 250, 251, 9, 47, 41, -37, 37, 50, 0, 0, 1, 0]

        calendar = ql.Brazil()

        for i in range(1, len(testDates)):
            calculated = calendar.businessDaysBetween(
                testDates[i - 1], testDates[i], True, False)
            self.assertFalse(calculated != expected[i - 1])

            calculated = calendar.businessDaysBetween(
                testDates[i - 1], testDates[i], False, True)
            self.assertFalse(calculated != expected_include_to[i - 1])

            calculated = calendar.businessDaysBetween(
                testDates[i - 1], testDates[i], True, True)
            self.assertFalse(calculated != expected_include_all[i - 1])

            calculated = calendar.businessDaysBetween(
                testDates[i - 1], testDates[i], False, False)
            self.assertFalse(calculated != expected_exclude_all[i - 1])