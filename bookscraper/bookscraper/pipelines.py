from itemadapter import ItemAdapter

STARS_MAPPING = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all the whitespaces from the strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        # To lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        # Keep only the number of the available books
        availability_string = adapter.get('availability')
        availability_numeric = ''.join(c for c in availability_string if c.isnumeric())
        adapter['availability'] = int(availability_numeric)

        # Convert the number of reviews to an int
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        # Stars --> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        adapter['stars'] = STARS_MAPPING.get(stars_text_value, 0)

        return item
