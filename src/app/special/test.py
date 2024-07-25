'''
File to confirm tests are working
'''

def add_two_nums(a: int, b: int):
    '''
    s.e.
    '''
    if isinstance(a, (int, float)) and isinstance(b, (int,float)):
        return a+b
    raise Exception
