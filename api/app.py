"""
Kascade Cloud API - Customer Signup & Provisioning
"""

from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.')

# In-memory storage (use database in production)
customers = {}

# Load secrets from environment
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/signup')
def signup_page():
    return send_from_directory('.', 'signup.html')

@app.route('/dashboard')
def dashboard_page():
    return send_from_directory('.', 'dashboard.html')

@app.route('/api/signup', methods=['POST'])
def handle_signup():
    """Handle customer signup"""
    import uuid
    from datetime import datetime
    
    data = request.json
    
    # Validate required fields
    required = ['email', 'business', 'name', 'plan']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Create customer
    customer_id = str(uuid.uuid4())[:8]
    customer = {
        'id': customer_id,
        'email': data['email'],
        'business': data['business'],
        'name': data['name'],
        'plan': data['plan'],
        'price': {'starter': 29, 'pro': 79, 'enterprise': 199}[data['plan']],
        'channel': data.get('channel', 'whatsapp'),
        'phone': data.get('phone', ''),
        'status': 'active',
        'created_at': datetime.utcnow().isoformat(),
        'messages_used': 0,
        'messages_limit': {
            'starter': 1000,
            'pro': 10000,
            'enterprise': float('inf')
        }
    }
    
    customers[customer_id] = customer
    
    print(f"📦 New signup: {data['business']} ({data['plan']})")
    
    return jsonify({
        'success': True,
        'customer_id': customer_id,
        'message': 'Account created!'
    })

@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer_dashboard(customer_id):
    """Get customer dashboard data"""
    customer = customers.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    return jsonify({
        'business': customer['business'],
        'plan': customer['plan'],
        'messages_used': customer['messages_used'],
        'messages_limit': customer['messages_limit'],
        'status': customer['status'],
        'whatsapp_link': f'wa.me/{WHATSAPP_NUMBER}' if WHATSAPP_NUMBER else None
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'customers': len(customers)})

if __name__ == '__main__':
    app.run()
