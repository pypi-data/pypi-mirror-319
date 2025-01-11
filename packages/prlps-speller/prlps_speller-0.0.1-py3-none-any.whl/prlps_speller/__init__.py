from typing import Iterable, Literal

from httpx import AsyncClient


class BaseSpellerError(Exception):
    """базовая ошибка для спеллера."""


class BadArgumentError(BaseSpellerError):
    """некорректный аргумент."""


class YandexSpeller:
    """
    асинхронный спеллер с использованием API Yandex Speller.

    ограничения для одного IP-адреса:

    • на количество обращений к API - 10 000 обращений в сутки;
    • на объем проверяемого текста - 10 000 000 символов в сутки.

    Args:
        format_text: формат текста ('auto', 'html', 'text')
        lang: языки проверки ('en', 'ru', 'uk')
        check_yo: учитывать букву ё
        ignore_urls: игнорировать ссылки
        ignore_tags: игнорировать HTML-теги
        ignore_capitalization: игнорировать регистр
        ignore_digits: игнорировать цифры
        find_repeat_words: искать повторяющиеся слова
    """

    _supported_langs = ['en', 'ru', 'uk']

    def __init__(
            self,
            format_text: Literal['auto', 'html', 'text'] = 'auto',
            lang: Literal['en', 'ru', 'uk'] | list[str] | None = None,
            check_yo: bool = False,
            ignore_urls: bool = False,
            ignore_tags: bool = False,
            ignore_capitalization: bool = False,
            ignore_digits: bool = False,
            find_repeat_words: bool = False,
    ) -> None:
        self._lang: list[str] = []
        self.lang = lang or self._supported_langs

        self._format = 'plain' if format_text == 'auto' else format_text
        self._check_yo = check_yo
        self._ignore_urls = ignore_urls
        self._ignore_tags = ignore_tags
        self._ignore_capitalization = ignore_capitalization
        self._ignore_digits = ignore_digits
        self._find_repeat_words = find_repeat_words

        self._api_query = 'https://speller.yandex.net/services/spellservice.json/checkText'

    @property
    def lang(self) -> list[str]:
        """получить языки проверки"""
        return self._lang

    @lang.setter
    def lang(self, language: str | Iterable[str]) -> None:
        """установить языки проверки"""
        if isinstance(language, str):
            self._lang = [language]
        elif isinstance(language, Iterable):
            self._lang = list(language)

        if any(lang not in self._supported_langs for lang in self._lang):
            raise BadArgumentError(f'неподдерживаемый язык: {self._lang}, поддерживаемые языки: {self._supported_langs}')

    @property
    def _api_options(self) -> int:
        """настройки спеллера"""
        options = 0
        if self._ignore_digits:
            options |= 2
        if self._ignore_urls:
            options |= 4
        if self._find_repeat_words:
            options |= 8
        if self._ignore_capitalization:
            options |= 512
        return options

    async def spell_text(self, text: str) -> list[dict[str, str | int | list[str]]]:
        """
        асинхронная проверка текста на ошибки и вывод списка вариантов исправлений

        Args:
            text: строка с текстом

        Returns:
            список словарей с позициями ошибок и вариантами исправлений
        """
        lang = ','.join(self._lang)
        data = {
            'text': text,
            'options': self._api_options,
            'lang': lang,
            'format': self._format,
        }

        async with AsyncClient() as client:
            response = await client.post(url=self._api_query, data=data)
            if response.status_code != 200:
                raise BaseSpellerError(f'{response.status_code} ошибка API Yandex Speller: {response.text}')
            return response.json()

    async def spelled(self, text: str) -> str:
        """
        Асинхронная проверка текста и исправление ошибок.

        Args:
            text: строка с текстом

        Returns:
            текст с исправленными ошибками в орфографии
        """
        changes = await self.spell_text(text)
        for change in changes:
            if change.get('s'):
                word = change.get('word')
                suggestion = change.get('s', [])[0]
                text = text.replace(word, suggestion)
        return text


__all__ = ['YandexSpeller']
