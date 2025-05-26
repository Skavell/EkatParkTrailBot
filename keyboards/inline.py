from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from config import load_config


def main_menu_kb():
    """Создание клавиатуры главного меню"""
    config = load_config()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="О Парковой тропе", callback_data="about_park_trail"))
    builder.row(
        InlineKeyboardButton(text="О маршруте Горный", callback_data="about_mountain"),
        InlineKeyboardButton(text="О маршруте Юго-западный", callback_data="about_southwest")
    )
    builder.row(
        InlineKeyboardButton(text="Перейти на карту", url=config.content.main_menu.url),
        InlineKeyboardButton(text="Контакты организаторов", callback_data="show_contacts")
    )
    return builder.as_markup()


def contacts_kb(site, vk, tg):
    """Создание клавиатуры для контактов организаторов"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Группа Вконтакте", url=vk))
    builder.row(InlineKeyboardButton(text="Канал Телеграм", url=tg))
    builder.row(InlineKeyboardButton(text="Сайт", url=site))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main"))
    return builder.as_markup()


def back_to_main_kb(route_type=None, map_url=None):
    """Создание кнопки "Назад" с возможностью перехода на карту"""
    builder = InlineKeyboardBuilder()
    if route_type and map_url:
        if route_type == "park_trail":
            builder.add(InlineKeyboardButton(text="Сайт", url=map_url))
        else:
            builder.add(InlineKeyboardButton(text="Перейти на карту", url=map_url))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main"))
    return builder.as_markup()
