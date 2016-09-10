from pygments.lexer import RegexLexer
from pygments.token import Keyword

__all__ = ["OSLexer"]


class OSLexer(RegexLexer):
    name = 'OSShell'
    aliases = ['osshell']
    filenames = ['*.osshell']

    tokens = {
        'root': [(r'\bserver\b', Keyword),
                 (r'\bimage\b', Keyword)],
    }

