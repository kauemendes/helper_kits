

class BaseController(object):

    model = None

    def __init__(self, model):
        self.model = model

    def save(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def get_list(self, *args, **kwargs):
        pass

    def get_one(self, id):
        pass
