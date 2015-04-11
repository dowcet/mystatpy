# This example uses pint to do calculations based on prices given in pre-decimal British pounds (shillings and pence).
# TODO format the numbers better in the output

# pint is available on pip as well as GitHub
from pint import UnitRegistry 
ureg = UnitRegistry()
Q_ = ureg.Quantity

# these defintiions could also be set in a text file
# just replace the above two lines with this one:
# ureg = UnitRegistry('/your/path/to/my_def.txt')
ureg.define('pound_sterling = [money] = L') 
ureg.define('shillings = L / 20 = d = s')
ureg.define('pence = s/12 = d')

#  1908: the company produced over 80,000 lbs. of rubber, which sold at an average 4s. 3.75d
price_1908 = (Q_(4, 's')) + (Q_(3.75, 'd'))
sales_1908 = 80000 * (price_1908.to('L'))

# 1910: crop rose to 320,000 lb. and sold for 6s. 2.5d
price_1910 = (Q_(6, 's')) + (Q_(2.5, 'd'))
sales_1910 = 320000 * (price_1910.to('L'))

# they issued L22,500 of shares in 1903
capital = (Q_(22500, 'L'))

print "1908 sales :", sales_1908
print "1910 sales :", sales_1910
print "Total:", sales_1908 + sales_1910
print
print "~", str(((sales_1908 + sales_1910) / capital))[0], "times initial capital issue of", str(capital)+"."  
