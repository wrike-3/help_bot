import yaml


class ConfigBot():
    def __init__(self, root_path, values):
        super().__init__()
        self.read(values)

    @classmethod
    def load(cls, root_path, path):
        values = yaml.load(open(f'{root_path}/{path}'), Loader=yaml.FullLoader)
        values = {k: f'{root_path}/{v}' if isinstance(v, str) else v for k, v in values.items() }
        return cls(root_path, values)

    def read(self, values):
        self.log = ConfigLog(values['log'])
        self.token = values['token']
        self.vectorizer_path = values['vectorizer']
        self.encoder_chapter = values['encoder_chapter']
        self.encoder_section = values['encoder_section']
        self.encoder_paper = values['encoder_paper']
        self.model_chapter = values['model_chapter']
        self.model_section = values['model_section']
        self.model_paper = values['model_paper']


class ConfigLog:
    def __init__(self, values):
        super().__init__()
        self.read(values)

    def read(self, values):
        self.filename = values['filename']
        self.format = values.get('format', '%(asctime)s (%(name)s/%(threadName)s) [%(levelname)s]: %(message)s')
        self.datefmt = values.get('datefmt', '%Y-%m-%d %H:%M:%S')
        self.level = values.get('level', 'INFO')

    def to_dict(self):
        res = {}
        for name, obj in self.__dict__.items():
            res[name] = obj
        return res
