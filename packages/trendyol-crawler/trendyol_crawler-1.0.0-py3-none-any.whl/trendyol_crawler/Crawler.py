import base64
import datetime
from typing import Optional
from requests import Session
from dotenv import load_dotenv
import os

from trendyol_crawler.models.Menu import Menu, ProductStatus
from trendyol_crawler.models.Order import OrderCancelReasonType, OrderResponse, OrderStatus, Order
from trendyol_crawler.models.Restaurant import RestaurantStatus, RestaurantsResponse


class TrendyolAPI:
    def __init__(self, supplier_id: str, api_key: str, api_secret: str, is_test: bool = False):
        load_dotenv()
        self.url = f"https://api.trendyol.com/mealgw/suppliers/{supplier_id}/" if not is_test else f"https://stageapi.trendyol.com/mealgw/suppliers/{supplier_id}/"
        self.supplier_id = supplier_id        
        self.headers = {
            "User-Agent": f"{supplier_id} - SelfIntegration",
            "Authorization": f"Basic {base64.b64encode(f'{api_key}:{api_secret}'.encode('ascii')).decode('ascii')}"
        }
        self.session = Session()

    
    def get_restaurants(self) -> RestaurantsResponse:
        url_path = "restaurants"
        params = {
            "page": 0,
            "size": 50
        }
        response = self.session.get(self.url + url_path, headers=self.headers, params=params).json()
        return RestaurantsResponse(**response)

    def update_restaurant_status(self, restaurant_id: str, status: RestaurantStatus):
        url_path = f"restaurants/{restaurant_id}/status"
        
        self.session.put(self.url + url_path, headers=self.headers, json={"status": status})
        
        return "OK."
    
    def get_menu(self, restaurant_id: str) -> Menu:
        url_path = f"restaurants/{restaurant_id}/products"
        res = self.session.get(self.url + url_path, headers=self.headers)
        print(res.url)
        return Menu(**res.json())
    
    def update_product_status(self, restaurant_id: str, product_id: int, status: ProductStatus):
        url_path = f"restaurants/{restaurant_id}/products/{product_id}/status"
        data = {
            "status": status
        }
        self.session.put(self.url + url_path, headers=self.headers, json=data)
        return "Ok."
    
    def get_orders(self, page: int = 0, size: int = 50, status: OrderStatus = OrderStatus.Created, restaurant_id: Optional[str] = None) -> OrderResponse:
        url_path = "packages"
        _headers = self.headers
        _headers.update({
            "x-agentname": "SelfIntegration",
            "x-executor-user": "esat3515@gmail.com"
        }
        )
        params = {
            #"page": page,
            #"size": size,
            "packageStatuses": status,
            "supplierId": self.supplier_id,
            #"packageModificationStartDate": int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()),
            #"packageModificationEndDate": int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp())
        }
        
        if restaurant_id is not None:
            params.update({
                "storeId": restaurant_id
            })
        data = self.session.get(self.url + url_path, headers=_headers, params=params).json()
        
        
        if data.get("errors") is not None:
            return None
        return OrderResponse(**data, current_page=page)

    def get_order(self, id: str):
        url_path = f"packages/{id}"
        _headers = self.headers
        _headers.update({
            "x-agentname": "SelfIntegration",
            "x-executor-user": "esat3515@gmail.com"
        }
        )
        response = self.session.get(self.url + url_path, headers=_headers).json()
        return Order(**response)
    
    def cancel_order(self, order: Order, order_cancel_reason: OrderCancelReasonType):
        url_path = "packages/unsupplied"
        _headers = self.headers
        _headers.update({
            "x-agentname": "SelfIntegration",
            "x-executor-user": "esat3515@gmail.com"
        }
        )
        data = {
            "packageId": order.orderId,
            "reasonId": order_cancel_reason,
            "itemIdList": [item.lineItemId for line in order.lines for item in line.items]
        }
        self.session.put(self.url + url_path, headers=self.headers, json=data)
        return "Ok."
    
    def pick_order(self, order: Order):
        url_path = "packages/picked"
        _headers = self.headers
        _headers.update({
            "x-agentname": "SelfIntegration",
            "x-executor-user": "esat3515@gmail.com"
        }
        )
        data = {
            "packageId": order.id,
            "preparationTime": 30
            
        }
        print("Pick Order")
        self.session.put(self.url + url_path, headers=_headers, json=data)
        return "Ok."