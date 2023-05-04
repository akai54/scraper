from itemadapter import ItemAdapter

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all the whitespaces from the strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'descryption':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        # To lowercase
        lowercase_fields_names = ['category', 'product_type']
        for lowercase_field_name in lowercase_fields_names:
            value = adapter.get(lowercase_field_name)
            adapter[lowercase_field_name] = value.lower()

        # Keep only the number of the books
        availabilty_string = adapter.get('availabilty')
        split_string_array = availabilty_string.split('()')
        if len(split_string_array) < 2:
            adapter['availabilty'] = 0
        else:
            availabilty_array = split_string_array[1].split(' ')
            adapter['availabilty'] = int(availabilty_array[0])

        # Convert the number of reviews to an int
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        # Stars --> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5

        return item
