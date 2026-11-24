# Каталог пицц
PIZZAS = {
    "margherita": "Маргарита",
    "pepperoni": "Пепперони",
    "four_cheese": "Четыре сыра",
    "hawaiian": "Гавайская",
    "napoletano": "Неаполитанская"
}

# Доступные размеры пиццы
SIZES = {
    "small": "Маленькая",
    "medium": "Средняя",
    "large": "Большая"
}

# Каталог напитков
DRINKS = {
    "juice": "Сок",
    "mors": "Морс",
    "tea": "Чай",
    "cola": "Кола",
    "none": "Без напитка"
}

# Формирование inline-клавиатуры
def make_keyboard(catalog):
    return {
        "inline_keyboard": [
            [{"text": name, "callback_data": key}]
            for key, name in catalog.items()
        ]
    }