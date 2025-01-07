import fnmatch
import re
from abc import ABC, abstractmethod


class AbstractMatcher(ABC):
    @staticmethod
    @abstractmethod
    def get_name():
        raise NotImplementedError

    @abstractmethod
    def is_text_matches_pattern(self, pattern, text):
        raise NotImplementedError


class PlainMatcher(AbstractMatcher):
    @staticmethod
    def get_name():
        return 'plain'

    def is_text_matches_pattern(self, pattern, text):
        return pattern in text


class ReMatcher(AbstractMatcher):
    @staticmethod
    def get_name():
        return 're'

    def is_text_matches_pattern(self, pattern, text):
        return re.search(pattern=pattern, string=text, flags=re.MULTILINE) is not None


class GlobMatcher(AbstractMatcher):
    @staticmethod
    def get_name():
        return 'glob'

    def is_text_matches_pattern(self, pattern, text):
        for line in text.splitlines():
            if fnmatch.fnmatch(name=line.strip(), pat=pattern):
                return True
        return False


class MatcherFactory:
    _matchers = {
        matcher_class.get_name(): matcher_class for matcher_class in (
            PlainMatcher,
            ReMatcher,
            GlobMatcher,
        )
    }

    @classmethod
    def get_by_name(cls, name):
        if name in cls._matchers:
            return cls._matchers[name]()
        return None

    @classmethod
    def get_avaliable_matchers_names(cls):
        return cls._matchers.keys()
