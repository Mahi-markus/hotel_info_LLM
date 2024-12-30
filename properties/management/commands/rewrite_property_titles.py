# this is property_info/management/commands/rewrite_property_titles.py
########################################


import requests
import json
from django.core.management.base import BaseCommand
from django.db import connections
from properties.models import Property

class Command(BaseCommand):
    help = "Rewrite property titles using Ollama model and save to ollama database"

    def handle(self, *args, **options):
        # Connect to the ecommerce database and fetch property titles
        with connections['scraper_db'].cursor() as cursor:
            cursor.execute("SELECT id, title FROM hotels_info LIMIT 5")
            properties = cursor.fetchall()

        for prop_id, title in properties:
            try:
                # Rewrite the title with Ollama
                rewritten_title = self.rewrite_title_with_ollama(title)
                
                # Save to ollama database
                Property.objects.create(
                    original_id=prop_id,
                    original_title=title,
                    rewritten_title=rewritten_title
                )

                self.stdout.write(self.style.SUCCESS(
                    f"Original: {title}\nRewritten: {rewritten_title}\n"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing ID {prop_id}: {str(e)}"))

    def rewrite_title_with_ollama(self, title):
        prompt = (
            "As an e-commerce expert, please change the following product title to make it unique"
            "to be more engaging and SEO-friendly while maintaining accuracy: "
            f"'{title}'"
        )

        response = requests.post(
            "http://ollama:11434/api/generate",
            json={
                "model": "phi",  # Using mistral instead of phi
                "prompt": prompt,
                "system": "You are an e-commerce product title optimization expert. Respond with only the modified and changed title, no explanations."
            }
        )

        if response.status_code == 200:
            try:
                response_data = json.loads(response.text)
                return response_data.get('response', '').strip()
            except json.JSONDecodeError:
                return title
        else:
            self.stdout.write(self.style.WARNING(f"Error from Ollama: {response.text}"))
            return title

##########################################
# Run with:
# docker-compose exec django python manage.py rewrite_property_titles