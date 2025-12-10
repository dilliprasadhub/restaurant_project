from ..repositories.restaurant_repository import RestaurantRepository

class RestaurantService():
    def __init__(self):
        self._repository = RestaurantRepository()

    def signup_restaurant(self, email, password):
        return self._repository.signup_restaurant(email, password)
    
    def login_restaurant(self, email, password):
        return self._repository.login_restaurant(email, password)


    def add_dish(self,add_item):
        return self._repository.add_dish(add_item)
    
    def get_edit_dish(self,item_id):
        return self._repository.get_edit_dish(item_id)
    
    def update_dish(self,item_id,item_name,Description,item_price,item_image,item_status):
        return self._repository.update_dish(item_id,item_name,Description,item_price,item_image,item_status)
    
    def unavailable_dish(self,item_id):
        return self._repository.unavailable_dish(item_id)
    
    def get_item(self):
        return self._repository.get_item_by_id()
    
    def add_order(self, order_data):
        return self._repository.add_order(order_data)
    
    def get_owner_orders(self):
        return self._repository.get_all_orders_for_owner()
    
    def get_user_list(self):
        return self._repository.get_all_dishes()
    
    def update_order_status(self,order_id,new_status):
        return self._repository.update_order_status(order_id,new_status)
    
    def get_user_orders(self,user_id):
        return self._repository.get_user_orders(user_id)
    
    def get_total_orders_count(self):
        return self._repository.get_total_orders_count()
    
    def get_total_items(self):
        return self._repository.get_total_items()
    
    def get_pending_orders_count(self):
        return self._repository.get_pending_orders_count()
    
    def get_accepted_orders_count(self):
        return self._repository.get_accepted_orders_count()

    
    def get_current_user(self, session_token):
        return self._repository.get_current_user(session_token)