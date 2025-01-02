# Hotel Information Rewriter using LLM (Django CLI Application)

## Overview

This project is a Django CLI application designed to rewrite property information using the Ollama model. The application fetches property titles and descriptions, rewrites them using an LLM model, and stores the updated information in a PostgreSQL database. Additionally, it generates summaries, ratings, and reviews for each property using the same or other LLM models.

---

## Features

1. Rewrites property titles and descriptions using the Ollama model.
2. Stores the rewritten information in the `properties` table.
3. Generates summaries for properties and saves them in the `summaries` table.
4. Generates ratings and reviews for properties and saves them in the `ratings_reviews` table.
5. Utilizes Docker for easy setup and deployment.
6. Includes unit tests with coverage reports.

---

## Prerequisites

- Python 3.8+
- Docker

---

## Installation

- **Clone the previous scrapy project and run that project as per the readme instructions given there.**
  heres the clone link: https://github.com/Mahi-markus/Scrapy_python

### Create Virtual Environment

```bash
create a new directory(New folder) and open terminal there
```

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Clone the Repository

```bash

git clone https://github.com/Mahi-markus/hotel_info_LLM.git
cd hotel_info_LLM
```

## Delete the volume data(Recommended) :

Open another terminal inside hotel_info_LLM directory and Run the following commands to set up the database:

```bash
docker volume ls
if "rm hotel_info_llm_postgres_data" exists then 
docker volume rm hotel_info_llm_postgres_data

```

### Build and Start Docker Containers

```bash
docker-compose up --build
```
**incase if you see any error just press ctrl-c in order to stop the server and "docker-compose up" again**
---

## Running the Application

### Database Migrations

open another terminal inside hotel_info_LLM directory and Run the following commands to set up the database:

```bash
docker exec -it django python manage.py makemigrations
docker exec -it django python manage.py migrate
```

### Rewrite Property Titles and Descriptions,Generating Summary,Reviews,Rating

Use the CLI command to rewrite property titles and descriptions,Review,Rating and Description generations:

```bash
docker exec -it django python manage.py generate_description
docker exec -it django python manage.py generate_sum
docker exec -it django python manage.py rewrite_property_titles
docker exec -it django python manage.py generate_rating_review
```

**if any of the above generation related commnad line doesnt work at the first try , just run that specific commandline again**
**above commandlines can show "429 Resource error" but it wont cause problem to the overall functionality of the project** 

### Testing

open another terminal inside hotel_info_LLM directory and Run the unit tests with the following commands:

```bash
docker exec -it django python manage.py test properties
```

Generate a coverage report:

```bash
docker exec -it django coverage run manage.py test properties
```

View the coverage report:

```bash
docker exec -it django coverage report
```

---

## Accessing the Admin Panel

To view the tables and manage data via the Django Admin panel:

### Create a Superuser in the terminal

```bash
docker exec -it django python manage.py createsuperuser
```

- Username: `admin`
- Email: _(leave blank)_
- Password: `admin`

### Access Admin Panel

Visit [http://localhost:8000/admin](http://localhost:8000/admin) and log in with the credentials above.

---

## Additional Information

- to stop the docker and remove the container

```bash
ctrl-c   in that specific terminal where docker is runing  and 
docker-compose down
```

### Scraper Database

This project integrates with a scraper database set up using a prior Scrapy project. Ensure that the Scrapy project is configured and running correctly.

---

## Tables

1. **Properties Table**:
   - Fields: -`original_id`
     - `original title`
     - `rewriten title`
2. **Summaries Table**:
   - Fields:
     - `hotel_id`
     - `summary`
3. **Ratings and Reviews Table**:
   - Fields:
     - `hotel_id`
     - `rating`
     - `review`
4. **Description Table**
   - Fields:
   - `hotel_id`
   - `description`

---

## Technologies Used

- **Backend Framework**: Django
- **Database**: PostgreSQL
- **LLM Integration**: Gemini model
- **Testing**: Django Test Framework, Coverage
- **Containerization**: Docker, Docker Compose

---

## Author

Developed by [Mahi Markus](mailto:mrahman61142@gmail.com).
