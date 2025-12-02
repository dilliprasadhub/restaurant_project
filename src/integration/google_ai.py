from google import genai
from ..repositories.restaurant_repository import RestaurantRepository
import os 
from dotenv import load_dotenv

load_dotenv()



client = genai.Client(api_key=os.getenv('api_key'))

res_service = RestaurantRepository()

def ask_gemini(prompt: str):
    
    items = res_service.get_menu_items()
    menu_text = res_service.format_menu_items(items)

    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f'''
        You are the official AI assistant of the restaurant “Crunchy Kitchen”.

        Here is the restaurant menu from the real database:
        {menu_text}

        🎯 RULES:
        - Always answer as Crunchy Kitchen’s assistant.
        - Recommend only Crunchy Kitchen menu items.
        - If user asks food suggestions → suggest ONLY from the menu above.
        - If user asks for a dish not in the menu → say:
          “Sorry, we don’t have that item at Crunchy Kitchen. Here are similar dishes…”
        - If question is not related to restaurant/food → give a short answer and say:
          “This is outside Crunchy Kitchen services.”
        - If no data available → say:
          “I don’t have the information for that.”

        USER ASKED: {prompt}
        '''
    )
    
    return response.text
