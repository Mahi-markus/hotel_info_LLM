import google.generativeai as genai
from django.core.management.base import BaseCommand
from django.db import connections
from time import sleep
from django.core.management import CommandError
from properties.models import Property

class Command(BaseCommand):
    help = 'Fetch hotel data from scraper_db and use Google Gemini API for title regeneration'

    API_KEY = "AIzaSyCi3Jwp17IjkKPKZODiMkhTzoGFcq3tOeE"

    def setup_model(self, api_key):
        """Configure and return the Gemini model"""
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            return model
        except Exception as e:
            raise CommandError(f"Error setting up model: {str(e)}")

    def generate_text(self, model, prompt, max_tokens, temperature):
        """Generate text using the Gemini model"""
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    'temperature': temperature,
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': max_tokens,
                }
            )
            return response.text
        except Exception as e:
            raise CommandError(f"Error generating text: {str(e)}")

    def handle(self, *args, **kwargs):
        try:
            # Connect to the scraper_db and fetch the hotel data
            with connections['scraper_db'].cursor() as cursor:
                cursor.execute("SELECT id, location, title FROM hotels_info;")
                rows = cursor.fetchall()

            # Hardcoded prompt for title regeneration
            prompt_template = (
                "Generate a catchy and SEO-friendly title for a hotel named '{property_title}' "
                "located in {location}. Please make the title creative, engaging, and SEO-friendly, "
                "considering the location and features of the property. "
                "The title should be different from {property_title}. Only give me the new title. Don't give any options."
            )

            # Initialize the model
            model = self.setup_model(self.API_KEY)

            # Iterate through each row and send the property_title to API
            for row in rows:
                id = row[0]
                location = row[1]
                property_title = row[2]

                # Prepare the prompt using the hardcoded template
                prompt = prompt_template.format(
                    property_title=property_title,
                    location=location
                )

                # Generate text using the model
                generated_title = self.generate_text(
                    model,
                    prompt,
                    max_tokens=256,
                    temperature=0.7
                )

                # Add a small delay between requests to avoid rate limiting
                sleep(1)

                # Save the regenerated title data to the database
                summary_instance, created = Property.objects.update_or_create(
                        original_id=id,
                        original_title = property_title,
                        rewritten_title = generated_title
                         # Ensure correct column mapping
                        
                    )

                # Output the hotel info with regenerated title
                self.stdout.write(self.style.SUCCESS(
                    f"ID: {id}, Original Title: {property_title}, Generated Title: {generated_title}, Location: {location}"
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
