from pathlib import Path
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import load_config, update_config_field, save_config
from keyboards.inline import (
    admin_menu_kb,
    edit_content_kb,
    edit_photos_kb,
    back_to_admin_kb, edit_contacts_kb
)

router = Router()
config_path = Path("assets/config.yaml")


class EditTextStates(StatesGroup):
    waiting_for_section = State()
    waiting_for_text = State()


class EditPhotoStates(StatesGroup):
    waiting_for_section = State()
    waiting_for_photo = State()


class EditLinkStates(StatesGroup):
    waiting_for_section = State()
    waiting_for_link = State()


class EditContactsStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_site = State()
    waiting_for_vk = State()
    waiting_for_tg = State()
    waiting_for_caption = State()


class AdminStates(StatesGroup):
    waiting_for_id = State()


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Обработчик команды /admin"""
    config = load_config()
    if message.from_user.id not in config.bot.admin_ids:
        return await message.answer("❌ У вас нет прав администратора.")

    await message.answer(
        "👨‍💻 Админ-панель:",
        reply_markup=admin_menu_kb()
    )


@router.callback_query(F.data == "admin_back")
async def back_to_admin(callback: CallbackQuery, state: FSMContext):
    """Возврат в админ-меню"""
    await callback.message.edit_text(
        "👨‍💻 Админ-панель:",
        reply_markup=admin_menu_kb()
    )
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "admin_add")
async def add_admin(callback: CallbackQuery, state: FSMContext):
    config = load_config()
    await callback.message.edit_text(
        f"""
        👤 Список администраторов: {config.bot.admin_ids}
        Введите ID пользователя, которого хотите добавить в администраторы:
        """,
        reply_markup=back_to_admin_kb()
    )
    await state.set_state(AdminStates.waiting_for_id)
    await callback.answer()


@router.message(AdminStates.waiting_for_id)
async def add_admin_id(message: Message, state: FSMContext):
    user_id = int(message.text)
    config = load_config()
    config.bot.admin_ids.append(user_id)
    save_config(config)
    await message.answer(
        f"✅ Пользователь с ID {user_id} добавлен в администраторы!",
        reply_markup=admin_menu_kb()
    )
    await state.clear()


# --- Редактирование текста ---
@router.callback_query(F.data == "edit_content")
async def edit_content(callback: CallbackQuery, state: FSMContext):
    """Выбор раздела для редактирования текста"""
    await callback.message.edit_text(
        "📝 Выберите раздел для редактирования текста:",
        reply_markup=edit_content_kb()
    )
    await state.set_state(EditTextStates.waiting_for_section)
    await callback.answer()


@router.callback_query(EditTextStates.waiting_for_section)
async def select_section_for_edit(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора раздела"""
    section = callback.data.replace("edit_text_", "")
    await state.update_data(section=section)
    await callback.message.edit_text(
        f"✏️ Введите новый текст для раздела '{section}':",
        reply_markup=back_to_admin_kb()
    )
    await state.set_state(EditTextStates.waiting_for_text)
    await callback.answer()


@router.message(EditTextStates.waiting_for_text)
async def save_new_text(message: Message, state: FSMContext):
    """Сохранение нового текста"""
    data = await state.get_data()
    section = data["section"]
    new_text = message.text

    # Обновляем конфиг
    update_config_field(f"content.{section}.caption", new_text)

    await message.answer(
        f"✅ Текст раздела '{section}' успешно обновлён!",
        reply_markup=admin_menu_kb()
    )
    await state.clear()


# --- Редактирование фото ---
@router.callback_query(F.data == "edit_photos")
async def edit_photos(callback: CallbackQuery, state: FSMContext):
    """Выбор раздела для замены фото"""
    await callback.message.edit_text(
        "🖼 Выберите раздел для замены фотографии:",
        reply_markup=edit_photos_kb()
    )
    await state.set_state(EditPhotoStates.waiting_for_section)
    await callback.answer()


@router.callback_query(EditPhotoStates.waiting_for_section)
async def select_section_for_photo(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора раздела для фото"""
    section = callback.data.replace("edit_photo_", "")
    await state.update_data(section=section)
    await callback.message.edit_text(
        f"📤 Отправьте новое фото для раздела '{section}':",
        reply_markup=back_to_admin_kb()
    )
    await state.set_state(EditPhotoStates.waiting_for_photo)
    await callback.answer()


@router.message(EditPhotoStates.waiting_for_photo, F.photo)
async def save_new_photo(message: Message, state: FSMContext, bot: Bot):
    """Сохранение нового фото"""
    data = await state.get_data()
    section = data["section"]

    # Скачиваем фото
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = f"assets/images/{section}.jpg"

    await bot.download_file(file.file_path, file_path)

    await message.answer(
        f"✅ Фото для раздела '{section}' успешно обновлено!",
        reply_markup=admin_menu_kb()
    )
    await state.clear()


# --- Редактирование ссылок ---
@router.callback_query(F.data == "edit_links")
async def edit_links(callback: CallbackQuery, state: FSMContext):
    """Выбор раздела для редактирования ссылки"""
    await callback.message.edit_text(
        "🔗 Выберите раздел для редактирования ссылки:",
        reply_markup=edit_content_kb(links=True)
    )
    await state.set_state(EditLinkStates.waiting_for_section)
    await callback.answer()


@router.callback_query(EditLinkStates.waiting_for_section)
async def select_section_for_link(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора раздела для ссылки"""
    section = callback.data.replace("edit_link_", "")
    await state.update_data(section=section)
    await callback.message.edit_text(
        f"✏️ Введите новую ссылку для раздела '{section}':",
        reply_markup=back_to_admin_kb()
    )
    await state.set_state(EditLinkStates.waiting_for_link)
    await callback.answer()


@router.message(EditLinkStates.waiting_for_link)
async def save_new_link(message: Message, state: FSMContext):
    """Сохранение новой ссылки"""
    data = await state.get_data()
    section = data["section"]
    new_link = message.text

    update_config_field(f"content.{section}.url", new_link)

    await message.answer(
        f"✅ Ссылка для раздела '{section}' успешно обновлена!",
        reply_markup=admin_menu_kb()
    )
    await state.clear()


# --- Редактирование контактов ---
@router.callback_query(F.data == "edit_contacts")
async def edit_contacts_menu(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        "📇 Выберите что хотите изменить:",
        reply_markup=edit_contacts_kb()
    )
    await callback.answer()


# Обработчики для каждого поля
@router.callback_query(F.data == "edit_contacts_photo")
async def edit_contacts_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📤 Отправьте новое фото для контактов:",
        reply_markup=back_to_admin_kb()
    )
    await state.set_state(EditContactsStates.waiting_for_photo)
    await callback.answer()


@router.message(EditContactsStates.waiting_for_photo, F.photo)
async def save_contacts_photo(message: Message, state: FSMContext, bot: Bot):
    config = load_config()
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = config.content.contacts.photo

    await bot.download_file(file.file_path, file_path)

    await message.answer("✅ Фото контактов обновлено!", reply_markup=admin_menu_kb())
    await state.clear()


@router.callback_query(F.data == "edit_contacts_site")
async def edit_contacts_site(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🌐 Введите новую ссылку на сайт:",
        reply_markup=back_to_admin_kb()
    )
    await state.set_state(EditContactsStates.waiting_for_site)
    await callback.answer()


@router.message(EditContactsStates.waiting_for_site)
async def save_contacts_site(message: Message, state: FSMContext):

    update_config_field(f"content.contacts.site", message.text)

    await message.answer("✅ Ссылка на сайт обновлена!", reply_markup=admin_menu_kb())
    await state.clear()


# Аналогичные обработчики для vk, tg и caption
@router.callback_query(F.data == "edit_contacts_vk")
async def edit_contacts_vk(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🔵 Введите новую ссылку VK:",
        reply_markup=back_to_admin_kb()
    )
    await state.set_state(EditContactsStates.waiting_for_vk)
    await callback.answer()


@router.message(EditContactsStates.waiting_for_vk)
async def save_contacts_vk(message: Message, state: FSMContext):

    update_config_field(f"content.contacts.vk", message.text)

    await message.answer("✅ Ссылка VK обновлена!", reply_markup=admin_menu_kb())
    await state.clear()


@router.callback_query(F.data == "edit_contacts_tg")
async def edit_contacts_tg(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📢 Введите новую ссылку Telegram:",
        reply_markup=back_to_admin_kb()
    )
    await state.set_state(EditContactsStates.waiting_for_tg)
    await callback.answer()


@router.message(EditContactsStates.waiting_for_tg)
async def save_contacts_tg(message: Message, state: FSMContext):

    update_config_field(f"content.contacts.tg", message.text)

    await message.answer("✅ Ссылка Telegram обновлена!", reply_markup=admin_menu_kb())
    await state.clear()


@router.callback_query(F.data == "edit_contacts_caption")
async def edit_contacts_caption(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📝 Введите новый заголовок:",
        reply_markup=back_to_admin_kb()
    )
    await state.set_state(EditContactsStates.waiting_for_caption)
    await callback.answer()


@router.message(EditContactsStates.waiting_for_caption)
async def save_contacts_caption(message: Message, state: FSMContext):

    update_config_field(f"content.contacts.caption", message.text)

    await message.answer("✅ Заголовок контактов обновлен!", reply_markup=admin_menu_kb())
    await state.clear()

'''
@router.callback_query(F.data == "edit_contacts")
async def edit_contacts(callback: CallbackQuery, state: FSMContext):
    """Редактирование контактов"""
    await callback.message.edit_text(
        "📇 Введите новые контактные данные:",
        reply_markup=back_to_admin_kb()
    )
    await state.set_state(EditContactsStates.waiting_for_contacts)
    await callback.answer()


@router.message(EditContactsStates.waiting_for_contacts)
async def save_new_contacts(message: Message, state: FSMContext):
    """Сохранение новых контактов"""
    new_contacts = message.text

    # Обновляем конфиг
    new_contacts_item = ContactsItem(text=new_contacts)
    update_config("content.contacts", new_contacts_item)

    await message.answer(
        "✅ Контактные данные успешно обновлены!",
        reply_markup=admin_menu_kb()
    )
    await state.clear()
'''
