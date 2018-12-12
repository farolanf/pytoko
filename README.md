# pytoko - Marketplace Website (WIP)

- it uses SSR for speed
- uses vanilla JS and jQuery for simple client-side logic, and Vue for complex ones

Please ignore the old frontend code in the `/app` folder, it stays there for reference as I moved to SSR.

## Requirements

- python 3.7
- python3.7-dev
- elasticsearch

## Setup

- npm install
- pip install -r requirements.txt
- ./resetdb
    - enter details to create superuser
    - it will populate database with some content and rebuild elasticsearch index
    - this will take a minute or two
- python manage.py runserver
- open http://localhost:8000
