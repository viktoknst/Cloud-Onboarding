'''
Result model
'''
class Result:
    '''
    Result model
    '''
    id: str
    result: str

    def __init__(self, id: str, result: str):
        self.id = id
        self.result = result
