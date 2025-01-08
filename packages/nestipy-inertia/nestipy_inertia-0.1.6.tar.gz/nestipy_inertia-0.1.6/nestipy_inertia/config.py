import os
from dataclasses import dataclass
from json import JSONEncoder
from typing import Literal, Type

from .utils import InertiaJsonEncoder

try:
    import httpx
except ImportError:
    httpx = None


@dataclass
class InertiaConfig:
    """
    Configuration class for Inertia
    """
    environment: Literal["development", "production"] = "development"
    version: str = "1.0"
    json_encoder: Type[JSONEncoder] = InertiaJsonEncoder
    dev_url: str = "http://localhost:5173"
    ssr_url: str = "http://localhost:13714"
    ssr_enabled: bool = False
    manifest_json_path: str = "manifest.json"
    root_dir: str = os.getcwd()
    root_template_filename: str = "index.html"
    entrypoint_filename: str = "main.tsx"
    use_flash_messages: bool = True
    use_flash_errors: bool = True
    flash_message_key: str = "messages"
    flash_error_key: str = "errors"
    assets_prefix: str = "/dist"
    build_dir: str = "dist"
    src_dir: str = "src"
