from src.config.db import db
import os

class RestaurantRepository():
    def __init__(self):
        pass

    def signup_restaurant(self,email,password):
        user = db.auth.sign_up({"email":email,"password":password})
        return user
    
    def login_restaurant(self,email,password):
        user=db.auth.sign_in_with_password({
            "email":email,
            "password":password
        })
        return user
    
    def add_dish(self,add_item):
        response=db.table('items').insert(add_item).execute()
        return response
    
    def get_edit_dish(self,item_id):
        response = db.table('items').select ('*').eq("id",item_id).execute()
        return response
    
    def update_dish(self,item_id,item_name,Description,item_price,item_image,item_status):
        return db.table('items').update({
            "item_name":item_name,
            "description":Description,
            "item_price":item_price,
            "item_image":item_image,
            "item_status":item_status
        }).eq('id',item_id).execute()
    

    def unavailable_dish(self,item_id):
        return db.table('items').update({'item_status':"Unavailable"}).eq('id',item_id).execute()
    

    def get_all_dishes(self):
        response = db.table("items").select("*") .eq("item_status", "Available").execute()
        return response.data
    

    def get_item_by_id(self):
        return db.table("items") .select("*").execute().data
    
    def get_item_by_user(self):
        return ( db.table("items") .select("*").eq("status", "available").execute() .data)
   

    def add_order(self, order_data):
        return db.table("orders") .insert(order_data) .execute().data
    

    def get_all_orders_for_owner(self):
        return db.table("orders") .select(""" *, item:item_id(item_name, item_price, item_image) """).neq("order_status", "Served") .execute().data
    

    def update_order_status(self, order_id, new_status):
        return (db.table("orders").update({"order_status": new_status}).eq("id", order_id).execute().data)
    

    def get_user_orders(self, user_id):
        return db.table("orders").select("*, item:item_id(item_name, item_price, item_image)").eq("user_id", user_id).execute().data
    

    def get_total_orders_count(self):
        return (db.table("orders").select("id", count="exact").execute().count)
    

    def get_total_items(self):
        return db.table('items').select("id",count="exact").execute().count
    

    def get_pending_orders_count(self):
        return (db.table("orders").select("id", count="exact").eq("order_status", "Pending").execute().count)
    

    def get_accepted_orders_count(self):
        return (db.table("orders").select("id", count="exact").eq("order_status", "Accepted").execute().count)
    


    def get_menu_items(self):
        items = db.table("items").select("*").execute().data
        return items
    

    def format_menu_items(self,items):
        text = "MENU ITEMS:\n"
        for item in items:
            text += f"- {item['item_name']} | Price: {item['item_price']} | Description: {item['description']}\n"
        return text


    def get_current_user(self,session_token):
        user=db.auth.get_user(session_token)
        return user
    
