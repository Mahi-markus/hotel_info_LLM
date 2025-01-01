import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.db import connections
from properties.models import Property, Summary, Description, RatingAndReview
from django.core.management import call_command

@patch('google.generativeai.GenerativeModel')
class RewritePropertyTitlesCommandTests(TestCase):
    databases = {'default', 'scraper_db'}
    
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_cursor.fetchall.return_value = [
            (1, "New York", "Original Hotel Title")
        ]
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor

    @patch('properties.management.commands.rewrite_property_titles.connections')
    def test_command_execution(self, mock_connections, mock_genai):
        """Test the basic execution of the command"""
        # Create mock content response
        mock_content_response = MagicMock()
        mock_content_response.text = "New Hotel Title"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_content_response
        mock_genai.return_value = mock_model
        
        # Set up the mock connection
        mock_connections.__getitem__.return_value = self.mock_connection
        
        # Create test property instance
        Property.objects.create(
            original_id=1,
            rewritten_title="New Hotel Title"
        )
        
        call_command('rewrite_property_titles')

        # Verify that a Property instance exists
        property = Property.objects.filter(original_id=1).first()
        self.assertIsNotNone(property)
        self.assertEqual(property.original_id, 1)
        self.assertEqual(property.rewritten_title, "New Hotel Title")


@patch('google.generativeai.GenerativeModel')
class GenerateSummaryCommandTests(TestCase):
    databases = {'default', 'scraper_db'}
    
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_cursor.fetchall.return_value = [
            (1, "New York", "Hotel Name", None, "100", "4.5", "123 Main St", "40.7", "-74.0", "Deluxe")
        ]
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor

    @patch('properties.management.commands.generate_sum.connections')
    def test_command_execution(self, mock_connections, mock_genai):
        """Test the basic execution of the command"""
        # Create mock content response
        mock_content_response = MagicMock()
        mock_content_response.text = "Generated summary text"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_content_response
        mock_genai.return_value = mock_model
        
        # Set up the mock connection
        mock_connections.__getitem__.return_value = self.mock_connection
        
        # Create test summary instance
        Summary.objects.create(
            hotel_id=1,
            summary="Generated summary text"
        )
        
        call_command('generate_sum')

        # Verify that a Summary instance exists
        summary = Summary.objects.filter(hotel_id=1).first()
        self.assertIsNotNone(summary)
        self.assertEqual(summary.hotel_id, 1)
        self.assertEqual(summary.summary, "Generated summary text")


@patch('google.generativeai.GenerativeModel')
class GenerateRatingReviewCommandTests(TestCase):
    databases = {'default', 'scraper_db'}
    
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_cursor.fetchall.return_value = [
            (1, "New York", "Hotel Name", "100", "4.5", "123 Main St", "40.7", "-74.0", "Deluxe")
        ]
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor

    @patch('properties.management.commands.generate_rating_review.connections')
    def test_command_execution(self, mock_connections, mock_genai):
        """Test the basic execution of the command"""
        # Create two separate response mocks
        mock_rating_response = MagicMock()
        mock_rating_response.text = "4.5"
        
        mock_review_response = MagicMock()
        mock_review_response.text = "Excellent hotel with great amenities"
        
        # Set up the mock model to return different responses for each call
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = [mock_rating_response, mock_review_response]
        mock_genai.return_value = mock_model
        
        # Set up the mock connection
        mock_connections.__getitem__.return_value = self.mock_connection
        
        # Create test rating and review instance
        RatingAndReview.objects.create(
            hotel_id="1",
            rating="4.5",
            review="Excellent hotel with great amenities"
        )
        
        call_command('generate_rating_review')

        # Verify that a RatingAndReview instance exists
        rating_review = RatingAndReview.objects.filter(hotel_id="1").first()
        self.assertIsNotNone(rating_review)
        self.assertEqual(rating_review.hotel_id, "1")
        self.assertEqual(float(rating_review.rating), 4.5)
        self.assertEqual(rating_review.review, "Excellent hotel with great amenities")


@patch('google.generativeai.GenerativeModel')
class GenerateDescriptionCommandTests(TestCase):
    databases = {'default', 'scraper_db'}
    
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_cursor.fetchall.return_value = [
            (1, "New York", "Hotel Name", "100", "4.5", "123 Main St", "40.7", "-74.0", "Deluxe")
        ]
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor

    @patch('properties.management.commands.generate_description.connections')
    def test_command_execution(self, mock_connections, mock_genai):
        """Test the basic execution of the command"""
        # Create mock content response
        mock_content_response = MagicMock()
        mock_content_response.text = "Generated description text"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_content_response
        mock_genai.return_value = mock_model
        
        # Set up the mock connection
        mock_connections.__getitem__.return_value = self.mock_connection
        
        # Create test description instance
        Description.objects.create(
            hotel_id=1,
            description="Generated description text"
        )
        
        call_command('generate_description')

        # Verify that a Description instance exists
        description = Description.objects.filter(hotel_id=1).first()
        self.assertIsNotNone(description)
        self.assertEqual(description.hotel_id, 1)
        self.assertEqual(description.description, "Generated description text")