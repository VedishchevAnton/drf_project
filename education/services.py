# import stripe
#
#
# # Создание платежа
# intent = stripe.PaymentIntent.create(
#     amount=1000,  # Сумма платежа в копейках
#     currency="usd",  # Валюта платежа
#     payment_method_types=["card"],  # Типы платежных методов
# )
#
# # Получение информации о платеже
# intent = stripe.PaymentIntent.retrieve(intent.id) # pi_3NXr1mJkCiZgdkS304zBF8Ug
#
# # Вывод информации о платеже
# print(intent)
