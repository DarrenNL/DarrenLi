import datetime
import time
from xml.dom import minidom
import pandas as pd

def daily_readme(date):
    """
    Returns the length of time since inception date
    e.g. 'XX' days
    """
    return '{}'.format((datetime.datetime.today() - date).days)

def formatter(query_type, difference, funct_return=False, whitespace=0):
    """
    Prints a formatted time differential
    Returns formatted result if whitespace is specified, otherwise returns raw result
    """
    print('{:<23}'.format('   ' + query_type + ':'), sep='', end='')
    print('{:>12}'.format('%.4f' % difference + ' s ')) if difference > 1 else print('{:>12}'.format('%.4f' % (difference * 1000) + ' ms'))
    if whitespace:
        return f"{'{:,}'.format(funct_return): <{whitespace}}"
    return funct_return

def format_plural(unit):
    """
    Returns a properly formatted number
    e.g.
    'day' + format_plural(diff.days) == 5
    >>> '5 days'
    'day' + format_plural(diff.days) == 1
    >>> '1 day'
    """
    return 's' if unit != 1 else ''

def perf_counter(funct, *args):
    """
    Calculates the time it takes for a function to run
    Returns the function result and the time differential
    """
    start = time.perf_counter()
    funct_return = funct(*args)
    return funct_return, time.perf_counter() - start

def svg_overwrite(filename, age_data, cagr_data, total_data, alpha_data, beta_data, sharpe_data, drawdown_data):
    """
    Parse SVG files and update elements with my age, commits, stars, repositories, and lines written
    """
    svg = minidom.parse(filename)
    f = open(filename, mode='w', encoding='utf-8')
    tspan = svg.getElementsByTagName('tspan')
    tspan[50].firstChild.data = cagr_data
    tspan[53].firstChild.data = age_data
    tspan[55].firstChild.data = total_data
    tspan[57].firstChild.data = alpha_data
    tspan[59].firstChild.data = beta_data
    tspan[61].firstChild.data = sharpe_data
    tspan[63].firstChild.data = drawdown_data
    f.write(svg.toxml('utf-8').decode('utf-8'))
    f.close()

if __name__ == '__main__':
    print('Calculation times:')
    age_data, age_time = perf_counter(daily_readme, datetime.datetime(2022, 7, 1))
    formatter('age calculation', age_time)
    data = pd.read_csv('performance.csv', header=None, index_col=0)[1].to_dict()
    cagr = "{}%".format(round(((data['total_performance']/100+1)**(365/int(age_data))-1)*100,2))
    total_performance = "{}%".format(data['total_performance'])
    alpha = "{}".format(data['alpha'])
    beta = "{}".format(data['beta'])
    sharpe = "{}".format(data['sharpe'])
    max_drawdown = "{}%".format(data['max_drawdown'])
    svg_overwrite('dark_ver.svg', age_data, cagr, total_performance, alpha, beta, sharpe, max_drawdown)
    svg_overwrite('light_ver.svg', age_data, cagr, total_performance, alpha, beta, sharpe, max_drawdown)
