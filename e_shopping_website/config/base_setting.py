# -*- coding: utf-8 -*-
import json
import os


class InvalidConfigError(ValueError):
    """Raised if an invalid configuration is encountered."""

    def __init__(self, msg):
        super(InvalidConfigError, self).__init__(msg)


class BaseConfig:
    def __init__(self, filename, default_filename, default_setting):
        if not filename:
            if os.path.isfile(default_filename):
                filename = default_filename
            else:
                raise InvalidConfigError("Wrong config path")

        self.override(self.__dict__, default_setting)
        self.filename = filename
        self.load_file_config(filename)
        for key, value in self.items():
            setattr(self, key, value)

        return filename

    def load_file_config(self, filename):
        if filename is not None:
            try:
                with open(filename, encoding="utf-8") as fp:
                    fileconfig = json.load(fp)
            except ValueError as e:
                raise InvalidConfigError(
                    "Failed to read configuration file '{}'. Error: {}".format(
                        filename, e
                    )
                )
            self.override(self.__dict__, fileconfig)

        for key, value in self.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __getstate__(self):
        return self.as_dict()

    def items(self):
        return list(self.__dict__.items())

    def as_dict(self):
        return dict(list(self.items()))

    def override(self, cur_dict, config):
        for key, value in config.items():

            # new-config is dictionary
            if isinstance(value, dict) and len(value.keys()) != 0:
                if key in cur_dict:
                    if cur_dict[key] is None:
                        cur_dict[key] = value
                    else:
                        self.override(cur_dict[key], value)
                else:
                    cur_dict[key] = value
            else:
                cur_dict[key] = value

    def dump(self):
        output = dict(self.as_dict())
        json_str = json.dumps(output)

        return json_str

    def no_required_dump(self):
        output = dict(self.as_dict())
        if "required_field" in output:
            del output["required_field"]
        json_str = json.dumps(output, ensure_ascii=False, indent=4)

        return json_str

    def update(self, config_dict):
        for key, value in config_dict.items():
            self.__dict__[key] = value
