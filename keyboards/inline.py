from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="О Парковой тропе", callback_data="about_park_trail"),
        InlineKeyboardButton(text="О маршруте Горный + Юго-западный", callback_data="about_mountain_southwest")
    )
    builder.row(
        InlineKeyboardButton(text="Перейти на карту", url="https://example.com/maps"),
        InlineKeyboardButton(text="Контакты организаторов", callback_data="show_contacts")
    )
    return builder.as_markup()


def back_to_main_kb(route_type=None, map_url=None):
    builder = InlineKeyboardBuilder()
    if route_type and map_url:
        builder.add(InlineKeyboardButton(text="Перейти на карту", url=map_url))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="back_to_main"))
    return builder.as_markup()


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
    return builder.as_markup()


def edit_content_kb(links=False):
    builder = InlineKeyboardBuilder()
    if links:
        builder.add(
            InlineKeyboardButton(text="Парковая тропа", callback_data="edit_link_park_trail"),
            InlineKeyboardButton(text="Горный маршрут", callback_data="edit_link_mountain_trail"),
            InlineKeyboardButton(text="Юго-западный", callback_data="edit_link_southwest_trail"),
            InlineKeyboardButton(text="Основная карта", callback_data="edit_link_main_map")
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
        InlineKeyboardButton(text="Юго-западный", callback_data="edit_photo_southwest_trail")
    )
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back"))
    return builder.as_markup()


def back_to_admin_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back"))
    return builder.as_markup()
