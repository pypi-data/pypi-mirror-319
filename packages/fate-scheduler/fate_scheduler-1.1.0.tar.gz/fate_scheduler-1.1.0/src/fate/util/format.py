"""Configurable support for serialization formats."""
import bz2
import collections
import csv
import gzip
import io
import json
import lzma
import tarfile
import typing
from functools import partial

import toml
import yaml
from descriptors import classproperty

from fate.util.datastructure import CallableEnum, FileFormatEnum


class ConfigurableYamlLoader(yaml.SafeLoader):
    """YAML SafeLoader supporting alternate collection classes.

    Mapping objects default to the built-in `dict`. Sequences to the
    built-in `list`. Alternate constructors may be specified upon
    initialization of the loader.

    Note: To use with the default interface, `yaml.load()`, a `partial`
    must be constructed, for example:

        yaml.load(stream, functools.partial(ConfigurableYamlLoader,
                                            dict_=NewDict))

    """
    def __init__(self, stream, dict_=None, list_=None):
        super().__init__(stream)
        self.dict_ = dict_
        self.list_ = list_

    def construct_yaml_seq(self, node):
        data = [] if self.list_ is None else self.list_()
        yield data
        data.extend(self.construct_sequence(node))

    def construct_yaml_map(self, node):
        data = {} if self.dict_ is None else self.dict_()
        yield data
        value = self.construct_mapping(node)
        data.update(value)


ConfigurableYamlLoader.add_constructor('tag:yaml.org,2002:seq',
                                       ConfigurableYamlLoader.construct_yaml_seq)

ConfigurableYamlLoader.add_constructor('tag:yaml.org,2002:map',
                                       ConfigurableYamlLoader.construct_yaml_map)


class ConfigurableTomlDecoder(toml.TomlDecoder):

    def __init__(self, _dict=dict, _list=list):
        super().__init__(_dict=_dict)
        self._list = _list

    def load_array(self, a):
        result = super().load_array(a)
        return result if type(result) == self._list else self._list(result)


class JSONEncoder(json.JSONEncoder):
    """JSON encoder supporting abstract Sequence and Mapping objects."""

    def default(self, obj):
        if isinstance(obj, collections.abc.Mapping):
            return dict(obj)

        if isinstance(obj, collections.abc.Sequence):
            return tuple(obj)

        # let base class raise TypeError
        return super().default(obj)

json_encoder = JSONEncoder()


class tag:
    """configurable decorator to set given attribute to given value"""

    _undefined_ = object()

    def __init__(self, name, value=_undefined_):
        self.name = name
        self.value = value

    def __call__(self, value_or_target):
        if self.value is self._undefined_:
            return self.__class__(self.name, value_or_target)

        setattr(value_or_target, self.name, self.value)
        return value_or_target

    def __repr__(self):
        value = 'Undefined' if self.value is self._undefined_ else repr(self.value)
        return f"{self.__class__.__name__}({self.name!r}, {value})"


raises = tag('raises')

auto = tag('auto', True)

binary = tag('binary', True)


class _NameList:

    @classproperty
    def __names__(cls):
        return [member.name for member in cls]


class _Raises:

    @property
    def raises(self):
        return getattr(self.value, 'raises', ())


class Decoder(typing.NamedTuple):

    loader: typing.Callable[[typing.Union[str, bytes]], typing.Any]
    binary: bool
    raises: typing.Tuple[Exception]
    suffix: str

    def __call__(self, value: typing.Union[str, bytes], *args, **kwargs):
        return self.loader(value, *args, **kwargs)


class Decoding(typing.NamedTuple):

    decoded: typing.Any
    decoder: Decoder


def taropen(binary: bytes) -> tarfile.TarFile:
    return tarfile.open(fileobj=io.BytesIO(binary))


class SLoader(_NameList, _Raises, FileFormatEnum, CallableEnum):

    @CallableEnum.member
    @raises(csv.Error)
    def csv(text):
        return list(csv.reader(text.splitlines()))

    @CallableEnum.member
    @auto
    @raises(json.decoder.JSONDecodeError)
    def json(text, dict_=None):
        if dict_ is None:
            return json.loads(text)

        return json.loads(text, object_hook=dict_)

    @CallableEnum.membermethod
    @auto
    @binary
    @raises(tarfile.TarError)
    def tar(self, binary):
        archive = taropen(binary)

        if isinstance(archive.fileobj, gzip.GzipFile):
            suffix = '.tar.gz'
        elif isinstance(archive.fileobj, bz2.BZ2File):
            suffix = '.tar.bz2'
        elif isinstance(archive.fileobj, lzma.LZMAFile):
            suffix = '.tar.xz'
        else:
            suffix = self.suffix

        decoder = self.decoder._replace(loader=taropen, suffix=suffix)

        return self.Decoding(archive, decoder)

    @CallableEnum.member
    @auto
    @raises(toml.decoder.TomlDecodeError)
    def toml(text, **types):
        switched = {f'_{name}'.rstrip('_'): value for (name, value) in types.items()}
        decoder = ConfigurableTomlDecoder(**switched)
        return toml.loads(text, decoder=decoder)

    @CallableEnum.member
    @auto
    @raises(yaml.error.YAMLError)
    def yaml(text, **types):
        conf = yaml.load(text, partial(ConfigurableYamlLoader, **types))
        return {} if conf is None else conf

    @classproperty
    def __deserializers__(cls):
        return [member.name for member in cls if not member.binary]

    @classproperty
    def __auto__(cls):
        return [member for member in cls if member.auto]

    __abstract_formats__ = ('auto', 'mixed')

    @classproperty
    def __formats__(cls):
        return [*cls.__abstract_formats__, *cls.__members__]

    @property
    def auto(self):
        return getattr(self.value, 'auto', False)

    @property
    def binary(self):
        return getattr(self.value, 'binary', False)

    @property
    def decoder(self):
        return self.Decoder(loader=self, binary=self.binary,
                            raises=self.raises, suffix=self.suffix)

    @classmethod
    def autoload(cls, content: typing.Union[str, bytes], format_, **types):
        if not format_:
            return (None, None)

        if isinstance(format_, str) or not isinstance(format_, collections.abc.Iterable):
            formats = {format_}
        else:
            formats = set(format_)

        if formats & {'auto', 'mixed'}:
            if not content:
                return (None, None)

            if isinstance(content, str):
                (binary, text) = (None, content)
            else:
                binary = content

                try:
                    text = binary.decode()
                except UnicodeDecodeError:
                    text = None

            for loader in cls.__auto__:
                encoded = binary if loader.binary else text

                if encoded is None:
                    continue

                try:
                    decoding = loader(encoded, **types)
                except loader.raises:
                    pass
                else:
                    if isinstance(decoding, cls.Decoding):
                        (result, loader) = decoding
                    else:
                        result = decoding

                    # yaml.load treats a string literal as a valid document;
                    # however, this is probably not what's wanted.
                    if not isinstance(result, str):
                        return (result, loader)
            else:
                return (None, None)

        raise cls.NonAutoError(format_)


class NonAutoError(ValueError):
    pass


SLoader.NonAutoError = NonAutoError
SLoader.Decoding = Decoding
SLoader.Decoder = Decoder


class Loader(_Raises, FileFormatEnum, CallableEnum):

    @CallableEnum.member
    @raises(toml.decoder.TomlDecodeError)
    def toml(path, **types):
        with open(path) as fd:
            return SLoader.toml(fd.read(), **types)

    @CallableEnum.member
    @raises(yaml.error.YAMLError)
    def yaml(path, **types):
        with open(path) as fd:
            return SLoader.yaml(fd, **types)


class Dumper(_NameList, CallableEnum):

    @CallableEnum.member
    def json(obj):
        return json_encoder.encode(obj)

    @CallableEnum.member
    def toml(obj):
        return toml.dumps(obj)

    @CallableEnum.member
    def yaml(obj):
        return yaml.dump(obj)
