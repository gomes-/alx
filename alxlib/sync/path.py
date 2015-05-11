__author__ = 'Alex Gomes'

class SyncPath():

    def __init__(self):
        self.IsDir = False
        self.IsFile = False
        self.BasePath=""
        self.AbsPath=""
        self.SPath=""
        self.CreationTS=""
        self.ModifiedTS=""
        self.MD5=""
        self.Size=0
        self.sys=""

    def __str__(self):
        return "IsDir: {0}, IsFile:{1}, AbsPath:{2}, SPath:{3}"\
            .format(self.IsDir, self.IsFile, self.AbsPath, self.SPath)

    """def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        import copy
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result"""




