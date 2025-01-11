
from nwebclient import web as w


class Param:
    func = None
    name: str
    type: str
    description: str
    is_pos: bool
    default_value = None

    def __init__(self, name: str, datatype: str = 'str', is_pos: bool = True):
        self.name = name
        self.type = datatype
        self.is_pos = is_pos

    def desc(self, val):
        self.description = val
        return self

    def default(self, val):
        self.default_value = val
        return self

    def to_html(self):
        return self.name + f': <span style="color: #ccc;">{self.type}</span> '

    def to_openapi(self):
        """ https://swagger.io/docs/specification/v3_0/describing-parameters/
        in: path|query
          name: userId
          schema:
            type: integer
          required: true
          description: Numeric ID of the user to get

        requestBody:
        description: Optional description in *Markdown*
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Pet"
          application/x-www-form-urlencoded:
            schema:
              $ref: "#/components/schemas/PetForm"
        """
        return {
            'name': self.name,
            'in': 'query',
            'schema': {
                'type': self.type
            },
            'required': self.default_value is None,
            'description': self.description
        }


class Func:
    lang: str
    name: str
    description: str
    params: list[Param]
    defined_in: str

    def __init__(self, name: str = '', description: str = '', defined_in: str = '', *params):
        self.lang = 'py'
        if isinstance(name, Param):
            params = [name, *params]
        else:
            self.name = name
        if isinstance(description, Param):
            params = [description, *params]
        else:
            self.description = description
        if isinstance(defined_in, Param):
            params = [defined_in, *params]
        else:
            self.defined_in = defined_in
        self.params = params
        for param in self.params:
            param.func = self

    def for_py(self):
        ps = ','.join(map(lambda p: p.to_html(), self.params))
        s = f'{self.name} ({ps})'
        return s

    def for_esp(self):
        ps = ' '.join(map(lambda p: p.to_html(), self.params))
        s = f'{self.name} {ps}'
        return s

    def for_npy(self):
        ps = ' '.join(map(lambda p: p.to_html(), self.params))
        s = f'{self.name} {ps}'
        return s

    def to_html(self):
        lng = getattr(self, 'for_' + self.lang, self.for_py)
        s = lng()
        s += f'<br />{self.description}'
        return w.div(s, _class='Func', style='border: 1px #444 solid; padding: 5px; margin: 5px;')

    def to_openapi_properties(self):
        """ https://swagger.io/docs/specification/v3_0/components/ """
        res = {}
        for p in self.params:
            pass

    def to_openapi_params(self):
        pass


class Package:

    lang: str = 'py'

    def __init__(self, lang='py', *items):
        """
        :param lang: [py, esp, npy]
        """
        self.lang = lang
        self.items = list(items)
        for itm in self.items:
            itm.lang = lang

    def __iter__(self):
        return self.items.__iter__()

    def __len__(self):
        return len(self.items)

    def append(self, item):
        item.lang = self.lang
        self.items.append(item)

    def to_html(self):
        s = ''
        for item in self.items:
            s += item.to_html()
        return w.div(s, _class='Package')
