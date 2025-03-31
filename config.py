import yaml
from pydantic import BaseModel, Field


class BotConfig(BaseModel):
    token: str
    admin_ids: list[int] = Field(default_factory=list)


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


def update_nested_config(config: Config, path: str, new_value: str | int | list | dict) -> Config:
    """
    Обновляет вложенное поле в конфиге по пути типа 'content.contacts.vk'.

    Пример:
        update_nested_config(config, "content.contacts.vk", "https://new-vk-link")
    """
    parts = path.split('.')
    current = config

    # Идём по пути, кроме последней части
    for part in parts[:-1]:
        current = getattr(current, part)

    # Устанавливаем новое значение в последний атрибут
    setattr(current, parts[-1], new_value)

    return config


def update_config_field(path: str, new_value: str | int | list | dict, config_path: str = "assets/config.yaml"):
    """Обновляет поле в конфиге и сразу сохраняет его в файл."""
    config = load_config(config_path)
    updated_config = update_nested_config(config, path, new_value)
    save_config(updated_config, config_path)


def update_config(update_path: str, new_value: BaseModel, config_path: str = "assets/config.yaml"):
    """
    Обновляет конкретную часть конфига по указанному пути.

    :param update_path: Путь к обновляемому полю в формате 'parent.child' (например, 'content.contacts')
    :param new_value: Новое значение (должно быть экземпляром соответствующей Pydantic модели)
    :param config_path: Путь к файлу конфигурации
    """
    try:
        # Загружаем текущий конфиг
        config = load_config(config_path)

        # Разбиваем путь на компоненты
        path_parts = update_path.split('.')
        current = config

        # Идем по пути до предпоследнего элемента
        for part in path_parts[:-1]:
            current = getattr(current, part)

        # Устанавливаем новое значение для последнего элемента пути
        setattr(current, path_parts[-1], new_value)

        # Сохраняем обновленный конфиг
        save_config(config, config_path)
    except Exception as e:
        raise RuntimeError(f"Ошибка обновления конфига: {e}")
