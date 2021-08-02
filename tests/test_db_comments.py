#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-db-comments
------------

Tests for `django-db-comments` module.
"""

from mock import patch
from psycopg2 import sql

from django.test import TestCase
from django.db import models, DEFAULT_DB_ALIAS
from django.utils.translation import ugettext_lazy as _

from django_db_comments.db_comments import (
    get_comments_for_model,
    add_column_comments_to_database,
    add_table_comments_to_database,
    POSTGRES_COMMENT_SQL,
    POSTGRES_COMMENT_ON_TABLE_SQL,
)


class TestDjangoDbComments(TestCase):
    def test_get_comments_for_model(self):
        class Model(models.Model):
            no_comment = models.TextField()
            verbose_name = models.TextField("This is verbose name")
            help_text = models.TextField(
                help_text="I am really should see this in database"
            )

            class Meta:
                app_label = "tests"

        column_comments = get_comments_for_model(Model)
        self.assertDictEqual(
            column_comments,
            {
                "verbose_name": "This is verbose name",
                "help_text": "I am really should see this in database",
            },
        )

    @patch("django_db_comments.db_comments.connections")
    def test_add_column_comments_to_database(self, mock_connections):
        mock_cursor = mock_connections.__getitem__(
            DEFAULT_DB_ALIAS
        ).cursor.return_value.__enter__.return_value

        model_table = "model"
        table_column = "verbose_name"
        comment = "This is verbose name"

        add_column_comments_to_database({model_table: {table_column: comment}})

        query = POSTGRES_COMMENT_SQL.format(
            sql.Identifier(model_table), sql.Identifier(table_column)
        )

        # Demonstrating assert_* options:
        mock_cursor.execute.assert_called_once()
        mock_cursor.execute.assert_called()
        mock_cursor.execute.assert_called_once_with(query, [comment])

    @patch("django_db_comments.db_comments.connections")
    def test_add_table_comments_to_database(self, mock_connections):
        mock_cursor = mock_connections.__getitem__(
            DEFAULT_DB_ALIAS
        ).cursor.return_value.__enter__.return_value

        model_table = "model"
        comment = "This is verbose name"

        add_table_comments_to_database({model_table: comment})

        query = POSTGRES_COMMENT_ON_TABLE_SQL.format(
            sql.Identifier(model_table), sql.Identifier(comment)
        )

        # Demonstrating assert_* options:
        mock_cursor.execute.assert_called_once()
        mock_cursor.execute.assert_called()
        mock_cursor.execute.assert_called_once_with(query, [comment])

    def test_ugettext_lazy_workaround(self):
        class Model(models.Model):
            # Example from Django auth.User
            is_superuser = models.BooleanField(
                _("superuser status"),
                help_text=_(
                    "Designates that this user has all permissions without "
                    "explicitly assigning them."
                ),
            )

            class Meta:
                app_label = "tests"

        column_comments = get_comments_for_model(Model)
        self.assertDictEqual(
            column_comments,
            {
                "is_superuser": "superuser status | Designates that this user has all "
                "permissions without explicitly assigning them."
            },
        )
