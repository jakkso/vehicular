import os

"""
Contains Config
"""


class Config:
    """
    Contains configuration values
    """
    hostname = 'smtp.gmail.com'
    port = 587
    database = os.path.join(os.path.dirname(__file__), 'data.db')
