from dotenv import load_dotenv
from dynaconf import Dynaconf, Validator

load_dotenv()

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml']
)

settings.validators.register(
    Validator("models__api_key", must_exist=True),
    Validator("models__api_base", must_exist=True),
    Validator("models__api_version", must_exist=True)
)

# `envvar_prefix` = export envvars with `export CONF_FOO=bar`.
# `settings_files` = Load these files in the order.
