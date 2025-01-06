import os
from dataclasses import dataclass, field, replace
from functools import wraps

from daggerml_cli.repo import Ref
from daggerml_cli.util import readfile, writefile


class ConfigError(RuntimeError):
    pass


def config_property(f=None, **opts):
    def inner(f):
        @wraps(f)
        def getter(self) -> str:
            if base and getattr(self, priv) is None:
                val = os.getenv(env) or readfile(self.get(base), *path)
                setattr(self, priv, val)
            result = f(self) or getattr(self, priv, None)
            if not result:
                errmsg = f'required: --{kebab} option or DML_{name} environment variable'
                errmsg = '%s or `dml %s`' % (errmsg, opts['cmd']) if opts.get('cmd') else errmsg
                raise ConfigError(errmsg)
            return result
        name = f.__name__
        priv = f'_{name}'
        env = f'DML{priv}'
        kebab = name.lower().replace('_', '-')
        base, *path = opts.get('path', [None])
        result = property(getter)
        if base:
            @result.setter
            def setter(self, value):
                if len(self._writes):
                    self._writes[-1][(self.get(base), *path)] = value
                setattr(self, priv, value)
            return setter
        return result
    return inner if f is None else inner(f)


@dataclass
class Config:
    """This class holds the global configuration options."""
    _CONFIG_DIR: str | None = None
    _PROJECT_DIR: str | None = None
    _REPO: str | None = None
    _BRANCH: str | None = None
    _USER: str | None = None
    _REPO_PATH: str | None = None
    _DEBUG: bool = False
    _writes: list = field(default_factory=list)

    def get(self, name, default=None):
        try:
            return getattr(self, name)
        except ConfigError:
            return default

    @property
    def DEBUG(self):
        return self._DEBUG

    @config_property
    def CONFIG_DIR(self):
        pass

    @config_property
    def PROJECT_DIR(self):
        pass

    @config_property(path=['PROJECT_DIR', 'repo'], cmd='project init')  # type: ignore
    def REPO(self):
        pass

    @config_property(path=['PROJECT_DIR', 'head'], cmd='branch use')  # type: ignore
    def BRANCH(self):
        pass

    @config_property(path=['CONFIG_DIR', 'config', 'user'], cmd='config set user')  # type: ignore
    def USER(self):
        pass

    @config_property
    def BRANCHREF(self):
        return Ref(f'head/{self.BRANCH}')

    @config_property
    def REPO_DIR(self):
        return os.path.join(self.CONFIG_DIR, 'repo')  # type: ignore

    @config_property
    def REPO_PATH(self):
        return os.path.join(self.REPO_DIR, self.REPO)  # type: ignore

    def replace(self, **changes):
        return replace(self, **changes)

    def __enter__(self):
        self._writes.append({})
        return self

    def __exit__(self, type, *_):
        writes = self._writes.pop()
        if type is None:
            if len(self._writes):
                return self._writes[-1].update(writes)
            [writefile(v, *k) for k, v in writes.items()]
