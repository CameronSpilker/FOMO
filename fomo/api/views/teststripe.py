from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_API_SECRET

stripe.Charge.create(
  amount=2000,
  currency="usd",
  source="tok_19zWFrJqPUgxJRQzMFwXT35J", # obtained with Stripe.js
  metadata={'order_id': '6735'}
)