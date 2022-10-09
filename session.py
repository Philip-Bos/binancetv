from binance import Client
import config

futures_Client_test = Client(config.futures_api_key_test,
                             config.futures_api_secret_test, testnet=True)

futures_Client = Client(config.futures_api_key,
                        config.futures_api_key_test, testnet=False)


spot_Client_test = Client(config.spot_api_key_test,
                          config.spot_api_secret_test, testnet=True)

spot_Client = Client(config.spot_api_key,
                     config.spot_api_secret, testnet=False)
