# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        ## Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                if value is not None:
                    adapter[field_name] = value.strip()
                
        ## Category and product type --> switch to lowecase (standerdisation)
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = str(value).lower().replace(' ', '-')
            
        ## Converting price keys to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if value is not None:
                value = value.replace('£', '')
                adapter[price_key] = float(value)
            else:
                adapter[price_key] = float(0)
            
        ## Extract number of boks in stock from availibility string
        availibility_string = adapter.get('availibility')
        if availibility_string is not None:
            split_string_array = availibility_string.split('(')
            if len(split_string_array) < 2:
                adapter['availibility'] = 0
            else:
                availibility_array = split_string_array[1].split(' ')
                if availibility_array is not None:
                    adapter['availibility'] = int(availibility_array[0])
                else:
                    adapter['availibility'] = int(0)
        else:
            adapter['availibility'] = int(0)
            
        ## convert Review field from string to number
        num_review_string = adapter.get('num_reviews')
        if num_review_string is not None:
            adapter['num_reviews'] = int(num_review_string)
        else:
            adapter['num_reviews'] = int(0)
        
        ## convert image url to right link
        image_string = adapter.get('image')
        if image_string is not None:
            adapter['image'] = f'{adapter.get("url").split("catalogue/")[0]}{image_string.replace("../../", "")}'
            
        ## Convert Star rating from string word to number, eg: One = 1
        star_string = adapter.get("stars")
        if star_string is not None:
            split_stars_array = star_string.split(' ')
            if split_stars_array is not None:
                star_text_value = split_stars_array[1].lower()
                match star_text_value:
                    case "zero":
                        adapter["stars"] = 0
                    case "one":
                        adapter["stars"] = 1
                    case "two":
                        adapter["stars"] = 2
                    case "three":
                        adapter["stars"] = 3
                    case "four":
                        adapter["stars"] = 4
                    case "five":
                        adapter["stars"] = 5
                    case _ :
                        adapter["stars"] = 0
            else:
                 adapter["stars"] = 0
        else:
            adapter["stars"] = 0
            
        return item


import mysql.connector

class SaveToMySQLPipeline:
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings) -> None:
        self.host = settings.get('SQL_HOST', 'localhost')
        self.user = settings.get('SQL_USER', 'root')
        self.password = settings.get('SQL_PASSWORD', '')
        self.database = settings.get('SQL_DATABASE', 'scraper')
        self.enable_sql = settings.get('SQL_ENABLED', False)
        
        if self.enable_sql:
            self.conn = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
            )
            
            self.cur = self.conn.cursor()
            
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS bookscraper (
                        id INT NOT NULL AUTO_INCREMENT,
                        url VARCHAR(255),
                        title TEXT,
                        upc VARCHAR(50) UNIQUE,
                        product_type VARCHAR(50),
                        price_excl_tax DECIMAL,
                        price_incl_tax DECIMAL,
                        tax DECIMAL,
                        price DECIMAL,
                        availability INTEGER,
                        num_reviews INTEGER,
                        stars INTEGER,
                        category VARCHAR(100),
                        description TEXT,
                        image VARCHAR(255),
                        PRIMARY KEY (id)
                    );
                    """
                )
        
    def process_item(self, item, spider):
        if self.enable_sql:
            self.cur.execute(
                """INSERT INTO bookscraper (
                        url, 
                        title, 
                        upc, 
                        product_type, 
                        price_excl_tax, 
                        price_incl_tax, 
                        tax, 
                        price,
                        availability, 
                        num_reviews, 
                        stars, 
                        category, 
                        description, 
                        image
                        ) VALUES (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                            )""",(
                                item['url'],
                                item['title'],
                                item['upc'],
                                item['product_type'],
                                item['price_excl_tax'],
                                item['price_incl_tax'],
                                item['tax'],
                                item['price'],
                                item['availibility'],
                                item['num_reviews'],
                                item['stars'],
                                item['category'],
                                str(item['description']),
                                item['image']
                            ))
            self.conn.commit()
            return item
    
    def close_spider(self, spider):
        if self.enable_sql:
            self.cur.close()
            self.conn.close()