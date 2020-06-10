# OLX Price Tracker
Hey. This is my third day of 7. This time I decided to get out of ReactJS and create something with Python. I thought about making a simple price-tracker with web scraping, but then I met this [Selenium](https://www.selenium.dev/) and decided to test create something with it. So maybe I didn't use it correctly, but it shows up, this is my first project.

I am using the very popular website in my country, for buying and selling used items. [OLX](https://olx.com.br/). I open it with selenium firefox web driver, make the search and get the HTML information I need. I think maybe later I will take the selenium and leave it with web scraping, as I said, I did it just to test it.

**For now the script is creating a new json file in `/reports`, containing the products found and the best product found.**

## How to Use
```
$ git clone git@github.com:sammarxz/03-olx-price-tracker.git
$ cd 03-olx-price-tracker.git
$ pip install -r requirements.txt
```

edit the `config.py` with the **name, category and region** of product that you will want search and run the `app.py` script

### REQUIRED!
You will need the [geckodriver](https://github.com/mozilla/geckodriver/releases) for this works. Download the latest version and install it in your PC.

```
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux32.tar.gz
$ tar -xvzf geckodriver*
$ sudo mv geckodriver /usr/local/bin/
