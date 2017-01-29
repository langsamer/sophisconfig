'''
Sophisticated configuration option objects

Options and parameters can be accessed by dot notation and can be nested.
You can control if and what options can be dynamically created.

Example:

>>> c = Config()
>>> c.verbose
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: 'Config' object has no attribute 'verbose'

>>> c._create_option(name='verbose', value=False)
>>> c.verbose
False
>>> c.verbose = True
>>> c.verbose
True

>>> c._write(file)
# writes all options and parameters in c to file

Created on Jan 29, 2017

@author: malte
'''


class Config:
    def __init__(self, init_values=None, protected=False, typed=False):
        self.__dict__['_option_dict'] = {}
        self.__dict__['_section_dict'] = {}
        self.__dict__['_protected'] = protected
        self.__dict__['_typed'] = typed
        if init_values:
            self._from_dict(init_values)

    def __getattr__(self, attr):
        try:
            return self._option_dict[attr]
        except KeyError:
            try:
                return self._section_dict[attr]
            except KeyError:
                raise KeyError("No option or section named {} in this Config object".
                               format(attr))

    def __setattr__(self, attr, value):
        if attr in self._option_dict:
            typ = type(self._option_dict[attr])
            if self._typed and not isinstance(value, typ):
                raise TypeError("Value for {} must be {}".format(attr, str(typ)))
            else:
                self._option_dict[attr] = value
        elif attr not in self._section_dict:
            if self._protected:
                raise TypeError("This section is protected and you cannot create new options")
            self._create_option(attr, value)
        else:
            raise TypeError("Cannot assign to a section of a Config object")

    def _create_option(self, option, value=None):
        self._option_dict[option] = value

    def _create_section(self, section, init_values=None):
        self._section_dict[section] = Config(init_values)

    def _from_dict(self, d):
        for name, value in d.items():
            if isinstance(value, dict):
                self._section_dict[name] = Config(value)
            else:
                self._option_dict[name] = value
