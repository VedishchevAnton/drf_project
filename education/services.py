import stripe
from drf_project.settings import STRIPE_SECRET_KEY


class PaymentService:
    def __init__(self):
        stripe.api_key = STRIPE_SECRET_KEY

    def create_payment(self, amount, currency):
        amount = amount  # сумма в центах (например, 10.00 долларов США)
        currency = currency  # валюта платежа (например, доллар США)
        payment_method_types = ["card"]  # метод оплаты (например, "card" для оплаты картой)

        try:
            # Создаем сессию чекаута
            session = stripe.checkout.Session.create(
                payment_method_types=payment_method_types,
                line_items=[{
                    "price_data": {
                        "currency": currency,
                        "unit_amount": amount,
                        "product_data": {
                            "name": "Тестовый продукт",  # Название продукта
                        },
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url="https://example.com/success",  # URL для перенаправления после успешной оплаты
            )

            # Получаем идентификатор сессии чекаута (session_id)
            session = session.url
            return session
        except stripe.error.StripeError as e:
            print(f"Error: {e}")
            return None
