from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart

from config import load_config
from keyboards.inline import (
    main_menu_kb,
    back_to_main_kb
)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    config = load_config()
    photo = FSInputFile(config.content.main_menu.photo)

    # Удаляем предыдущее сообщение с меню, если оно есть
    await message.bot.delete_message(message.chat.id, message.message_id - 1)

    await message.answer_photo(
        photo=photo,
        caption=config.content.main_menu.caption,
        reply_markup=main_menu_kb()
    )


@router.callback_query(F.data == "about_park_trail")
async def about_park_trail(callback: CallbackQuery):
    """Информация о парковой тропе"""
    config = load_config()
    photo = FSInputFile(config.content.park_trail.photo)

    await callback.message.answer_photo(
        photo=photo,

        caption=config.content.park_trail.caption,
        reply_markup=back_to_main_kb("park_trail", config.content.park_trail.map_url)
    )
    await callback.answer()


@router.callback_query(F.data == "about_mountain_southwest")
async def about_mountain_southwest(callback: CallbackQuery):
    """Информация о горном и юго-западном маршрутах"""
    config = load_config()
    photo = FSInputFile(config.content.mountain_trail.photo)

    # Можно объединить информацию о двух маршрутах
    caption = (
        f"{config.content.mountain_trail.caption}\n\n"
        f"{config.content.southwest_trail.caption}"
    )

    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=back_to_main_kb(
            "mountain_southwest",
            config.content.mountain_trail.map_url
        )
    )
    await callback.answer()


@router.callback_query(F.data == "show_contacts")
async def show_contacts(callback: CallbackQuery):
    """Показать контакты организаторов"""
    config = load_config()
    await callback.message.answer(
        text=config.content.contacts.text,
        reply_markup=back_to_main_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    """Возврат в главное меню"""
    config = load_config()
    photo = FSInputFile(config.content.main_menu.photo)

    await callback.message.answer_photo(
        photo=photo,
        caption=config.content.main_menu.caption,
        reply_markup=main_menu_kb()
    )
    await callback.answer()
