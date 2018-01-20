class Dish:
    def __init__(self, venue, dish, ingredients=None, price=None, kcal=None, src=None):
        self.venue = venue
        self.dish = dish
        self.ingredients = ingredients
        self.price = price
        self.kcal = kcal
        self.src = src

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.venue, self.dish, self.ingredients, self.price, self.kcal)

    def is_cheaper_than(self, price):
        return self.price is None or self.price < price

    def has_less_kcal_than(self, kcal):
        return self.kcal is None or self.kcal < kcal

    def to_array(self):
        return [
            self.venue,
            self.dish,
            self.ingredients if self.ingredients is not None else '-',
            '%0.2f€' % self.price if self.price is not None else '-',
            '%s' % self.kcal if self.kcal is not None else '-'
        ]
