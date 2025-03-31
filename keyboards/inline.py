from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from config import load_config


# --- Основная часть ---
# --- Главное меню ---
def main_menu_kb():
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


# --- Меню "Контакты организаторов" ---
def contacts_kb(site, vk, tg):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Группа Вконтакте", url=vk))
    builder.row(InlineKeyboardButton(text="Канал Телеграм", url=tg))
    builder.row(InlineKeyboardButton(text="Сайт", url=site))
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_main"))
    return builder.as_markup()


# --- Допольнительные кнопки в каждом меню, по типу "назад" и перейти на карту для меню конкретных маршрутов ---
def back_to_main_kb(route_type=None, map_url=None):
    builder = InlineKeyboardBuilder()
    if route_type and map_url:
        if route_type == "park_trail":
            builder.add(InlineKeyboardButton(text="Сайт", url=map_url))
        else:
            builder.add(InlineKeyboardButton(text="Перейти на карту", url=map_url))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main"))
    return builder.as_markup()


# --- Кнопки для админского меню ---
def admin_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📝 Редактировать текст", callback_data="edit_content"),
        InlineKeyboardButton(text="🖼 Заменить фото", callback_data="edit_photos")
    )
    builder.row(
        InlineKeyboardButton(text="🔗 Изменить ссылки", callback_data="edit_links"),
        InlineKeyboardButton(text="📇 Изменить контакты", callback_data="edit_contacts")
    )
    builder.row(
        InlineKeyboardButton(text="Добавить администратора по id", callback_data="admin_add")
    )
    return builder.as_markup()


def edit_contacts_kb():
    """Меню редактирования контактов"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Изменить фото", callback_data="edit_contacts_photo"),
        InlineKeyboardButton(text="Изменить сайт", callback_data="edit_contacts_site")
    )
    builder.row(
        InlineKeyboardButton(text="Изменить VK", callback_data="edit_contacts_vk"),
        InlineKeyboardButton(text="Изменить Telegram", callback_data="edit_contacts_tg")
    )
    builder.row(
        InlineKeyboardButton(text="Изменить заголовок", callback_data="edit_contacts_caption"),
    )
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back"))
    return builder.as_markup()


def edit_content_kb(links=False):
    builder = InlineKeyboardBuilder()
    if links:
        builder.add(
            InlineKeyboardButton(text="Парковая тропа", callback_data="edit_link_park_trail"),
            InlineKeyboardButton(text="Горный маршрут", callback_data="edit_link_mountain_trail"),
            InlineKeyboardButton(text="Юго-западный", callback_data="edit_link_southwest_trail"),
            InlineKeyboardButton(text="Основная карта", callback_data="edit_link_main_menu")
        )
    else:
        builder.add(
            InlineKeyboardButton(text="Главное меню", callback_data="edit_text_main_menu"),
            InlineKeyboardButton(text="Парковая тропа", callback_data="edit_text_park_trail"),
            InlineKeyboardButton(text="Горный маршрут", callback_data="edit_text_mountain_trail"),
            InlineKeyboardButton(text="Юго-западный", callback_data="edit_text_southwest_trail"),
            InlineKeyboardButton(text="Контакты", callback_data="edit_text_contacts")
        )
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back"))
    return builder.as_markup()


def edit_photos_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Главное меню", callback_data="edit_photo_main_menu"),
        InlineKeyboardButton(text="Парковая тропа", callback_data="edit_photo_park_trail"),
        InlineKeyboardButton(text="Горный маршрут", callback_data="edit_photo_mountain_trail"),
        InlineKeyboardButton(text="Юго-западный", callback_data="edit_photo_southwest_trail"),
        InlineKeyboardButton(text="Контакты", callback_data="edit_photo_contacts")
    )
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back"))
    return builder.as_markup()


def back_to_admin_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back"))
    return builder.as_markup()
