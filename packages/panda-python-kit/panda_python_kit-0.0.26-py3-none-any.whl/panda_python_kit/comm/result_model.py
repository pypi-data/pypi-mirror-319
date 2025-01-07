import json


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
        data_dict = None
        if self.data:
            if hasattr(self.data, "to_dict"):
                data_dict = self.data.to_dict()
            else:
                data_dict = self.data
        return {
            "success": self.success,
            "data": data_dict,
            "message": self.message
        }


