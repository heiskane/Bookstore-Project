# Bookstore-Project

# ⚠ Work in Progress

## Uvicorn deployment (Development)
```bash
git clone https://github.com/heiskane/Bookstore-Project.git
cd Bookstore-Project/fastapi_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
firefox http://localhost:8000/docs
```

## Docker deployment
```bash
git clone https://github.com/heiskane/Bookstore-Project.git
cd Bookstore-Project/fastapi_backend
docker build -t bookstore_api .
docker run -d --name bookstore_backend -p 8000:80 -e GUNICORN_CONF="/app/app/gunicorn_conf.py"  bookstore_api
firefox http://localhost:8000/docs
```


Api documentation can be found at http://localhost:8000/docs


# PayPal Integration
## General idea
I had looked into PayPal integration for at least couple of days but every example seemed to use only the frontend appllication and from security standpoint that did not seem like a good solution. I didnt want to deal with secret keys on the frontend and i wanted to be able to do some things on the serverside like adding order information to the database and properly validate purchases. Eventually i found this article on PayPals developer documentation about [making API calls from your server](https://developer.paypal.com/docs/business/checkout/server-side-api-calls/). I'm still not sure about what **exactly** happens in every step of the way but from what i understand this is the basic idea.

* Frontend PayPal button launches "PayPal Experience"
* Frontend makes an API call to my backend to create an order
* Backend calls PayPal API to create an order and returns relevant data
* Client uses the PayPal window to authenticate with PayPal and approve the order
* Frontend makes an API call to the backend to "capture the order" aka get the money

With this structure i will have all the control that i want to deal with security. For example i can just expect a product id and craft the order with the data from the databse instead of offering an "Inspect Element"-discount (client changing the price in the client-side code). After that i am not sure if i really need to do more validation when capturing the order or not but from what i understand that **shouldn't** be nessesary. Either way after capturing the order i can add any relevant info into my database like allowing the user to download the book that is seen in the order information.

## Basic Implementation
### Backend
Note that everything here is done in the sandbox environtment with sandbox accounts. So far i have the backend code working but im still having some issues with the frontend portion so ill mostly focus on the backend here.

Update: I have fixed the issues i had. I will go over the issues i had a bit and and then I'll show the frontend that i have so far. the TLDR is that i was opening the HTML file with firefox and hosting the file with apache fixed my issues.

First the PayPal client has to be setup. I based my code on [PayPals documentation on the client](https://developer.paypal.com/docs/checkout/reference/server-integration/setup-sdk/). One thing im doing diffrently from PayPals code is that I'm using dotenv to deal with the secret and client id. The reason for this is that i do not want any secrets in the public repository and i suggest always doing this to avoid leaking things like API keys. To do this i created a `.env` file with the following contents and added `.env` to the `.gitignore` file.


* `.env`:

```
PAYPAL-SANDBOX-CLIENT-ID = MY_CLIENT_ID_HERE
PAYPAL-SANDBOX-CLIENT-SECRET = MY_CLIENT_SECRET_HERE
```



* `PayPalClient.py`:

```python
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from dotenv import load_dotenv
from os import getenv

import sys

load_dotenv()

CLIENT_ID = getenv('PAYPAL-SANDBOX-CLIENT-ID')
CLIENT_SECRET = getenv('PAYPAL-SANDBOX-CLIENT-SECRET')

# https://developer.paypal.com/docs/checkout/reference/server-integration/setup-sdk/
class PayPalClient:
	def __init__(self):
		self.client_id = CLIENT_ID
		self.client_secret = CLIENT_SECRET

		"""Set up and return PayPal Python SDK environment with PayPal access credentials.
		   This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

		self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

		""" Returns PayPal HTTP client instance with environment that has access
			credentials context. Use this instance to invoke PayPal APIs, provided the
			credentials have access. """
		self.client = PayPalHttpClient(self.environment)

	def object_to_json(self, json_data):
		"""
		Function to print all json data in an organized readable manner
		"""
		result = {}
		if sys.version_info[0] < 3:
			itr = json_data.__dict__.iteritems()
		else:
			itr = json_data.__dict__.items()
		for key,value in itr:
			# Skip internal attributes.
			if key.startswith("__"):
				continue
			result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
						self.object_to_json(value) if not self.is_primittive(value) else\
						 value
		return result;

	def array_to_json_array(self, json_array):
		result =[]
		if isinstance(json_array, list):
			for item in json_array:
				result.append(self.object_to_json(item) if  not self.is_primittive(item) \
							  else self.array_to_json_array(item) if isinstance(item, list) else item)
		return result;

	def is_primittive(self, data):
		return isinstance(data, str) or isinstance(data, str) or isinstance(data, int)
```

This class will be used by the others to communicate with PayPals API. Next the the class for creating orders has to be created. I based my code off [PayPals example](https://developer.paypal.com/docs/business/checkout/server-side-api-calls/create-order/
) again and removed some unnessesary data from the example order.

* `CreateOrder.py`:

```python
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
							"value": "180.00",
							"breakdown": {
								"item_total": {
									"currency_code": "EUR",
									"value": "180.00"
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
									"value": "90.00"
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
									"value": "45.00"
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
```

This class has a `build_request_body` method that essentially json data for the order. Eventually i will have to add some logic to set the data depending on what the client orders in the store. I will probably do that in the `build_request_body` method and the API endpoint that i created for it. The code for the endpoint is pretty minimal so all it does is initialize the class and run the `create_order` method. Notice that debugging is **on** here and should be removed in preduction.

* `main.py`:

```python
[...snip...]

@app.post("/checkout/paypal/order/create/")
def paypal_create_order():
	return CreateOrder().create_order(debug=True)
```

When sending a request to this endpoint it returns all of the relevant order information but there is so much of it that i dont want to include it here. Looking at the terminal though the code prints all the data i need for now because debugging is on.

```bash
Status Code:  201
Status:  CREATED
Order ID:  44V630951H329442K
Intent:  CAPTURE
Links:
        self: https://api.sandbox.paypal.com/v2/checkout/orders/44V630951H329442K       Call Type: GET
        approve: https://www.sandbox.paypal.com/checkoutnow?token=44V630951H329442K     Call Type: GET
        update: https://api.sandbox.paypal.com/v2/checkout/orders/44V630951H329442K     Call Type: PATCH
        capture: https://api.sandbox.paypal.com/v2/checkout/orders/44V630951H329442K/capture    Call Type: POST
Total Amount: EUR 180.00
INFO:     127.0.0.1:60326 - "POST /checkout/paypal/order/create/ HTTP/1.1" 200 OK
```

The most important lin here is the `approve` link. It is used for the client to approve the payment after which it is ready to be captured. One issue i am facing here is that after clicking on the `Pay Now` button the page is refreshed and nothing seems to change. In reality payment does get approved but for some reason nothing happens. I know that it gets approved because i have tested capturing it so ill go over that next. First though i want to mention that i know that in `CreateOrder.py` i can add `return_url` in the `application_context` (in the order JSON data) but what that does is that it redirects the window to chosen url. The way i want it to work (and the way its supposed to work) is that clientside JavaScript should open the "PayPal experience" and after client approves the order the clientside code should make an API call to the backend which captures that funds without any redirects. I'll should the clientside code that is *supposed* to work at the end. Now finally for the code to capture the order and the API endpoint to use it. Again i based it off [PayPals example](https://developer.paypal.com/docs/business/checkout/server-side-api-calls/capture-order/).

* `main.py`:

```python
@app.post("/checkout/paypal/order/{order_id}/capture")
def paypal_capture_order(order_id: str):
	return CaptureOrder().capture_order(order_id, debug=True)
```

* `CaptureOrder.py`:

```python
# 1. Import the PayPal SDK client created in `Set up Server-Side SDK` section.
from .PayPalClient import PayPalClient
from paypalcheckoutsdk.orders import OrdersCaptureRequest

# https://developer.paypal.com/docs/business/checkout/server-side-api-calls/capture-order/
class CaptureOrder(PayPalClient):

	#2. Set up your server to receive a call from the client
	"""this sample function performs payment capture on the order.
	Approved order ID should be passed as an argument to this function"""

	def capture_order(self, order_id, debug=False):
		"""Method to capture order using order_id"""
		request = OrdersCaptureRequest(order_id)
		#3. Call PayPal to capture an order
		response = self.client.execute(request)
		#4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
		if debug:
			print('Status Code: ', response.status_code)
			print('Status: ', response.result.status)
			print('Order ID: ', response.result.id)
			print('Links: ')
			for link in response.result.links:
				print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
			print('Capture Ids: ')
			for purchase_unit in response.result.purchase_units:
				for capture in purchase_unit.payments.captures:
					print('\t', capture.id)
			print("Buyer:")
			print("\tEmail Address: {}\n\tName: {}".format(response.result.payer.email_address,
				response.result.payer.name.given_name + " " + response.result.payer.name.surname))
		return response


"""This driver function invokes the capture order function.
Replace Order ID value with the approved order ID. """
if __name__ == "__main__":
	order_id = '8FG1114532522410D'
	CaptureOrder().capture_order(order_id, debug=True)
```

Now making a request to the endpoint with the order id i got earlier.

```bash
curl -X 'POST' \
  'http://localhost:8000/checkout/paypal/order/44V630951H329442K/capture' \
  -H 'accept: application/json' \
  -d ''
```

Looking at the console it prints some data showing that the order was successfully captured.

```bash
Status Code:  201
Status:  COMPLETED
Order ID:  44V630951H329442K
Links: 
        self: https://api.sandbox.paypal.com/v2/checkout/orders/44V630951H329442K       Call Type: GET
Capture Ids: 
         3P262213NS999274N
Buyer:
        Email Address: sb-hqb47c7620436@personal.example.com
        Name: John Doe
INFO:     127.0.0.1:60834 - "POST /checkout/paypal/order/44V630951H329442K/capture HTTP/1.1" 200 OK
```

I also verified that the funds were transfered in [PayPals sandbox](https://www.sandbox.paypal.com/activities/)

![[/img/paypal_transaction.png]]

### Frontend

So as mentioned before the issues i was having with the frontend were because i was opening the HTML file with firefox instead of hosting it with a web server. I think PayPal might just be picky about the protocol or something. Either way the code that i have i (again) based on [PayPals example code](https://developer.paypal.com/demo/checkout/#/pattern/server)

```html
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="utf-8">
	<!-- Add meta tags for mobile and IE -->
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta http-equiv="X-UA-Compatible" content="IE=edge" />
	<title> PayPal Checkout Integration | Server Demo </title>
</head>

<body>
	<!-- Set up a container element for the button -->
	<div id="paypal-button-container"></div>

	<!-- Include the PayPal JavaScript SDK -->
	<!-- https://developer.paypal.com/docs/business/javascript-sdk/javascript-sdk-reference/ -->
	<!-- https://developer.paypal.com/demo/checkout/#/pattern/server -->
	<script src="https://www.paypal.com/sdk/js?client-id=AVRE2PhqcdO4hh6ak49te0ouOyRq3cdngOheyPvCqS7QQew1XOykcvEM4L9X3DGyWRDnyhGsCZtUg62m&currency=EUR"></script>

	<script>
		// Render the PayPal button into #paypal-button-container
		paypal.Buttons({

			// Call your server to set up the transaction
			createOrder: function(data, actions) {
				return fetch('http://localhost:8000/checkout/paypal/order/create/', {
					method: 'post'
				}).then(function(res) {
					return res.json();
				}).then(function(orderData) {
					// Maybe deal with this server-side
					return orderData.result.id;
				});
			},
			
			// Call your server to finalize the transaction
			onApprove: function(data, actions) {
				return fetch('http://localhost:8000/checkout/paypal/order/' + data.orderID + '/capture/', {
					method: 'post'
				}).then(function(res) {
					return res.json();
				}).then(function(orderData) {
					// Three cases to handle:
					//   (1) Recoverable INSTRUMENT_DECLINED -> call actions.restart()
					//   (2) Other non-recoverable errors -> Show a failure message
					//   (3) Successful transaction -> Show confirmation or thank you

					// This example reads a v2/checkout/orders capture response, propagated from the server
					// You could use a different API or structure for your 'orderData'
					var errorDetail = Array.isArray(orderData.details) && orderData.details[0];

					if (errorDetail && errorDetail.issue === 'INSTRUMENT_DECLINED') {
						return actions.restart(); // Recoverable state, per:
						// https://developer.paypal.com/docs/checkout/integration-features/funding-failure/
					}

					if (errorDetail) {
						var msg = 'Sorry, your transaction could not be processed.';
						if (errorDetail.description) msg += '\n\n' + errorDetail.description;
						if (orderData.debug_id) msg += ' (' + orderData.debug_id + ')';
						return alert(msg); // Show a failure message (try to avoid alerts in production environments)
					}

					// Successful capture! For demo purposes:
					console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
					var transaction = orderData.result.purchase_units[0].payments.captures[0];
					alert('Transaction '+ transaction.status + ': ' + transaction.id + '\n\nSee console for all available details');

					// Replace the above to show a success message within this page, e.g.
					// const element = document.getElementById('paypal-button-container');
					// element.innerHTML = '';
					// element.innerHTML = '<h3>Thank you for your payment!</h3>';
					// Or go to another URL:  actions.redirect('thank_you.html');
				});
			},



		}).render('#paypal-button-container');
	</script>
</body>

</html>
```

Essentially this code just launches the "PayPal experience" in a new window and creates the order using previously created endpoint. In the future this is also going to specify the product that the user wants to buy but for now im just using the test data in `CreateOrder.py`. As the code suggests when the client approves the order an API call is made to my backend to simply capture the order. There are still some errors when trying to log the data to console but all of that is just example code that will change later and the actual payments are going through so this will have to be good enough for now.
