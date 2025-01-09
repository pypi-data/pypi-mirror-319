import logging
import re
from abc import ABC, abstractmethod
from textwrap import indent
from typing import Callable, List, Union

from attrs import define, field
from bs4 import BeautifulSoup, NavigableString, Tag

log = logging.getLogger(__name__)


class HtmlRule(ABC):
    @abstractmethod
    def apply(self, soup: BeautifulSoup) -> BeautifulSoup:
        pass
