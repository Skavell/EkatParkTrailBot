import yaml
from pydantic import BaseModel


class BotConfig(BaseModel):
    token: str


class MainMenuItem(BaseModel):
    photo: str
    caption: str
    url: str


class ContactsItem(BaseModel):
    photo: str
    site: str
    vk: str
    tg: str
    caption: str


class ContentConfig(BaseModel):
    main_menu: MainMenuItem
    park_trail: MainMenuItem
    mountain_trail: MainMenuItem
    southwest_trail: MainMenuItem
    contacts: ContactsItem


class Config(BaseModel):
    bot: BotConfig
    content: ContentConfig


def load_config(path: str = "config/config.yaml") -> Config:
    """Загрузка конфигурации из YAML файла"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return Config(**data)
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки конфига: {e}")
