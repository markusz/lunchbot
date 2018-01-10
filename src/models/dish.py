class Dish:
    def __init__(self, venue, dish, ingredients, price, kcal):
        self.venue = venue
        self.dish = dish
        self.ingredients = ingredients
        self.price = price
        self.kcal = kcal

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.venue, self.dish, self.ingredients, self.price, self.kcal)

    def to_array(self):
        return [
            self.venue,
            self.dish,
            self.ingredients if self.ingredients != None else '-',
            '%0.2f€' % self.price if self.price != None else '-',
            '%s' % self.kcal if self.kcal != None else '-'
        ]
