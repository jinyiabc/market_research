https://www.youtube.com/watch?v=__PBUqjCy6E&list=PLu_PrO8j6XAvOAlZND9WUPwTHY_GYhJVr&index=1

# Embed testSuite for data validation. 
# usage:
`from utils import run_test` \
`from test.<module> import <test class>` \

`run_test(<test_class>())`


# eg:
`from utils import run_test`

`from test.daycounters import DayCountersTest`

`run_test(DayCountersTest())`