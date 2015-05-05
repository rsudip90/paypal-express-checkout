import requests
from cgi import parse_qs
from ConfigParser import SafeConfigParser

__all__ = ['PayPalExpressCheckout', 'PAYMENT_APPROVE_URL']

# cancel url redirected from paypal in case of cancelation
CANCEL_URL = 'http://www.example.com/cancel.html'
# return url redirected from paypal
RETURN_URL = 'http://www.example.com/return.html'
# we only test it in sandbox not really !!
PAYPAL_API_END_POINT = 'https://api-3t.sandbox.paypal.com/nvp'
# api version
PAYPAL_API_VERSION = 109.0
# paypal payment approval url
PAYMENT_APPROVE_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token='

class PayPalExpressCheckout(object):
	"""
	A Simple Python module for PayPal Express Checkout.
	Have a look at link to implement express checkout:
	https://developer.paypal.com/docs/classic/express-checkout/integration-guide/ECGettingStarted/#idbec8c969-cd47-4d23-bb4b-18a5e0c1fd17
	"""

	def __init__(self):
		parser = SafeConfigParser()
		parser.read('keys.ini')

		user = parser.get('paypal_express_auth', 'USER')
		pwd = parser.get('paypal_express_auth', 'PWD')
		signature = parser.get('paypal_express_auth', 'SIGNATURE')

		self.auth_params = {
			'USER': user,
			'PWD': pwd,
			'SIGNATURE': signature,
			'VERSION': PAYPAL_API_VERSION,
		}

	def set_express_checkout(self):
		params = {
			'METHOD': 'SetExpressCheckout',
			'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
			'PAYMENTREQUEST_0_AMT': 100,
			'PAYMENTREQUEST_0_CURRENCYCODE': 'USD',
			'CANCELURL': CANCEL_URL,
			'RETURNURL': RETURN_URL,
		}
		params.update(self.auth_params)
		r = requests.get(PAYPAL_API_END_POINT, params = params)
		data = parse_qs(r.text)
		for d in data:
			print '%s : %s' % (d, data[d])
		print '=' * 100
		print '\n'
		return data['TOKEN'][0]

	def get_express_checkout_details(self, token):
		params = {
			'METHOD' : "GetExpressCheckoutDetails",
			'RETURNURL' : RETURN_URL, 
			'CANCELURL' : CANCEL_URL,  
			'TOKEN' : token,
		}
		params.update(self.auth_params)
		r = requests.get(PAYPAL_API_END_POINT, params = params)
		data = parse_qs(r.text)
		for d in data:
			print '%s : %s' % (d, data[d])
		print '=' * 100
		print '\n'
		try:
			response_token = data['TOKEN'][0]
			payer_id = data['PAYERID'][0]
		except KeyError:
			response_token = data
			payer_id = ''
		return response_token, payer_id

	def do_express_checkout_payment(self, token, payer_id):
		params = {
			'METHOD' : "DoExpressCheckoutPayment",
			'PAYMENTREQUEST_0_PAYMENTACTION' : 'Sale',
			'RETURNURL' : RETURN_URL,
			'CANCELURL' : CANCEL_URL,
			'TOKEN' : token,
			'PAYMENTREQUEST_0_AMT' : 100,
			'PAYERID' : payer_id
		}
		params.update(self.auth_params)
		r = requests.get(PAYPAL_API_END_POINT, params = params)
		data = parse_qs(r.text)
		for d in data:
			print '%s : %s' % (d, data[d])
		print '=' * 100
		print '\n'

	def get_pal_details(self):
		params = {
			'METHOD' : "GetPalDetails",
		}
		params.update(self.auth_params)
		r = requests.get(PAYPAL_API_END_POINT, params = params)
		data = parse_qs(r.text)
		for d in data:
			print '%s : %s' % (d, data[d])
		print '=' * 100
		print '\n'

