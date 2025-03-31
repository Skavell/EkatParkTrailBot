import yaml
from pydantic import BaseModel, Field


class BotConfig(BaseModel):
    token: str
    admin_ids: list[int] = Field(default_factory=list)


class MainMenuItem(BaseModel):
    photo: str
    caption: str


class TrailItem(BaseModel):
    photo: str
    caption: str
    map_url: str


class ContactsItem(BaseModel):
    text: str


class ContentConfig(BaseModel):
    main_menu: MainMenuItem
    park_trail: TrailItem
    mountain_trail: TrailItem
    southwest_trail: TrailItem
    contacts: ContactsItem


class Config(BaseModel):
    bot: BotConfig
    content: ContentConfig


def load_config(path: str = "assets/config.yaml") -> Config:
    """Загрузка конфигурации из YAML файла"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return Config(**data)
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки конфига: {e}")


def save_config(config: Config, path: str = "assets/config.yaml"):
    """Сохранение конфигурации в YAML файл"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            # Конвертируем модель Pydantic в словарь перед сохранением
            yaml.dump(config.model_dump(), f, allow_unicode=True, sort_keys=False)
    except Exception as e:
        raise RuntimeError(f"Ошибка сохранения конфига: {e}")