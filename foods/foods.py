import json
from json import *


 def update(to_update: list) -> None:
     with open('foods/foods.json', 'w') as outfile:
         json.dump(to_update, outfile, ensure_ascii=False, indent=4)

 def append(record) -> None:
     with open('foods/foods.json', 'r') as outfile:
         recorder = json.load(outfile)
         recorder.append(record)
         update(recorder)

def check_existance(name: str) -> bool:
     with open('foods/foods.json', 'r') as inputfile:
         checker = json.load(inputfile)
         for objects in checker:
             if objects['name'] == name:
                 return True
         return False

 def delete(name) -> str:
     with open('foods/foods.json', 'r') as infile:
         deleter = json.load(infile)
         for record in deleter:
             if record['name'] == name:
                 deleter.remove(record)
                 update(deleter)
                 return 'Продукт успешно удален'
         return 'Такого продукта не существует'

 def get_food_info(name) -> dict:
     with open('foods/foods.json', 'r') as infile:
         getter = json.load(infile)
         for record in getter:
             if record['name'] == name:
                 return record


