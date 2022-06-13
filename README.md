# WGCCC Web Payments

<p align="center">
  <img src=https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue></img>
  <img src=https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white></img>
  <img src=https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white></img>

### [NOTICES OF PLAGIARISM]
- autocomplete.js - https://stackoverflow.com/questions/31364880/combine-street-number-and-route-in-address-autocomplete-api
- main.js:4-26 - https://www.w3schools.com/howto/howto_css_modals.asp
- main.js:29-42 - https://github.com/miguelgrinberg/flask-phone-input/blob/master/templates/index.html

RUN: main.py

HTML Templates: www/templates

CSS/JS/Images/Fonts: www/static

### Prerequisites
```sh
pip install -r requirements.txt
```
- flask
- pymysql
- stripe
- python-dotenv
- textmagic

### .ENV file Requirements
- 'SECRET_KEY' - Randomised string for FLASK secret key
- 'SQL_HOST' - Database host
- 'SQL_PORT' - Database port (3306 most of the time)
- 'SQL_USER' - Database username
- 'SQL_PASSWORD' - Database password
- 'SQL_DATABASE' - Database name
- 'STRIPE_API_LIVE_PK' - Stripe live private key
- 'STRIPE_API_LIVE_SK' - Stripe live secret key
- 'STRIPE_API_TEST_PK' - Stripe test suite private key
- 'STRIPE_API_TEST_SK' - Stripe test suite secret key
- 'TEXTMAGIC_USERNAME' - TextMagic username
- 'TEXTMAGIC_API_KEY' - TextMagic api key
