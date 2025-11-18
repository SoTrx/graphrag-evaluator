from dotenv import load_dotenv
from dynaconf import Dynaconf, Validator

load_dotenv()

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml']
)

settings.validators.register(
    Validator("project__subscription_id", must_exist=True),
    Validator("project__resource_group_name", must_exist=True),
    Validator("project__project_name", must_exist=True),
    Validator("project__azure_ai_project", must_exist=True)
)

# `envvar_prefix` = export envvars with `export CONF_FOO=bar`.
# `settings_files` = Load these files in the order.
