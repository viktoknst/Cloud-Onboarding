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

    @staticmethod
    def from_dict(json_dict: dict):
        '''
        Initialize from dict
        '''
        return Result(
            json_dict['id'],
            json_dict['result']
        )
