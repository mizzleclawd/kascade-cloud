"""
Kascade Cloud - Stripe Payment Integration
"""

import stripe
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_placeholder')

PRICING = {
    'starter': {'price': 2900, 'product': 'prod_starter'},
    'pro': {'price': 7900, 'product': 'prod_pro'},
    'enterprise': {'price': 19900, 'product': 'prod_enterprise'}
}

def create_checkout_session(customer_email, plan, success_url, cancel_url):
    """Create Stripe checkout session"""
    price = PRICING.get(plan, PRICING['pro'])
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'Kascade Cloud - {plan.title()} Plan',
                },
                'unit_amount': price['price'],
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=customer_email,
        metadata={'plan': plan}
    )
    
    return session

def handle_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, 
            os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_placeholder')
        )
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle events
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Activate customer account
        customer_email = session.get('customer_email')
        plan = session.get('metadata', {}).get('plan')
        print(f"✅ Payment received from {customer_email} ({plan})")
    
    return jsonify({'received': True})

@app.route('/api/create-checkout', methods=['POST'])
def checkout():
    """Create checkout session"""
    data = request.json
    session = create_checkout_session(
        data['email'],
        data.get('plan', 'pro'),
        data.get('success_url', 'https://kascade.cloud/dashboard'),
        data.get('cancel_url', 'https://kascade.cloud/signup')
    )
    return jsonify({'session_id': session.id, 'url': session.url})

@app.route('/api/webhook/stripe', methods=['POST'])
def stripe_webhook():
    return handle_webhook(request)

if __name__ == '__main__':
    app.run()
