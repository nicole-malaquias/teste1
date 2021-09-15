class FieldError(Exception):

    
    def __init__(self, data):
        
        data = list(data)
        problem = [ i for i in data if i not in ["anime","season","released_date"] ]
        
        self.message = {
            "available_keys": [
                "anime", "released_date","season",
                ],
            "Wrong_keys_sended": [*problem]          
        }
        super().__init__(self.message)