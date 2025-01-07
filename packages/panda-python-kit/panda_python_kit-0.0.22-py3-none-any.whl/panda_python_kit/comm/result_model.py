import json


class ResultModel:
    def __init__(self,success=True,data=None,message=""):
        self.success = success
        self.data = data
        self.message = message

    def __str__(self):
        return "success:%s,data:%s,message:%s" % (self.success,self.data,self.message)

    def to_json(self):
        return json.dumps(self.__dict__())

    def __dict__(self):
        return  {
            "success":self.success,
            "data": self.data,
            "message":self.message
        }