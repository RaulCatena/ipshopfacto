import json

class Faker:
    def generateShoppingList():
        data = [{
            "id": 1,
            "product": "Petit Baguette",
            "amount": 2,
            "price": "CHF 20.58"
            }, {
            "id": 2,
            "product": "Wheat - Soft Kernal Of Wheat",
            "amount": 7,
            "price": "CHF 19.57"
            }, {
            "id": 3,
            "product": "Puree - Passion Fruit",
            "amount": 7,
            "price": "CHF 0.05"
            }, {
            "id": 4,
            "product": "Mushroom - Chanterelle Frozen",
            "amount": 6,
            "price": "CHF 17.49"
            }, {
            "id": 5,
            "product": "Napkin Colour",
            "amount": 2,
            "price": "CHF 6.18"
            }, {
            "id": 6,
            "product": "Bar Mix - Lime",
            "amount": 6,
            "price": "CHF 0.56"
            }, {
            "id": 7,
            "product": "Chips - Doritos",
            "amount": 1,
            "price": "CHF 3.00"
            }, {
            "id": 8,
            "product": "Juice - Orange, 341 Ml",
            "amount": 10,
            "price": "CHF 10.28"
            }, {
            "id": 9,
            "product": "Turkey - Ground. Lean",
            "amount": 1,
            "price": "CHF 21.50"
            }, {
            "id": 10,
            "product": "Sobe - Tropical Energy",
            "amount": 2,
            "price": "CHF 13.31"
            }, {
            "id": 11,
            "product": "Pasta - Cheese / Spinach Bauletti",
            "amount": 3,
            "price": "CHF 6.36"
            }, {
            "id": 12,
            "product": "Rice - Jasmine Sented",
            "amount": 7,
            "price": "CHF 11.83"
            }, {
            "id": 13,
            "product": "Soup Campbells Split Pea And Ham",
            "amount": 2,
            "price": "CHF 24.83"
            }, {
            "id": 14,
            "product": "Wine - Clavet Saint Emilion",
            "amount": 1,
            "price": "CHF 11.16"
            }, {
            "id": 15,
            "product": "Dates",
            "amount": 10,
            "price": "CHF 6.11"
            }, {
            "id": 16,
            "product": "Wine - Jafflin Bourgongone",
            "amount": 6,
            "price": "CHF 12.39"
            }, {
            "id": 17,
            "product": "Muffin - Mix - Strawberry Rhubarb",
            "amount": 6,
            "price": "CHF 23.00"
            }, {
            "id": 18,
            "product": "Plums - Red",
            "amount": 3,
            "price": "CHF 6.12"
            }, {
            "id": 19,
            "product": "Wine - Magnotta - Cab Sauv",
            "amount": 4,
            "price": "CHF 11.79"
            }, {
            "id": 20,
            "product": "Tofu - Firm",
            "amount": 7,
            "price": "CHF 6.30"
            }, {
            "id": 21,
            "product": "V8 - Tropical Blend",
            "amount": 5,
            "price": "CHF 7.96"
            }, {
            "id": 22,
            "product": "Mountain Dew",
            "amount": 8,
            "price": "CHF 2.68"
            }, {
            "id": 23,
            "product": "Pike - Frozen Fillet",
            "amount": 3,
            "price": "CHF 0.29"
            }, {
            "id": 24,
            "product": "Wine - Vidal Icewine Magnotta",
            "amount": 8,
            "price": "CHF 18.14"
            }, {
            "id": 25,
            "product": "Soup - Campbells, Cream Of",
            "amount": 7,
            "price": "CHF 9.67"
            }]
        json_data = json.dumps(data)
        print(json_data)
        return json_data
