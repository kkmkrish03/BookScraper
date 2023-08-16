>>pip3.11 install scrapy
>>scrapy startproject bookscraper <!-- scrapy startproject {scraper_name} -->
>>cd bookscraper/
>>cd bookscraper/spiders/
>>scrapy genspider bookspider books.toscrape.com <!-- scrapy genspider {spider_name} {url_to_scrape} -->
..........
>>pip3.11 install ipython
>>shell = ipython > scrapy.cfg
<!-- scrapy shell
*** issue fix
apt-get install -y liblzma-dev
pip3.11 install backports.lzma
 vi /usr/local/lib/python3.11/lzma.py  or vi /usr/local/python3.*/lib/python3.*/lzma.py
        # Before modification
        from _lzma import *
        from _lzma import _encode_filter_properties, _decode_filter_properties

        # After modification
        try:
            from _lzma import *
            from _lzma import _encode_filter_properties, _decode_filter_properties
        except ImportError:
            from backports.lzma import *
            from backports.lzma import _encode_filter_properties, _decode_filter_properties

instead of scrapy shell, use apt install python3-scrapy after pip uninstall ipython scrapy rm -rf ~/.ipython ~/.config/ipython pip install ipython -->
>>pip install ipython
>>apt install python3-scrapy
<!-- upgrade all pip packages -->
>>pip freeze --local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U 

.......................
>>scrapy list
>>scrapy crawl bookspider
>>scrapy crawl bookspider -o bookdata.csv
>>scrapy crawl bookspider -o bookdata.json

>>sudo apt install mysql-server
>>sudo mysql_secure_installation
>>sudo systemctl start mysql
>>sudo systemctl enable mysql
>>sudo systemctl status mysql
>>mysql -u root -p
>>mysql>CREATE DATABASE scraper;
>>mysql>GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY 'your_password' WITH GRANT OPTION;
>>mysql>USE mysql;
>>mysql>SELECT User, Host, plugin FROM mysql.user;
+------------------+-----------------------+
| User             | plugin                |
+------------------+-----------------------+
| root             | auth_socket           |
| mysql.sys        | mysql_native_password |
| debian-sys-maint | mysql_native_password |
+------------------+-----------------------+
As you can see in the query, the root user is using the auth_socket plugin.

There are two ways to solve this:
 - You can set the root user to use the mysql_native_password plugin
 - You can create a new db_user with you system_user (recommended)

 Option 1.
    >>sudo mysql -u root 
    >>mysql> USE mysql;
    >>mysql> UPDATE user SET plugin='mysql_native_password' WHERE User='root';
    >>mysql> FLUSH PRIVILEGES;
    >>mysql> exit;
    >>sudo service mysql restart

 Option 2. (replace YOUR_SYSTEM_USER with the username you have)
    >>sudo mysql -u root
    >>mysql> USE mysql;
    >>mysql> CREATE USER 'YOUR_SYSTEM_USER'@'localhost' IDENTIFIED BY 'YOUR_PASSWD';
    >>mysql> GRANT ALL PRIVILEGES ON *.* TO 'YOUR_SYSTEM_USER'@'localhost';
    >>mysql> UPDATE user SET plugin='auth_socket' WHERE User='YOUR_SYSTEM_USER';
    >>mysql> FLUSH PRIVILEGES;
    >>mysql> exit;
    >>sudo service mysql restart


>>pip install mysql mysql-connector-python

>>pip install scrapy-rotating-proxies

>>pip install scrapeops-scrapy-proxy-sdk