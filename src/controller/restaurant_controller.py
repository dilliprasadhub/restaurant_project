from fastapi import APIRouter,FastAPI,Request,Form
from fastapi.responses import HTMLResponse, JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from ..service.restaurant_service import RestaurantService
from .. integration.google_ai import ask_gemini

from src.config.db import db

router=APIRouter()

templates=Jinja2Templates(directory="templates")


def get_loggedin_user(request: Request):
    token = request.cookies.get('user_session')
    res_service =  RestaurantService()
    user = res_service.get_current_user(token)
    if user:
        return user
    return None




###################################################################################
#   OWNER
##################################################################################
    
@router.get('/owner/dashboard')
def get_owner_dashboard(request:Request):
    user=get_loggedin_user(request)
    if user:
        res_service = RestaurantService()
        res=res_service.get_item()
        total_orders = res_service.get_total_orders_count()
        total_items =res_service.get_total_items()
        pending_orders = res_service.get_pending_orders_count()
        accepted_order = res_service.get_accepted_orders_count()
        return templates.TemplateResponse('owner_dashboard.html',{'request':request,"dishes":res,"total_orders":total_orders ,"pending_orders":pending_orders,"accepted_orders":accepted_order,"total_items":total_items})
    return RedirectResponse('/login')


@router.get('/add/dish')
def get_add_dish_page(request:Request):
    user=get_loggedin_user(request)
    if user: 
       return templates.TemplateResponse('add_dish.html',{'request':request})
    return RedirectResponse('/login')


@router.get('/view/orders')
def get_view_all_orders(request:Request):
    user=get_loggedin_user(request)
    if user:
        res_service = RestaurantService()
        orders = res_service.get_owner_orders()
        print(orders)
        return templates.TemplateResponse('view_orders.html',{'request':request,"orders":orders})
    return {"message":"wnt wrong"}


@router.get('/edit/dish/{item_id}')
def get_edit_dish_page(request:Request,item_id):
    user = get_loggedin_user(request)
    if user:
        res_service = RestaurantService()
        res = res_service.get_edit_dish(item_id)
        data = res.data
        print(data)
        if res:
            return templates.TemplateResponse('edit_dish.html',{"request":request,"dish":data[0]})
    return {"message":"no dish"}



@router.get('/unavailable/{item_id}')
def delete_item(request:Request,item_id):
    user = get_loggedin_user(request)
    if user:
        res_service = RestaurantService()
        res = res_service.unavailable_dish(item_id)
        if res :
            return RedirectResponse('/owner/dashboard',status_code=302)
        return {"message":"Something went wrong"}


@router.post('/add/dish')
def add_dish(request:Request,item_name=Form(...),Description=Form(...),item_price=Form(...),item_image=Form(...),item_status=Form(...)):
    print(item_name)
    print(Description)
    print(item_price,item_image,item_status)
    user = get_loggedin_user(request)
    if user:
        item={
            "item_name":item_name,
            "description":Description,
            "item_price":item_price,
            "item_image":item_image,
            "item_status":item_status
        }
        res_service=RestaurantService()
        res=res_service.add_dish(item)
        if res:
            return RedirectResponse('/owner/dashboard',status_code=302)
        return RedirectResponse('/login',status_code=302)
    

@router.post('/edit/dish/{item_id}')
def update_dish(request:Request,item_id,item_name=Form(...),Description=Form(...),item_price=Form(...),item_image=Form(...),item_status=Form(...)):
    res_service=RestaurantService()
    res = res_service.update_dish(item_id,item_name,Description,item_price,item_image,item_status)
    if res.data:
        return RedirectResponse('/owner/dashboard',status_code=302)
    return {"message":"Something wrong"}



@router.post('/update/order/status')
def update_order_status(request:Request,order_id=Form(...),status=Form(...)):
    res_service = RestaurantService()
    res = res_service.update_order_status(order_id,status)
    if res:
        return RedirectResponse('/view/orders',status_code=302)




#######################################################################################
#    USER
#######################################################################################


@router.get('/user/dashboard')
def get_user_dashboard(request:Request):
    user=get_loggedin_user(request)
    if user : 
        res_service=RestaurantService()
        res = res_service.get_item()    
        return templates.TemplateResponse('user_dashboard.html',{'request':request,"dishes":res})
    return RedirectResponse('/login')


@router.get('/add/order/{item_id}')
def get_order_page(request:Request,item_id):
    user=get_loggedin_user(request)
    if user:
        item=db.table('items').select ('*') .eq ('id',item_id).execute()
        if item.data:
            return templates.TemplateResponse('order.html',{'request':request,'item':item.data[0],'user':user})
        else:
            return {"message":"error happen "}
    return RedirectResponse ('/login',status_code=302)




@router.get('/view/user/orders')
def get_user_order(request:Request):
    user = get_loggedin_user(request)
    if user:
        user_id =user.user.id
        res_service = RestaurantService()
        orders = res_service.get_user_orders(user_id)
        print(orders)
        if orders :
            return templates.TemplateResponse('user_order.html',{'request':request,'orders':orders})
    return {"message":"no orders"}


@router.get('/ai/suggest')
def get_ai_suggest_page(request:Request):
    user = get_loggedin_user(request)
    if user:
        return templates.TemplateResponse('/ai_suggest.html',{'request':request})




@router.post('/add/order')
def add_order(request:Request,item_id=Form(...),item_name=Form(...),item_quantity=Form(...)):
    user=get_loggedin_user(request)
    res_service = RestaurantService()
    print(item_id)
    print(item_name)
    print(item_quantity)
    if user:
        user_id=user.user.id
        item =  res_service.get_item()
        if item:
            item_price=int(item[0]['item_price'])
            qty = int(item_quantity)
            total_amount = item_price*qty

        order = {
            "user_id":user_id,
            "item_id":item_id,
            "item_quantity":item_quantity,
            "total_amount":total_amount,
            "order_status":"Pending"            
        }
        response= res_service.add_order(order)
        if response:
            return RedirectResponse('/user/dashboard',status_code=302)
        return RedirectResponse('/login',status_code=302)


@router.post('/ai/suggest')
async def ai_suggest(request: Request):
    data = await request.json()     
    prompt = data.get("prompt", "")

    ai_response = ask_gemini(prompt)

    return JSONResponse({"response": ai_response})



###################################################################################################
#    AUTH
###################################################################################################






@router.get('/')
def home():
    return RedirectResponse('/login')

@router.get('/signup')
def get_signup_page(request:Request):
    return templates.TemplateResponse('signup.html',{'request':request})


@router.get('/login')
def get_signup_page(request:Request):
    return templates.TemplateResponse('login.html',{'request':request})  


@router.post('/api/signup')
def api_signup(request:Request,email=Form(...),password=Form(...)):
    res_service=RestaurantService()
    user=res_service.signup_restaurant(email,password)
    if user:
        print(email)
        print(password)
        return RedirectResponse('/login',status_code=303)  


@router.post('/api/login')
def api_login(request:Request,email=Form(...),password=Form(...)):
    print(email) 
    print(password) 
    res_service=RestaurantService() 
    user=res_service.login_restaurant(email,password) 
    owner="demo@gmail.com"
    if email == owner:
        response = RedirectResponse('/owner/dashboard',status_code=302)
    else:
        response = RedirectResponse('/user/dashboard',status_code=302)
    response.set_cookie('user_session',user.session.access_token,max_age=3600)
    return response



@router.get('/api/logout')
def api_logout():
    response= RedirectResponse('/login')
    response.delete_cookie("user_session")
    return response




