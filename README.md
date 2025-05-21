# Personalized News Aggregator 📰

A Django-based web application that delivers personalized news articles to users based on their preferences.
Personalized News Aggregator and Recommendation System is a web-based application that delivers customized news feeds to users based on their selected interests and reading behavior. Built using Django and Python, the system fetches the latest news from multiple sources and applies simple recommendation logic to prioritize content relevant to the user. It also features an admin panel for content management and user administration, making it a scalable solution for personalized content delivery. The project aims to improve user engagement by minimizing information overload and providing meaningful, targeted news recommendations.

## How to Run the Project

1. **Open Two PowerShell Windows**  
   Open two separate PowerShell terminals on your machine.

2. **Navigate to the Project Directory in Both**  
   Example:  
   cd C:\Users\<YourUsername>\Personalized-News-Aggregator

3. **Activate the Virtual Environment in Both**  
   In both terminals, run:  
   .\venv\Scripts\activate

4. **Fetch Latest News in the First Terminal**  
   In the first terminal, run:  
   python manage.py fetch_news

5. **Start the Server in the Second Terminal**  
   In the second terminal, run:  
   python manage.py runserver  
   The server will start and provide a link like:  
   http://127.0.0.1:8000/

6. **Access the Application in Your Browser**  
   Open your browser and navigate to:  
   http://127.0.0.1:8000/

## Features

- Personalized news feed based on user interests
- Admin panel for managing articles and users
- Real-time news fetching from sources
