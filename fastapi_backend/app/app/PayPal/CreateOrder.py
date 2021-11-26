# 1. Import the PayPal SDK client that was created in `Set up Server-Side SDK`.
from typing import Any
from typing import Dict
from typing import List

from paypalcheckoutsdk.orders import OrdersCreateRequest

from ..models import Book
from .PayPalClient import PayPalClient


# https://developer.paypal.com/docs/business/checkout/server-side-api-calls/create-order/
class CreateOrder(PayPalClient):

	# 2. Set up your server to receive a call from the client
	"""This is the sample function to create an order. It uses the
	JSON body returned by buildRequestBody() to create an order."""

	def create_order(self, books: List[Book], debug: bool = False) -> str:
		request = OrdersCreateRequest()
		request.prefer("return=representation")
		# 3. Call PayPal to set up a transaction
		request.request_body(self.build_request_body(books))
		response = self.client.execute(request)
		if debug:
			print("Status Code: ", response.status_code)
			print("Status: ", response.result.status)
			print("Order ID: ", response.result.id)
			print("Intent: ", response.result.intent)
			print("Links:")
			for link in response.result.links:
				print(
					"\t{}: {}\tCall Type: {}".format(link.rel, link.href, link.method)
				)
			print(
				"Total Amount: {} {}".format(
					response.result.purchase_units[0].amount.currency_code,
					response.result.purchase_units[0].amount.value,
				)
			)

		return response

		"""Setting up the JSON request body for creating the order. Set the intent in the
		request body to "CAPTURE" for capture intent flow."""

	@staticmethod
	def build_request_body(books: List[Book]) -> Dict[str, Any]:
		"""Method to create body with CAPTURE intent"""
		books_json = []
		total_price = 0  # Use float
		for book in books:
			total_price += book.price
			books_json.append(
				{
					"name": book.title,
					"unit_amount": {"currency_code": "EUR", "value": book.price},
					"quantity": 1,
					"category": "DIGITAL_GOODS",
				}
			)

		return {
			"intent": "CAPTURE",
			"application_context": {
				"brand_name": "HLG Books",
				"landing_page": "NO_PREFERENCE",
				"user_action": "CONTINUE",
				# This is for mobile app
				"return_url": "https://api.hlgbooks.com/mobile/checkout/paypal/order/capture/"
			},
			"purchase_units": [
				{
					"amount": {
						"currency_code": "EUR",
						"value": total_price,
						"breakdown": {
							"item_total": {
								"currency_code": "EUR",
								"value": total_price,
							},
						},
					},
					"items": books_json,
				}
			],
		}
