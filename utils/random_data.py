"""
Random data generation helpers for the Turbo Test File Generator project.
"""

import random

from faker import Faker


fake = Faker()


def get_random_sentence():
    """
    Return a random sentence.
    """
    return fake.sentence()


def get_random_paragraph():
    """
    Return a random paragraph.
    """
    return fake.paragraph()


def get_random_text(paragraph_count=3):
    """
    Return multiple paragraphs of random text.

    Args:
        paragraph_count: Number of paragraphs to generate.

    Returns:
        A string containing multiple paragraphs.
    """
    if not isinstance(paragraph_count, int) or isinstance(paragraph_count, bool) or paragraph_count < 1:
        raise ValueError("paragraph_count must be a positive integer.")

    paragraphs = [fake.paragraph() for _ in range(paragraph_count)]
    return "\n\n".join(paragraphs)


def get_random_name():
    """
    Return a random full name.
    """
    return fake.name()


def get_random_email():
    """
    Return a random email address.
    """
    return fake.email()


def get_random_tags(count=3):
    """
    Return a list of random tags.

    Args:
        count: Number of tags to generate.

    Returns:
        A list of words.
    """
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise ValueError("count must be a positive integer.")

    return [fake.word() for _ in range(count)]


def get_random_title():
    """
    Return a short random title.
    """
    return fake.sentence(nb_words=4).rstrip(".")


def get_random_row():
    """
    Return a random row of fake tabular data.

    Returns:
        A dictionary representing one data row.
    """
    return {
        "name": fake.name(),
        "email": fake.email(),
        "company": fake.company(),
        "job_title": fake.job(),
        "city": fake.city(),
        "country": fake.country(),
    }


def get_random_filename_fragment():
    """
    Return a short random word fragment useful for filenames.
    """
    return fake.word().lower()


def set_random_seed(seed):
    """
    Set the seed for repeatable fake data generation.

    Args:
        seed: Integer seed value.
    """
    if seed is None:
        return

    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("seed must be an integer or None.")

    random.seed(seed)
    Faker.seed(seed)
