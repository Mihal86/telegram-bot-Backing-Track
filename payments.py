from aiogram import types
from aiogram.types import LabeledPrice, PreCheckoutQuery

# Обробка оплати
async def buy_track(message: types.Message):
    track_name = message.text.replace("Купити ", "").strip()
    price = 50 * 100  # Ціна у копійках

    await message.answer_invoice(
        title="Backing Track",
        description=f"Покупка треку: {track_name}",
        payload=track_name,
        provider_token="ТУТ_ВАШ_PAYMENT_PROVIDER_TOKEN",
        currency="UAH",
        prices=[LabeledPrice(label="Трек", amount=price)],
        start_parameter="purchase",
    )

async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

async def successful_payment(message: types.Message):
    track_name = message.successful_payment.invoice_payload
    await message.answer(f"Дякую за покупку! Ось ваш трек: 🔗 [Завантажити](https://example.com/{track_name}.mp3)")

def register_payment_handlers(dp):
    dp.register_message_handler(buy_track, lambda msg: msg.text.startswith("Купити "))
    dp.register_pre_checkout_query_handler(pre_checkout)
    dp.register_message_handler(successful_payment, content_types=types.ContentType.SUCCESSFUL_PAYMENT)
