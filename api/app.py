"""
Kascade Cloud - Main API Server
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Import modules
from email import send_welcome_email
from stripe import create_checkout_session

# Database (use PostgreSQL in production)
customers = {}

# Config
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '+16155108553')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')

PRICING = {
    'starter': 2900,
    'pro': 7900,
    'enterprise': 19900
}

# Serve static files
@app.route('/')
def index():
    return send_from_directory('..', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('..', filename)

# API Routes
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    customer_id = str(uuid.uuid4())[:8]
    
    customer = {
        'id': customer_id,
        'email': data['email'],
        'business': data['business'],
        'name': data['name'],
        'plan': data.get('plan', 'pro'),
        'channel': data.get('channel', 'whatsapp'),
        'status': 'active',
        'created_at': datetime.utcnow().isoformat(),
        'messages_used': 0,
        'messages_limit': {
            'starter': 1000,
            'pro': 10000,
            'enterprise': float('inf')
        }[data.get('plan', 'pro')],
        'stripe_customer_id': None,
        'checkout_session_id': None
    }
    
    customers[customer_id] = customer
    
    # Send welcome email
    send_welcome_email(customer['email'], customer['name'], customer['plan'])
    
    print(f"✅ New customer: {customer['business']} ({customer['plan']})")
    
    return jsonify({
        'success': True,
        'customer_id': customer_id,
        'message': 'Account created! Check your email.'
    })

@app.route('/api/create-checkout', methods=['POST'])
def checkout():
    """Create Stripe checkout session"""
    data = request.json
    customer_id = data.get('customer_id')
    plan = data.get('plan', 'pro')
    
    if customer_id in customers:
        customers[customer_id]['plan'] = plan
        customers[customer_id]['messages_limit'] = {
            'starter': 1000, 'pro': 10000, 'enterprise': float('inf')
        }[plan]
    
    if STRIPE_SECRET_KEY:
        session = create_checkout_session(
            data['email'], plan,
            f'https://kascade-cloud.vercel.app/dashboard.html?id={customer_id}',
            f'https://kascade-cloud.vercel.app/pricing'
        )
        return jsonify({'url': session.url})
    
    # Demo mode
    return jsonify({
        'url': f'https://kascade-cloud.vercel.app/dashboard.html?id={customer_id}&demo=true'
    })

@app.route('/api/customer/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = customers.get(customer_id)
    if not customer:
        return jsonify({'error': 'Not found'}), 404
    
    return jsonify({
        'business': customer['business'],
        'plan': customer['plan'],
        'messages_used': customer['messages_used'],
        'messages_limit': customer['messages_limit'],
        'status': customer['status'],
        'whatsapp_link': f'wa.me/{WHATSAPP_NUMBER}'
    })

@app.route('/api/usage', methods=['POST'])
def track_usage():
    data = request.json
    customer_id = data.get('customer_id')
    count = data.get('count', 1)
    
    if customer_id in customers:
        customers[customer_id]['messages_used'] = count
        
        used = customers[customer_id]['messages_used']
        limit = customers[customer_id]['messages_limit']
        
        if used >= limit:
            customers[customer_id]['status'] = 'limit_reached'
            return jsonify({'warning': 'Limit reached'})
    
    return jsonify({'success': True})

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'customers': len(customers)
    })

if __name__ == '__main__':
    app.run()
