# 1. Import the PayPal SDK client that was created in `Set up Server-Side SDK`.
from .PayPalClient import PayPalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest

# https://developer.paypal.com/docs/business/checkout/server-side-api-calls/create-order/
class CreateOrder(PayPalClient):

	#2. Set up your server to receive a call from the client
	""" This is the sample function to create an order. It uses the
		JSON body returned by buildRequestBody() to create an order."""

	def create_order(self, debug=False):
		request = OrdersCreateRequest()
		request.prefer('return=representation')
		#3. Call PayPal to set up a transaction
		request.request_body(self.build_request_body())
		response = self.client.execute(request)
		if debug:
			print('Status Code: ', response.status_code)
			print('Status: ', response.result.status)
			print('Order ID: ', response.result.id)
			print('Intent: ', response.result.intent)
			print('Links:')
			for link in response.result.links:
				print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
			print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
												 response.result.purchase_units[0].amount.value))

		return response

		"""Setting up the JSON request body for creating the order. Set the intent in the
		request body to "CAPTURE" for capture intent flow."""
	@staticmethod
	def build_request_body():
		"""Method to create body with CAPTURE intent"""
		return \
			{
				"intent": "CAPTURE",
				"application_context": {
					"brand_name": "HLG Books",
					"landing_page": "NO_PREFERENCE",
					"user_action": "PAY_NOW"
				},
				"purchase_units": [
					{
						"reference_id": "PUHF",
						"description": "Sporting Goods",

						"custom_id": "CUST-HighFashions",
						"soft_descriptor": "HighFashions",
						"amount": {
							"currency_code": "EUR",
							"value": "290.00",
							"breakdown": {
								"item_total": {
									"currency_code": "EUR",
									"value": "290.00"
								},
							}
						},
						"items": [
							{
								"name": "T-Shirt",
								"description": "Green XL",
								"sku": "sku01",
								"unit_amount": {
									"currency_code": "EUR",
									"value": "190.00"
								},
								"quantity": "1",
								"category": "PHYSICAL_GOODS"
							},
							{
								"name": "Shoes",
								"description": "Running, Size 10.5",
								"sku": "sku02",
								"unit_amount": {
									"currency_code": "EUR",
									"value": "50.00"
								},
								"quantity": "2",
								"category": "PHYSICAL_GOODS"
							}
						],
					}
				]
			}

"""This is the driver function that invokes the createOrder function to create
	 a sample order."""
if __name__ == "__main__":
	CreateOrder().create_order(debug=True)