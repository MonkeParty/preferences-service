from pydantic import BaseModel

class ActionRequest(BaseModel):
    '''
        Example:
        `{
            "film_id" : 123,
            "user_id" : 12,
            "action" : "film_rate",
            "value" : {
                "rate" : 1
            }
        }`
    '''
    film_id : int
    user_id : int
    action : str
    value : object
