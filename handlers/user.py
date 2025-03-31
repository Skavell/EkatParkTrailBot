from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart

from config import load_config
from keyboards.inline import (
    main_menu_kb,
    back_to_main_kb, contacts_kb
)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    config = load_config()
    photo = FSInputFile(config.content.main_menu.photo)
    await message.answer_photo(
        photo=photo,
        caption=config.content.main_menu.caption,
        reply_markup=main_menu_kb()
    )


@router.callback_query(F.data == "about_park_trail")
async def about_park_trail(callback: CallbackQuery):
    """Информация о парковой тропе"""
    config = load_config()
    media = InputMediaPhoto(
        media=FSInputFile(config.content.park_trail.photo),
        caption=config.content.park_trail.caption
    )
    await callback.message.edit_media(
        media=media,
        reply_markup=back_to_main_kb("park_trail", config.content.park_trail.url)
    )
    await callback.answer()


@router.callback_query(F.data == "about_mountain")
async def about_mountain(callback: CallbackQuery):
    """Информация о горном и юго-западном маршрутах"""
    config = load_config()

    media = InputMediaPhoto(
        media=FSInputFile(config.content.mountain_trail.photo),
        caption=config.content.mountain_trail.caption
    )

    await callback.message.edit_media(
        media=media,
        reply_markup=back_to_main_kb("mountain", config.content.mountain_trail.url)
    )
    await callback.answer()


@router.callback_query(F.data == "about_southwest")
async def about_southwest(callback: CallbackQuery):
    """Информация о горном и юго-западном маршрутах"""
    config = load_config()

    media = InputMediaPhoto(
        media=FSInputFile(config.content.southwest_trail.photo),
        caption=config.content.southwest_trail.caption
    )

    await callback.message.edit_media(
        media=media,
        reply_markup=back_to_main_kb("southwest", config.content.southwest_trail.url)
    )
    await callback.answer()


@router.callback_query(F.data == "show_contacts")
async def show_contacts(callback: CallbackQuery):
    """Показать контакты организаторов"""
    config = load_config()

    media = InputMediaPhoto(
        media=FSInputFile(config.content.contacts.photo),
        caption=config.content.contacts.caption
    )
    await callback.message.edit_media(
        media=media,
        reply_markup=contacts_kb(config.content.contacts.site, config.content.contacts.vk, config.content.contacts.tg)
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    """Возврат в главное меню"""
    config = load_config()
    media = InputMediaPhoto(
        media=FSInputFile(config.content.main_menu.photo),
        caption=config.content.main_menu.caption
    )
    await callback.message.edit_media(
        media=media,
        reply_markup=main_menu_kb()
    )
    await callback.answer()
