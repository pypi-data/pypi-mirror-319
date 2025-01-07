from pytest import ExitCode


def run_pytest_file(pytester, test_file_content):
    pytester.makepyfile(test_file_content)
    return pytester.runpytest('-v', '-ra')


def test_failed_match_log_arg(pytester):
    test_file = """
        import logging
        import pytest

        @pytest.mark.xfail_err('network error')
        def test_log():
            logging.error('network error')
            assert False
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.assert_outcomes(xfailed=1)
    assert test_result.ret == ExitCode.OK


def test_failed_match_log_kwarg(pytester):
    test_file = """
        import logging
        import pytest

        @pytest.mark.xfail_err(pattern='network error')
        def test_log():
            logging.error('network error')
            assert False
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.assert_outcomes(xfailed=1)
    assert test_result.ret == ExitCode.OK


def test_failed_match_stdout(pytester):
    test_file = """
        import pytest

        @pytest.mark.xfail_err(pattern='network error')
        def test_print():
            print('network error')
            assert False
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.assert_outcomes(xfailed=1)
    assert test_result.ret == ExitCode.OK


def test_failed_match_stderr(pytester):
    test_file = """
        import sys
        import pytest

        @pytest.mark.xfail_err(pattern='network error')
        def test_print():
            print('network error', file=sys.stderr)
            assert False
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.assert_outcomes(xfailed=1)
    assert test_result.ret == ExitCode.OK


def test_failed_no_match(pytester):
    test_file = """
        import logging
        import pytest

        @pytest.mark.xfail_err(pattern='network error')
        def test_print():
            logging.error('assertion failed')
            assert False
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.assert_outcomes(failed=1)
    assert test_result.ret == ExitCode.TESTS_FAILED


def test_passed_match(pytester):
    test_file = """
        import logging
        import pytest

        @pytest.mark.xfail_err(pattern='network error')
        def test_print():
            logging.error('network error ocurred, retrying')
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.assert_outcomes(passed=1)
    assert test_result.ret == ExitCode.OK


def test_reason(pytester):
    test_file = """
        import logging
        import pytest

        @pytest.mark.xfail_err(pattern='HTTPS connection broken', reason='network failure')
        def test_print():
            logging.error('error downloading file: HTTPS connection broken')
            assert False
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.assert_outcomes(xfailed=1)
    test_result.stdout.re_match_lines([r'^.*XFAIL.*network failure.*$'])
    assert test_result.ret == ExitCode.OK


def test_reason_default_text(pytester):
    test_file = """
        import logging
        import pytest

        @pytest.mark.xfail_err(pattern='HTTPS connection broken')
        def test_print():
            logging.error('error downloading file: HTTPS connection broken')
            assert False
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.assert_outcomes(xfailed=1)
    test_result.stdout.re_match_lines([r'^.*XFAIL.*caplog matches plain pattern \"HTTPS connection broken\".*$'])
    assert test_result.ret == ExitCode.OK


def test_multiple_marks_one_mark_matches(pytester):
    tests_file = """
        import pytest

        @pytest.mark.xfail_err(pattern='network error')
        @pytest.mark.xfail_err(pattern='http error 502')
        class TestSomething:
            def test_http(self):
                print('http error 502')
                assert False

            def test_network(self):
                print('network error')
                assert False
    """
    test_result = run_pytest_file(pytester, tests_file)

    test_result.assert_outcomes(xfailed=2)
    assert test_result.ret == ExitCode.OK


def test_multiple_marks_all_marks_match(pytester):
    tests_file = """
        import pytest

        @pytest.mark.xfail_err(pattern='http error 502', reason='http failure')
        @pytest.mark.xfail_err(pattern='network error', reason='network failure')
        def test_http():
            print('network error')
            print('http error 502')
            assert False
    """
    test_result = run_pytest_file(pytester, tests_file)

    test_result.assert_outcomes(xfailed=1)
    assert test_result.ret == ExitCode.OK


def test_error_required_pattern_arg_is_not_specified(pytester):
    test_file = """
        import pytest

        @pytest.mark.xfail_err
        def test_print():
            pass
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.stdout.re_match_lines([
        '^.*TypeError: Error message pattern should be specified in xfail_err marker argument'])
    assert test_result.ret == ExitCode.INTERNAL_ERROR


def test_failed_match_regexp(pytester):
    test_file = r"""
        import logging
        import pytest

        @pytest.mark.xfail_err(r'^Error: GET api.provider.com\/item\/\d+ HTTP status 502', matcher='re')
        def test_log():
            print('Downloading some data...')
            print('Error: GET api.provider.com/item/12345 HTTP status 502')
            assert False
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.assert_outcomes(xfailed=1)
    assert test_result.ret == ExitCode.OK


def test_failed_match_glob(pytester):
    test_file = r"""
        import logging
        import pytest

        @pytest.mark.xfail_err(r'Error: GET api.provider.com/item/* HTTP status 502', matcher='glob')
        def test_log():
            print('Downloading some data...')
            print('Error: GET api.provider.com/item/12345 HTTP status 502')
            assert False
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.assert_outcomes(xfailed=1)
    assert test_result.ret == ExitCode.OK


def test_error_unsupported_matcher(pytester):
    test_file = """
        import pytest

        @pytest.mark.xfail_err('test', matcher='foo')
        def test_print():
            pass
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.stdout.re_match_lines([
        '^.*TypeError: Unsupported value of matcher argument of xfail_err marker: foo'])
    assert test_result.ret == ExitCode.INTERNAL_ERROR


def test_error_pattern_is_not_str(pytester):
    test_file = """
        import pytest

        @pytest.mark.xfail_err(pattern=1, matcher='re')
        def test_print():
            pass
    """
    test_result = run_pytest_file(pytester, test_file)

    test_result.stdout.re_match_lines([
        (r"^.*TypeError: Error message pattern is not a str object \(got <class 'int'> object\)"),
    ])
    assert test_result.ret == ExitCode.INTERNAL_ERROR
