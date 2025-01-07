from dataclasses import dataclass

import pytest

from pytest_errxfail.matchers import AbstractMatcher, MatcherFactory


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'xfail_err(pattern, *, matcher="plain", reason=None): '
        'mark a failed test as xfailed if the captured output contains the specified string pattern',
    )


@dataclass
class XfailErrMarkerParams:
    message_pattern: str
    matcher: AbstractMatcher
    reason: str


def parse_marker_args(marker):
    message_pattern = marker.args[0] if marker.args else marker.kwargs.get('pattern')
    matcher_name = marker.kwargs.get('matcher', 'plain')
    reason = marker.kwargs.get('reason')

    matcher = MatcherFactory.get_by_name(matcher_name)
    if not matcher:
        raise TypeError(f'Unsupported value of matcher argument of xfail_err marker: {matcher_name}. '
                        f'Possible values: {MatcherFactory.get_avaliable_matchers_names()}')
    if message_pattern is None:
        raise TypeError('Error message pattern should be specified in xfail_err marker argument')
    elif not isinstance(message_pattern, str):
        raise TypeError(f'Error message pattern is not a str object (got {type(message_pattern)} object)')

    return XfailErrMarkerParams(message_pattern=message_pattern,
                                matcher=matcher,
                                reason=reason)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    if call.when != 'call':
        return

    for marker in item.iter_markers('xfail_err'):
        try:
            params = parse_marker_args(marker)
        except Exception as ex:
            outcome.force_exception(ex)
            break

        result = outcome.get_result()
        if result.outcome == 'failed':
            test_outputs = {
                'caplog': result.caplog,
                'stdout': result.capstdout,
                'stderr': result.capstderr,
            }
            for output_name in test_outputs:
                is_output_matches = params.matcher.is_text_matches_pattern(pattern=params.message_pattern,
                                                                           text=test_outputs[output_name])
                if is_output_matches:
                    result.outcome = 'skipped'
                    reason_defaut = (f'{output_name} matches {params.matcher.get_name()} pattern '
                                     f'"{params.message_pattern}"')
                    result.wasxfail = f'reason: {params.reason if params.reason else reason_defaut}'
                    outcome.force_result(result)
                    break
