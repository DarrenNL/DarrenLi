import datetime
import time
from xml.dom import minidom


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

def svg_overwrite(filename, age_data):
    """
    Parse SVG files and update elements with my age, commits, stars, repositories, and lines written
    """
    svg = minidom.parse(filename)
    f = open(filename, mode='w', encoding='utf-8')
    tspan = svg.getElementsByTagName('tspan')
    tspan[53].firstChild.data = age_data
    f.write(svg.toxml('utf-8').decode('utf-8'))
    f.close()

if __name__ == '__main__':
    print('Calculation times:')
    age_data, age_time = perf_counter(daily_readme, datetime.datetime(2022, 7, 1))
    formatter('age calculation', age_time)
    svg_overwrite('dark_ver.svg', age_data)
    svg_overwrite('light_ver.svg', age_data)
