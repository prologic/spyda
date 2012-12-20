from py import path

from spyda import get_links


def pytest_generate_tests(metafunc):
    tests = []
    for p in path.local(__file__).dirpath().visit(fil="*.html", rec=True):
        s = p.read()
        expected_links = [link for link in p.new(basename="links.txt").readlines(False) if link]
        args = (s, expected_links,)
        tests.append(args)

    metafunc.parametrize(["s", "expected_links"], tests)


def test(s, expected_links):
    actual_links = [element.get("href") for element in get_links(s)]
    assert actual_links == expected_links