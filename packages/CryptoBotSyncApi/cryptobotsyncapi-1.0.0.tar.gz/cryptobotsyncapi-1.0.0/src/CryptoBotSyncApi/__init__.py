import logging
from typing import Optional

import requests


class CryptoPay:

    def __init__(self, token: str, test_mode=False):
        """
        Object declaration. Check official docs: https://help.crypt.bot/crypto-pay-api
        :param token: Your app token in @CryptoBot. To create app use command /pay in bot.
        :param test_mode: Your dev mode. It doesn't work in most cases. Default False.
        """
        self.log = logging.getLogger('CryptoPay')
        self.url = 'https://pay.crypt.bot/api/'
        if test_mode:
            self.url = 'https://testnet-pay.crypt.bot/api/'
        self.headers = {
            'Accept': 'application/json',
            'Crypto-Pay-API-Token': token
        }

    def _request(self, method: str, payload: dict = None) -> dict:
        '''
        :param method:
        :param payload:
        :return:
        '''
        response = requests.post(url=self.url + method, headers=self.headers, data=payload)

        return response.json()

    def get_me(self) -> dict:
        '''
        Use this method to test your app's authentication token. Requires no parameters.
        :return: On success, returns basic information about an app.
        '''
        return self._request('getMe')

    def create_invoice(self,
                       amount: str,
                       currency_type: Optional[str] = None,
                       asset: Optional[str] = None,
                       fiat: Optional[str] = None,
                       accepted_assets: Optional[str] = None,
                       description: Optional[str] = None,
                       hidden_message: Optional[str] = None,
                       paid_btn_name: Optional[str] = None,
                       paid_btn_url: Optional[str] = None,
                       payload_param: Optional[str] = None,
                       allow_comments: Optional[bool] = True,
                       allow_anonymous: Optional[bool] = True,
                       expires_in: Optional[int] = None
                       ) -> dict:
        '''
        Use this method to create a new invoice.
        :param amount: Amount of the invoice in float. For example: 125.50
        :param currency_type: Optional. Type of the price, can be “crypto” or “fiat”. Defaults to crypto.
        :param asset: Optional.  Required if currency_type is “crypto”. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC”.
        :param fiat: Optional. Required if currency_type is “fiat”. Fiat currency code. Supported fiat currencies: “USD”, “EUR”, “RUB”, “BYN”, “UAH”, “GBP”, “CNY”, “KZT”, “UZS”, “GEL”, “TRY”, “AMD”, “THB”, “INR”, “BRL”, “IDR”, “AZN”, “AED”, “PLN” and “ILS".
        :param accepted_assets: Optional. List of cryptocurrency alphabetic codes separated comma. Assets which can be used to pay the invoice. Available only if currency_type is “fiat”. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param description: Optional. Description for the invoice. User will see this description when they pay the invoice. Up to 1024 characters.
        :param hidden_message: Optional. Text of the message which will be presented to a user after the invoice is paid. Up to 2048 characters.
        :param paid_btn_name: Optional. Label of the button which will be presented to a user after the invoice is paid. Supported names: viewItem – “View Item”
            openChannel – “View Channel”
            openBot – “Open Bot”
            callback – “Return”
        :param paid_btn_url: Optional. Required if paid_btn_name is specified. URL opened using the button which will be presented to a user after the invoice is paid. You can set any callback link (for example, a success link or link to homepage). Starts with https or http.
        :param payload_param: Optional. Any data you want to attach to the invoice (for example, user ID, payment ID, ect). Up to 4kb.
        :param allow_comments: Optional. Allow a user to add a comment to the payment. Defaults to true.
        :param allow_anonymous: Optional. Allow a user to pay the invoice anonymously. Defaults to true.
        :param expires_in: Optional. You can set a payment time limit for the invoice in seconds. Values between 1-2678400 are accepted.
        :return: On success, returns an object of the created invoice.
        '''
        payload = {
            'amount': amount
        }
        if currency_type == "fiat":
            payload["currency_type"] = currency_type
            payload["fiat"] = fiat
            payload["accepted_assets"] = accepted_assets
            if asset is not None:
                self.log.debug("Instead of 'asset' use parameter 'accepted_assets'")
                asset = None
        if asset:
            payload["asset"] = asset
        if description:
            payload["description"] = description
        if hidden_message:
            payload["hidden_message"] = hidden_message
        if paid_btn_name:
            payload["paid_btn_name"] = paid_btn_name
        if paid_btn_url:
            payload["paid_btn_url"] = paid_btn_url
        if payload_param:
            payload["payload"] = payload_param
        if not allow_comments:
            payload["allow_comments"] = allow_comments
        if not allow_anonymous:
            payload["allow_anoymous"] = allow_anonymous
        if expires_in:
            payload["expires_in"] = expires_in
        info = self._request("createInvoice", payload=payload)
        return info

    def delete_invoice(self,
                       invoice_id: int) -> dict:
        '''
        Use this method to delete invoices created by your app.
        :param invoice_id: Invoice_id to be deleted
        :return: Returns True on success.
        '''
        payload = {
            'invoice_id': invoice_id
        }
        info = self._request('deleteInvoice', payload)
        return info

    def create_check(self,
                     asset: str,
                     amount: str,
                     pin_to_user_id: Optional[int] = None,
                     pin_to_username: Optional[int] = None):
        '''
        Use this method to create a new check.

        :param asset: Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet).
        :param amount: Amount of the check in float. For example: 125.50
        :param pin_to_user_id: Optional. ID of the user who will be able to activate the check.
        :param pin_to_username: Optional. A user with the specified username will be able to activate the check.
        :return: On success, returns an object of the created check.
        '''
        payload = {
            'asset': asset,
            'amount': amount
        }
        if pin_to_user_id:
            payload['pin_to_user_id'] = pin_to_user_id
        if pin_to_username:
            payload['pin_to_username'] = pin_to_username
        info = self._request('createCheck', payload)
        return info

    def delete_check(self, check_id: int):
        '''
        Use this method to delete checks created by your app.
        :param check_id: Check ID to be deleted.
        :return:  Returns True on success.
        '''
        payload = {
            "check_id": check_id
        }
        info = self._request('deleteCheck', payload)
        return info

    def transfer(self,
                 user_id: int,
                 asset: str,
                 amount: str,
                 spend_id: str,
                 comment: Optional[str] = None,
                 disable_send_notification: Optional[bool] = False) -> dict:
        '''
        Use this method to send coins from your app's balance to a user.
        This method must first be enabled in the security settings of your app. Open @CryptoBot (@CryptoTestnetBot for testnet), go to Crypto Pay → My Apps, choose an app, then go to Security -> Transfers... and tap Enable.

        :param user_id: User ID in Telegram. User must have previously used @CryptoBot (@CryptoTestnetBot for testnet).
        :param asset: Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet).
        :param amount: Amount of the transfer in float. The minimum and maximum amount limits for each of the supported assets roughly correspond to 1-25000 USD. Use getExchangeRates to convert amounts. For example: 125.50
        :param spend_id: Random UTF-8 string unique per transfer for idempotent requests. The same spend_id can be accepted only once from your app. Up to 64 symbols.
        :param comment: Optional. Comment for the transfer. Users will see this comment in the notification about the transfer. Up to 1024 symbols.
        :param disable_send_notification: Optional. Pass true to not send to the user the notification about the transfer. Defaults to false.
        :return: On success, returns completed transfer.
        '''
        payload = {
            "user_id": user_id,
            "asset": asset,
            "amount": amount,
            "spend_id": spend_id,
        }
        if comment:
            payload["comment"] = comment
        if disable_send_notification:
            payload["disable_send_notification"] = disable_send_notification
        info = self._request('transfer', payload)
        return info

    def get_invoices(self, asset: Optional[str] = None,
                     fiat: Optional[str] = None,
                     invoice_ids: Optional[str] = None,
                     status: Optional[str] = None,
                     offset: Optional[int] = None,
                     count: Optional[int] = 100):
        """
        Use this method to get invoices created by your app.
        :param asset: Optional. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param fiat: Optional. Fiat currency code. Supported fiat currencies: “USD”, “EUR”, “RUB”, “BYN”, “UAH”, “GBP”, “CNY”, “KZT”, “UZS”, “GEL”, “TRY”, “AMD”, “THB”, “INR”, “BRL”, “IDR”, “AZN”, “AED”, “PLN” and “ILS". Defaults to all currencies.
        :param invoice_ids: Optional. List of invoice IDs separated by comma.
        :param status: Optional. Status of invoices to be returned. Available statuses: “active” and “paid”. Defaults to all statuses.
        :param offset: Optional. Offset needed to return a specific subset of invoices. Defaults to 0.
        :param count: Optional. Number of invoices to be returned. Values between 1-1000 are accepted. Defaults to 100.
        :return: On success, returns array of Invoice.
        """
        payload = {}
        if asset:
            payload['asset'] = asset
        if fiat:
            payload['fiat'] = fiat
        if invoice_ids:
            payload['invoice_ids'] = invoice_ids
        if status:
            payload['status'] = status
        if offset:
            payload['offset'] = offset
        if count:
            payload['count'] = count
        info = self._request('getInvoices', payload=payload)
        return info

    def get_transfers(self, asset: Optional[str] = None,
                      transfer_ids: Optional[str] = None,
                      spend_id: Optional[str] = None,
                      offset: Optional[int] = 0,
                      count: Optional[int] = 100):
        '''
        Use this method to get transfers created by your app.
        :param asset: Optional. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param transfer_ids: Optional. List of transfer IDs separated by comma.
        :param spend_id: Optional. Unique UTF-8 transfer string.
        :param offset: Optional. Offset needed to return a specific subset of transfers. Defaults to 0.
        :param count: Optional. Number of transfers to be returned. Values between 1-1000 are accepted. Defaults to 100.
        :return: On success, returns array of Transfer.
        '''
        payload = {}
        if asset:
            payload['asset'] = asset
        if transfer_ids:
            payload['transfer_ids'] = transfer_ids
        if spend_id:
            payload['spend_id'] = spend_id
        if offset:
            payload['offset'] = offset
        if count:
            payload['count'] = count
        info = self._request('getTransfers', payload)
        return info

    def get_checks(self, asset: Optional[str] = None,
                   check_ids: Optional[str] = None,
                   status: Optional[str] = None,
                   offset: Optional[int] = 0,
                   count: Optional[int] = 100):
        '''
        Use this method to get checks created by your app.
        :param asset: Optional. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param check_ids: Optional. List of check IDs separated by comma.
        :param status: Optional. Status of check to be returned. Available statuses: “active” and “activated”. Defaults to all statuses.
        :param offset: Optional. Offset needed to return a specific subset of check. Defaults to 0.
        :param count: Optional. Number of check to be returned. Values between 1-1000 are accepted. Defaults to 100.
        :return: On success, returns array of Check.
        '''
        payload = {}
        if asset:
            payload['asset'] = asset
        if check_ids:
            payload['check_ids'] = check_ids
        if status:
            payload['status'] = status
        if offset:
            payload['offset'] = offset
        if count:
            payload['count'] = count
        info = self._request('getChecks', payload)
        return info

    def get_balance(self):
        '''
        Use this method to get balances of your app. Requires no parameters.
        :return: Returns array of Balance.
        '''
        info = self._request('getBalance')
        return info

    def get_exchange_rates(self):
        '''
        Use this method to get exchange rates of supported currencies. Requires no parameters.
        :return: Returns array of ExchangeRate.
        '''
        info = self._request('getExchangeRates')
        return info

    def get_currencies(self):
        '''
        Use this method to get a list of supported currencies. Requires no parameters.
        :return: Returns a list of fiat and cryptocurrency alphabetic codes.
        '''
        info = self._request('getCurrencies')
        return info

    def get_stats(self, start_at: Optional[str] = None,
                  end_at: Optional[str] = None):
        """
        Use this method to get app statistics.
        :param start_at: Optional. Date from which start calculating statistics in ISO 8601 format. Defaults is current date minus 24 hours.
        :param end_at: Optional. The date on which to finish calculating statistics in ISO 8601 format. Defaults is current date.
        :return: On success, returns AppStats.
        """
        payload = {}
        if start_at:
            payload['start_at'] = start_at
        if end_at:
            payload['end_at'] = end_at
        info = self._request('getStats', payload)
        return info