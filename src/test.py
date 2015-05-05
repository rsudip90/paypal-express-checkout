from paypal_express import *

p = PayPalExpressCheckout()
token = p.set_express_checkout()
print '*' * 100
# tell user to visit this link otherwise paypal returns error at next step 'Payment not initialized'
raw_input('Please visit following link: '+ PAYMENT_APPROVE_URL + token)
print '*' * 100
print '\n'
token, payer_id = p.get_express_checkout_details(token)
p.do_express_checkout_payment(token, payer_id)
p.get_pal_details()
