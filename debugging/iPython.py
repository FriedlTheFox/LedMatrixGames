try:
    from ipHelp import IPS, ST, ip_syshook, dirsearch, sys
    ip_syshook(1)
except ImportError:
    pass


x = 0
IPS()
print('x = %s' %  x)
