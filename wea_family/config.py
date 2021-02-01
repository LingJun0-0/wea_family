import os
import sys

import yaml


def _bool(var: str, default=False):
    if var is None:
        return default
    var = var.upper()
    if var in ('TRUE', 'ON', 'YES', 'Y'):
        return True
    elif var in ('FALSE', 'OFF', 'NO', 'N'):
        return False
    print(
        f"unsupported bool value from var {var}, chose 'on' or 'off'.", file=sys.stderr, flush=True
    )
    return sys.exit(1)


def set_config_from_env(cfg, env, fmt):
    var = os.getenv(env, None)
    if var is None:
        return
    cfg[env] = fmt(var)


def _load_config():
    conf = {}
    env_config_file = os.getenv('WEBANK_API_CONFIG') or os.getenv('WEBANK_API_CONF')
    if not env_config_file:
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'etc', 'config.yaml'), 'rt') as f:
            conf = yaml.safe_load(f)
        return conf

    with open(env_config_file, 'rt') as f:
        user_conf = yaml.safe_load(f)

    user_conf['WEBANK_API_CONFIG'] = env_config_file
    conf.update(user_conf)

    set_config_from_env(conf, 'WEBANK_DEBUG', _bool)
    set_config_from_env(conf, 'WEBANK_API_CONFIG', str)
    return conf


def get_config():
    global __NEED_LOAD
    if __NEED_LOAD:
        config.update(_load_config())
    return config


class Config(dict):

    @property
    def debug_enabled(self):
        return self.get('WEBANK_DEBUG', False)

    @property
    def config_file(self):
        return self.get('WEBANK_API_CONFIG')


config = Config()
__NEED_LOAD = True
