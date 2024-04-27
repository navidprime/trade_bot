import time
import hashlib
import requests
import json

# https://viabtc.github.io/coinex_api_en_doc/
# https://viabtc.github.io/coinex_api_en_doc/general/#docsgeneral004_common005_api_error_code

class CoinexClient:
    def __init__(self, access_id, secret_key, timeout) -> None:
        self.base_url = "https://api.coinex.com"
        self.access_id = access_id
        self.secret_key = secret_key
        self.timeout = timeout

    def sign(self, args: dict) -> str:
        args["access_id"] = self.access_id
        args["tonce"] = int(time.time() * 1000)
        last_args = [("secret_key", self.secret_key)]
        sorted_args = sorted(args.items(), key=lambda x: x[0]) + last_args
        body = "&".join([f"{key}={value}" for key, value in sorted_args])
        md5 = hashlib.md5(body.encode("utf-8")).hexdigest()
        return md5.upper()

    def post(self, path: str, args: dict, signature: str = None) -> dict:
        json_data = json.dumps(args)
        headers = {"Content-Type": "application/json"}
        if signature is not None:
            headers["authorization"] = signature
        response = requests.post(
            self.base_url + path,
            data=json_data,
            headers=headers,
            timeout=self.timeout,
        )
        result = response.json()
        return result
    
    def get(self, path: str, args: dict = None, signature: str = None) -> dict:
        url = self.base_url + path
        if args is not None:
            param = "&".join([f"{key}={value}" for key, value in args.items()])
            url = url + "?" + param

        result = ""
        if signature is not None:
            headers = {"authorization": signature}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            result = response.content.decode("utf-8")
        else:
            response = requests.get(url, timeout=self.timeout)
            result = response.content.decode("utf-8")

        return json.loads(result)
    
    def account_balance(self):
        """https://viabtc.github.io/coinex_api_en_doc/spot/#docsspot002_account001_account_info"""
        args = {}
        signature = self.sign(args)
        return self.get("/v1/balance/info", args, signature)

    def place_market_order(self, **kwargs):
        """https://viabtc.github.io/coinex_api_en_doc/spot/#docsspot003_trade003_market_order"""
        signature = self.sign(kwargs)
        return self.post("/v1/order/market", kwargs, signature)

    def place_market_order2(self, **kwargs):
        orderType = kwargs["type"]
        market = kwargs["market"]
        percentage = float(kwargs["percentage"])
        
        balance = self.account_balance()
        assert balance["code"] == 0
        balance = balance["data"]
        
        if (orderType == "buy"): # USDT
            try:
                amount = float(balance["USDT"]["available"]) * percentage
            except KeyError:
                return {"message":"no USDT"}
            
            return self.place_market_order(
                market=market,
                type="buy",
                amount=amount
            )
        # sell
        try:
            amount = float(balance[market[:-4]]["available"]) * percentage
        except KeyError:
            return {"message":f"no {market[:-4]}"}
        
        return self.place_market_order(
            market=market,
            type="sell",
            amount=amount
        )
        
    def withdraw(self, **kwargs):
        """https://viabtc.github.io/coinex_api_en_doc/spot/#docsspot002_account015_submit_withdraw"""
        # args = {"coin_type":coin_type, "smart_contract_name":smart_contract_name,
                # "coin_address":coin_address, "transfer_method":transfer_method, "actual_amount":actual_amount}
        signature = self.sign(kwargs)
        
        return self.post("/v1/balance/coin/withdraw", kwargs, signature)
    
    def get_withdraw_record(self, **kwargs):
        """https://viabtc.github.io/coinex_api_en_doc/spot/#docsspot002_account026_withdraw_list"""
        signature = self.sign(kwargs)
        return self.get("/v1/balance/coin/withdraw",kwargs,signature)