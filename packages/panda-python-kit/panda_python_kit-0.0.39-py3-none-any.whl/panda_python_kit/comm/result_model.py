import json

from panda_python_kit.comm.comm import nested_to_dict


class ResultModel:
    def __init__(self,success=True,data=None,message=""):
        self.success = success
        self.data = data
        self.message = message

    def __str__(self):
        return "success:%s,data:%s,message:%s" % (self.success,self.data,self.message)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        data_dict = nested_to_dict(self.data)
        return {
            "success": self.success,
            "data": data_dict,
            "message": self.message
        }




