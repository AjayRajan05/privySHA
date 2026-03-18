from privysha.stages.sanitizer import Sanitizer


def test_sanitizer():

    s = Sanitizer()

    result = s.run("Hey bro please analyze dataset")

    assert "hey" not in result  