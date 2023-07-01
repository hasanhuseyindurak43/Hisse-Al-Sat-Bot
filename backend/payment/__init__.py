import requests
import hashlib
import base64


class ValletLightAPI:
    def __init__(self, username, password, shop_code, hash_key):
        self.username = username
        self.password = password
        self.shop_code = shop_code
        self.hash_key = hash_key

    def hash_generate(self, string):
        data = self.username + self.password + self.shop_code + string + self.hash_key
        hash_value = hashlib.sha1(data.encode()).digest()
        hash_base64 = base64.b64encode(hash_value).decode()
        return hash_base64

    def create_payment_link(self, order_data):
        post_data = {
            'userName': self.username,
            'password': self.password,
            'shopCode': self.shop_code,
            'productName': order_data['productName'],
            'productData': order_data['productData'],
            'productType': order_data['productType'],
            'productsTotalPrice': order_data['productsTotalPrice'],
            'orderPrice': order_data['orderPrice'],
            'currency': order_data['currency'],
            'orderId': order_data['orderId'],
            'conversationId': order_data['conversationId'],
            'buyerName': order_data['buyerName'],
            'buyerSurName': order_data['buyerSurName'],
            'buyerGsmNo': order_data['buyerGsmNo'],
            'buyerIp': order_data['buyerIp'],
            'buyerMail': order_data['buyerMail'],
            'callbackOkUrl': 'https://www.websiteniz.com/payment-ok',
            'callbackFailUrl': 'https://www.websiteniz.com/payment-fail',
            'module': 'NATIVE_PHP'
        }

        post_data['hash'] = self.hash_generate(
            str(post_data['orderId']) + str(post_data['currency']) + str(post_data['orderPrice']) +
            str(post_data['productsTotalPrice']) + post_data['productType'] +
            post_data['callbackOkUrl'] + post_data['callbackFailUrl']
        )

        response = self.send_post('https://www.vallet.com.tr/api/v1/create-payment-link', post_data)
        return response


    @staticmethod
    def send_post(post_url, post_data):
        headers = {'Referer': 'https://www.example.com'}
        response = requests.post(post_url, data=post_data, headers=headers)
        result_origin = response.text
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict):
                return result
        return {
            'status': 'error',
            'errorMessage': 'Invalid response from the server',
        }


# Initialize the API with your credentials
vallet = ValletLightAPI("barron4335_api", "cc915435f12858af4413b377169490266d1d23fe", "9001", "EiMnDXf6")

# Define order data
order_data = {
    'productName': 'Tükenmez Kalem',
    'productData': [
        {
            'productName': 'Tükenmez Kalem',
            'productPrice': 1,
            'productType': 'FIZIKSEL_URUN',
        },
    ],
    'productType': 'DIJITAL_URUN',
    'productsTotalPrice': 1,
    'orderPrice': 1,
    'currency': 'TRY',
    'orderId': 'AR-35137',
    'conversationId': '78.167.7.233',
    'buyerName': 'ADI',
    'buyerSurName': 'SOYADI',
    'buyerGsmNo': '05xxXXXxxXX',
    'buyerIp': '127.0.0.1',  # Replace with the actual buyer IP
    'buyerMail': 'test@mail.com',
}

# # Create payment link
# request = vallet.create_payment_link(order_data)
# if request['status'] == 'success' and 'payment_page_url' in request:
#     # Successful operation, retrieve the payment page URL
#     payment_link = request['payment_page_url']
#     print(payment_link)
# else:
#     # Error occurred during link generation
#     print('An error occurred while generating the payment link')
#     print(request)