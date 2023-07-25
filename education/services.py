import stripe

stripe.api_key = "sk_test_51NXm18JkCiZgdkS3bUMwFIRAGZ2NgCH0mn3tGMKeVd9kkDP9qD10HP1AgHAACLNJikkt6ZJGd6AWYA4WfNX72GPm00BMHDqRS8"

# Создание платежа
intent = stripe.PaymentIntent.create(
    amount=1000,  # Сумма платежа в копейках
    currency="usd",  # Валюта платежа
    payment_method_types=["card"],  # Типы платежных методов
)

# Получение информации о платеже
intent = stripe.PaymentIntent.retrieve(intent.id)

# Вывод информации о платеже
print(intent.stripe_id)
