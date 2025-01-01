import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.db import connections
from properties.models import Property, Summary, Description, RatingAndReview
from django.core.management import call_command
from django.core.management.base import CommandError

class PropertyModelTests(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            original_id=1,
            original_title="Original Hotel",
            rewritten_title="Rewritten Hotel"
        )

    def test_property_str(self):
        """Test the string representation of Property model"""
        expected_str = "Original Hotel -> Rewritten Hotel"
        self.assertEqual(str(self.property), expected_str)

    def test_property_fields(self):
        """Test that all fields are saved correctly"""
        self.assertEqual(self.property.original_id, 1)
        self.assertEqual(self.property.original_title, "Original Hotel")
        self.assertEqual(self.property.rewritten_title, "Rewritten Hotel")
        self.assertIsNotNone(self.property.created_at)

class SummaryModelTests(TestCase):
    def setUp(self):
        self.summary = Summary.objects.create(
            hotel_id=1,
            summary="Test summary content"
        )

    def test_summary_str(self):
        """Test the string representation of Summary model"""
        expected_str = "Summary for Hotel ID: 1"
        self.assertEqual(str(self.summary), expected_str)

    def test_summary_fields(self):
        """Test that all fields are saved correctly"""
        self.assertEqual(self.summary.hotel_id, 1)
        self.assertEqual(self.summary.summary, "Test summary content")

class DescriptionModelTests(TestCase):
    def setUp(self):
        self.description = Description.objects.create(
            hotel_id=1,
            description="Test description content"
        )

    def test_description_str(self):
        """Test the string representation of Description model"""
        expected_str = "Description for Hotel ID: 1"
        self.assertEqual(str(self.description), expected_str)

    def test_description_fields(self):
        """Test that all fields are saved correctly"""
        self.assertEqual(self.description.hotel_id, 1)
        self.assertEqual(self.description.description, "Test description content")

class RatingAndReviewModelTests(TestCase):
    def setUp(self):
        self.rating_review = RatingAndReview.objects.create(
            hotel_id="TEST123",
            rating=4.5,
            review="Great hotel with excellent service"
        )

    def test_rating_review_str(self):
        """Test the string representation of RatingAndReview model"""
        expected_str = "TEST123 - Rating: 4.5"
        self.assertEqual(str(self.rating_review), expected_str)

    def test_rating_review_fields(self):
        """Test that all fields are saved correctly"""
        self.assertEqual(self.rating_review.hotel_id, "TEST123")
        self.assertEqual(self.rating_review.rating, 4.5)
        self.assertEqual(self.rating_review.review, "Great hotel with excellent service")
        self.assertIsNotNone(self.rating_review.created_at)
        self.assertIsNotNone(self.rating_review.updated_at)

@patch('google.generativeai.GenerativeModel')
class RewritePropertyTitlesCommandTests(TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_cursor.fetchall.return_value = [
            (1, "New York", "Original Hotel Title")
        ]
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor

    def test_command_execution(self, mock_genai):
        """Test the basic execution of the command"""
        mock_model = MagicMock()
        mock_model.generate_content().text = "New Hotel Title"
        mock_genai.return_value = mock_model

        with patch.dict(connections.databases, {'scraper_db': {}}):
            with patch('django.db.connections.cursor', return_value=self.mock_cursor):
                call_command('rewrite_property_titles')

        # Verify that a Property instance was created
        property = Property.objects.first()
        self.assertIsNotNone(property)
        self.assertEqual(property.original_id, 1)
        self.assertEqual(property.rewritten_title, "New Hotel Title")

@patch('google.generativeai.GenerativeModel')
class GenerateSummaryCommandTests(TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_cursor.fetchall.return_value = [
            (1, "New York", "Hotel Name", None, "100", "4.5", "123 Main St", "40.7", "-74.0", "Deluxe")
        ]
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor

    def test_command_execution(self, mock_genai):
        """Test the basic execution of the command"""
        mock_model = MagicMock()
        mock_model.generate_content().text = "Generated summary text"
        mock_genai.return_value = mock_model

        with patch.dict(connections.databases, {'scraper_db': {}}):
            with patch('django.db.connections.cursor', return_value=self.mock_cursor):
                call_command('generate_sum')

        # Verify that a Summary instance was created
        summary = Summary.objects.first()
        self.assertIsNotNone(summary)
        self.assertEqual(summary.hotel_id, 1)
        self.assertEqual(summary.summary, "Generated summary text")

@patch('google.generativeai.GenerativeModel')
class GenerateRatingReviewCommandTests(TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_cursor.fetchall.return_value = [
            (1, "New York", "Hotel Name", "100", "4.5", "123 Main St", "40.7", "-74.0", "Deluxe")
        ]
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor

    def test_command_execution(self, mock_genai):
        """Test the basic execution of the command"""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = ["4.5", "Excellent hotel with great amenities"]
        mock_genai.return_value = mock_model

        with patch.dict(connections.databases, {'scraper_db': {}}):
            with patch('django.db.connections.cursor', return_value=self.mock_cursor):
                call_command('generate_rating_review')

        # Verify that a RatingAndReview instance was created
        rating_review = RatingAndReview.objects.first()
        self.assertIsNotNone(rating_review)
        self.assertEqual(rating_review.hotel_id, "1")
        self.assertEqual(float(rating_review.rating), 4.5)
        self.assertEqual(rating_review.review, "Excellent hotel with great amenities")

@patch('google.generativeai.GenerativeModel')
class GenerateDescriptionCommandTests(TestCase):
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_cursor.fetchall.return_value = [
            (1, "New York", "Hotel Name", "100", "4.5", "123 Main St", "40.7", "-74.0", "Deluxe")
        ]
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor

    def test_command_execution(self, mock_genai):
        """Test the basic execution of the command"""
        mock_model = MagicMock()
        mock_model.generate_content().text = "Generated description text"
        mock_genai.return_value = mock_model

        with patch.dict(connections.databases, {'scraper_db': {}}):
            with patch('django.db.connections.cursor', return_value=self.mock_cursor):
                call_command('generate_description')

        # Verify that a Description instance was created
        description = Description.objects.first()
        self.assertIsNotNone(description)
        self.assertEqual(description.hotel_id, 1)
        self.assertEqual(description.description, "Generated description text")