# 1. Import the PayPal SDK client that was created in `Set up Server-Side SDK`.
from paypalcheckoutsdk.orders import OrdersGetRequest

from .PayPalClient import PayPalClient


class GetOrder(PayPalClient):

    # 2. Set up your server to receive a call from the client
    """You can use this function to retrieve an order by passing order ID as an argument"""

    def get_order(self, order_id: str) -> str:
        """Method to get order"""
        request = OrdersGetRequest(order_id)
        # 3. Call PayPal to get the transaction
        response = self.client.execute(request)

        # 4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.
        print("Status Code: ", response.status_code)
        print("Status: ", response.result.status)
        print("Order ID: ", response.result.id)
        print("Intent: ", response.result.intent)
        print("Links:")
        for link in response.result.links:
            print("\t{}: {}\tCall Type: {}".format(link.rel, link.href, link.method))
        print(
            "Gross Amount: {} {}".format(
                response.result.purchase_units[0].amount.currency_code,
                response.result.purchase_units[0].amount.value,
            )
        )
        return response


"""This driver function invokes the get_order function with
	order ID to retrieve sample order details. """
if __name__ == "__main__":
    GetOrder().get_order("3LX55272PS028092W")
