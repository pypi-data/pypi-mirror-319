from never_sleep import cli


def test_create_parser():

    parser = cli.create_parser()
    assert parser is not None
