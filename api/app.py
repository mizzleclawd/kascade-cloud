"""
Kascade Cloud API - Customer Signup & Provisioning
Deploy to: Render.com or Fly.io
"""

from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Database (use real DB in production)
customers = {}

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '')

@app.route('/')
def index():
    return send_from_directory('..', 'index.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    customer_id = str(uuid.uuid4())[:8]
    customers[customer_id] = {
        'id': customer_id,
        'email': data['email'],
        'business': data['business'],
        'plan': data['plan'],
        'price': {'starter': 29, 'pro': 79, 'enterprise': 199}[data['plan']],
        'status': 'active',
        'created_at': datetime.utcnow().isoformat(),
        'messages_used': 0,
        'messages_limit': {'starter': 1000, 'pro': 10000, 'enterprise': float('inf')}
    }
    return jsonify({'success': True, 'customer_id': customer_id})

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'customers': len(customers)})

if __name__ == '__main__':
    app.run()
