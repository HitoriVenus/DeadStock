from .loader import ConfigNode, load_config

cfg: ConfigNode | None = None

def initialize(
    env_path: str = ".env",
    json_path: str = "config.json",
):
    global cfg

    if cfg is not None:
        raise RuntimeError("Configuration has already been initialized.")

    cfg = load_config(
        env_path=env_path,
        json_path=json_path,
    )

    return cfg