from src.sample_lambda.handler import get_urls


def test_true_is_true():
    assert True


def test_get_urls():
    assert get_urls() == {"cinch": "https://www.cinch.co.uk/"}
