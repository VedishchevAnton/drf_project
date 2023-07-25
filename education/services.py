import stripe  # импорт библиотеки Stripe

from datetime import datetime, timedelta  # импорт модулей datetime и timedelta

from education.models import Payments

# Установка ключа API Stripe
stripe.api_key = "pk_test_51NXm18JkCiZgdkS3oaayzptg1BOAlOJG39pgaC" \
                         "4i9dtwJPNciNcmnU4lNXBwWT8tjTwlRUp0fOOH4mO5t4vyO7GK00XoQEVRf9"


def check_payment_status():
    """Метод получения списка платежей для проверки"""
    payments = Payments.objects.filter(status__in=['requires_payment_method', 'requires_confirmation'])

    # Проверка статуса каждого платежа
    for payment in payments:
        payment_intent = stripe.PaymentIntent.retrieve(payment.payment_intent_id)
        if payment_intent.status == 'succeeded':
            payment.status = 'succeeded'
            payment.payment_date = datetime.now()
            payment.save()
        elif payment_intent.status == 'requires_payment_method':
            payment.status = 'requires_payment_method'
            payment.save()
        elif payment_intent.status == 'requires_confirmation':
            payment.status = 'requires_confirmation'
            payment.save()
        elif payment_intent.status == 'canceled':
            payment.status = 'canceled'
            payment.save()
        elif payment_intent.status == 'processing':
            # Если платеж обрабатывается более 24 часов, отменить его
            if payment.payment_date + timedelta(hours=24) < datetime.now():
                payment_intent.cancel()
                payment.status = 'canceled'
                payment.save()
