import logging
from time import time
from olab_open_api.api_client import ApiClient
from olab_open_api.api import open_api
from olab_open_api.configuration import Configuration
from .chain.contract_caller import ContractCaller
from .chain.py_order_utils.builders import OrderBuilder
from .chain.py_order_utils.model.order import OrderDataInput, OrderData
from .chain.py_order_utils.constants import ZERO_ADDRESS, ZX
from .chain.py_order_utils.model.signatures import POLY_GNOSIS_SAFE
from .chain.py_order_utils.model.sides import BUY, SELL

API_INTERNAL_ERROR_MSG = "Unable to process your request. Please contact technical support."
MISSING_MARKET_ID_MSG = "market_id is required."
MISSING_TOKEN_ID_MSG = "token_id is required."

class InvalidParamError(Exception):
    pass

class OpenApiError(Exception):
    pass

class Client:
    def __init__(self, host='', apikey='', private_key='', multi_sig_addr='', conditional_tokens_addr='', multisend_addr=''):
        self.conf = Configuration(host=host, api_key=apikey)
        self.contract_caller = ContractCaller(private_key=private_key, multi_sig_addr=multi_sig_addr,
                                              conditional_tokens_addr=conditional_tokens_addr,
                                              multisend_addr=multisend_addr)
        self.api_client = ApiClient(self.conf)
        self.api = open_api.OlabOpenApi(self.api_client)
        
    def get_currencies(self):
        thread = self.api.openapi_currency_get(self.conf.api_key, async_req=True)
        result = thread.get()
        return result
    
    def get_markets(self):
        thread = self.api.openapi_topic_get(self.conf.api_key, async_req=True)
        result = thread.get()
        return result
    
    def get_market(self, market_id):
        try:
            if not market_id:
                raise InvalidParamError(MISSING_MARKET_ID_MSG)
            
            thread = self.api.openapi_topic_topic_id_get(market_id, self.conf.api_key, async_req=True)
            result = thread.get()
            return result
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get market: {e}")
    
    def get_categorical_market(self, market_id):
        try:
            if not market_id:
                raise InvalidParamError(MISSING_MARKET_ID_MSG)
            
            thread = self.api.openapi_topic_multi_topic_id_get(market_id, self.conf.api_key, async_req=True)
            result = thread.get()
            return result
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get categorical market: {e}")
    
    def get_candles(self, token_id, interval="1hour", start_time=int(time()), bars=60):
        try:
            if not token_id:
                raise InvalidParamError(MISSING_TOKEN_ID_MSG)
            
            if not interval:
                raise InvalidParamError('interval is required')
                
            thread = self.api.openapi_order_kline_get(token_id, interval, start_time, bars, self.conf.api_key, async_req=True)
            result = thread.get()
            return result
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get candles: {e}")
    
    def get_orderbook(self, token_id):
        try:
            if not token_id:
                raise InvalidParamError(MISSING_TOKEN_ID_MSG)
            
            thread = self.api.openapi_order_orderbook_get(token_id, self.conf.api_key, async_req=True)
            result = thread.get()
            return result
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get orderbook: {e}")
    
    def get_depth(self, token_id):
        try:
            if not token_id:
                raise InvalidParamError(MISSING_TOKEN_ID_MSG)
            
            thread = self.api.openapi_order_market_depth_get(token_id, self.conf.api_key, async_req=True)
            result = thread.get()
            return result
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get depth: {e}")
    
    # def place_order(self, data: OrderDataInput, exchange_addr='', chain_id=8453):
    #     try:
    #         if not exchange_addr:
    #             raise InvalidParamError('exchange_addr is required')
    #         if not chain_id:
    #             raise InvalidParamError('chain_id is required')
            
    #         builder = OrderBuilder(exchange_addr, chain_id, self.contract_caller.signer)
    #         order_data = OrderData(
    #             maker=self.contract_caller.multi_sig_addr,
    #             taker=ZERO_ADDRESS,
    #             tokenId=data.tokenId,
    #             makerAmount=data.makerAmount,
    #             takerAmount=data.takerAmount,
    #             feeRateBps='0',
    #             side=data.side,
    #             signatureType=POLY_GNOSIS_SAFE,
    #             signer=self.contract_caller.signer.address()
    #         )
    #         signerOrder = builder.build_signed_order(order_data)
            
    #         currencies = self.get_currencies()
    #         market = self.get_market(data.marketId)
    #         currency = 
            
          
    #         v2_add_order_req_body = dict(
    #             salt=signerOrder.salt,
    #             maker=signerOrder.maker,
    #             signer=signerOrder.signer,
    #             taker=signerOrder.taker,
    #             tokenId=signerOrder.tokenId,
    #             makerAmount=signerOrder.makerAmount,
    #             takerAmount=signerOrder.takerAmount,
    #             expiration=signerOrder.expiration,
    #             nonce=signerOrder.nonce,
    #             feeRateBps=signerOrder.feeRateBps,
    #             side=signerOrder.side,
    #             signatureType=signerOrder.signatureType,
    #             signature=signerOrder.signature,
    #             contractAddress="",
    #             currencyAddress=
    #             price='0',
    #             tradingMethod=2,
    #             timestamp=int(time()),
    #             sign
    #         )

    #         thread = self.api.openapi_order_post(self.conf.api_key, v2_add_order_req=signerOrder, async_req=True)
    #         return thread.get()
    #     except InvalidParamError as e:
    #         logging.error(f"Validation error: {e}")
    #         raise
    #     except Exception as e:
    #         logging.error(f"API error: {e}")
    #         raise OpenApiError(f"Failed to place order: {e}")
    
    
    def cancel_order(self, trans_no):
        if not trans_no or not isinstance(trans_no, str):
            raise InvalidParamError('trans_no must be a non-empty string')
        
        request_body = dict(trans_no=trans_no)
        thread = self.api.openapi_order_cancel_order_post(self.conf.api_key, view_cancel_order_request=request_body, async_req=True)
        return thread.get()
    
    def get_my_open_orders(self, market_id=0, limit=10):
        try:
            if not isinstance(market_id, int):
                raise InvalidParamError('market_id must be an integer')
            
            thread = self.api.openapi_order_get(self.conf.api_key, topic_id=market_id, limit=limit, async_req=True)
            return thread.get()
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get open orders: {e}")
    
    def get_my_positions(self, market_id=0, page=1, pageSize=10):
        try: 
            if not isinstance(market_id, int):
                raise InvalidParamError('market_id must be an integer')
            
            if not isinstance(page, int):
                raise InvalidParamError('page must be an integer')
            
            if not isinstance(pageSize, int):
                raise InvalidParamError('pageSize must be an integer')
            
            
            thread = self.api.openapi_portfolio_get(self.conf.api_key, topic_id=market_id, page=page, limit=pageSize, async_req=True)
            return thread.get()
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get my positions: {e}")
    
    def get_my_balances(self):
        try:
            wallet_address = self.contract_caller.signer.address()
            thread = self.api.openapi_user_wallet_address_balance_get(wallet_address, self.conf.api_key, async_req=True)
            return thread.get()
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get my balances: {e}")
        
        return response
    
    def get_my_trades(self, market_id=0, limit=10):
        try:
            if not isinstance(market_id, int):
                raise InvalidParamError('market_id must be an integer')
            
            thread = self.api.openapi_trade_get(self.conf.api_key, topic_id=market_id, limit=limit, async_req=True)
            return thread.get()
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get my trades: {e}")