from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Python(QSyntaxHighlighter):
    def __init__(self, *args, **kwargs):
        super(QSyntaxHighlighter, self).__init__(*args, **kwargs)
        self.highlighting_rules = []

        # Define text formats for different types of highlighting
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.GlobalColor.blue)
        keyword_format.setFontWeight(99)  # Bold

        string_format = QTextCharFormat()
        string_format.setForeground(Qt.GlobalColor.darkGreen)

        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.GlobalColor.darkGray)
        comment_format.setFontItalic(True)

        number_format = QTextCharFormat()
        number_format.setForeground(Qt.GlobalColor.red)

        # Define regular expressions for the highlighting rules
        keyword_patterns = [
            r'\b' + keyword + r'\b' for keyword in
            ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class',
             'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global',
             'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
             'try', 'while', 'with', 'yield']
        ]

        string_pattern = r'\"[^\"]*\"|\'.*?\''
        comment_pattern = r'#.*'
        number_pattern = r'\b[0-9]+\b'

        self.highlighting_rules.extend(
            (QRegularExpression(pattern), keyword_format) for pattern in keyword_patterns
        )
        self.highlighting_rules.append((QRegularExpression(string_pattern), string_format))
        self.highlighting_rules.append((QRegularExpression(comment_pattern), comment_format))
        self.highlighting_rules.append((QRegularExpression(number_pattern), number_format))

    def highlightBlock(self, text):
        for pattern, char_format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)


class Cpp(QSyntaxHighlighter):
    def __init__(self, *args, **kwargs):
        super(QSyntaxHighlighter, self).__init__(*args, **kwargs)

        self.highlightingRules = []

        # Define keyword format
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.GlobalColor.darkBlue)
        keywordFormat.setFontWeight(75)

        keywords = ["alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor", "bool", "break", "case", "catch", "char", "char8_t", "char16_t", "char32_t", "class", "compl", "concept", "const", "consteval", "constexpr", "const_cast", "continue", "co_await", "co_return", "co_yield", "decltype", "default", "delete", "do", "double", "dynamic_cast", "else", "enum", "explicit", "export", "extern", "false", "float", "for", "friend", "goto", "if", "inline", "int", "long", "mutable", "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq", "private", "protected", "public", "register", "reinterpret_cast", "requires", "return", "short", "signed", "sizeof", "static", "static_assert", "static_cast", "struct", "switch", "template", "this", "thread_local", "throw", "true", "try", "typedef", "typeid", "typename", "union", "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq"]

        for keyword in keywords:
            self.highlightingRules.append((QRegularExpression(f'\\b{keyword}\\b'), keywordFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            while match.hasMatch():
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)
                match = expression.match(text, start + length)


class Sh(QSyntaxHighlighter):
    def __init__(self, *args, **kwargs):
        super(QSyntaxHighlighter, self).__init__(*args, **kwargs)

        self.highlighting_rules = []

        # Keyword format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keyword_list = [
            r'\bif\b', r'\bthen\b', r'\belse\b', r'\bfi\b',
            r'\bfor\b', r'\bin\b', r'\bdo\b', r'\bdone\b',
            r'\bwhile\b', r'\bdone\b', r'\buntil\b', r'\bdone\b',
            r'\bcase\b', r'\besac\b', r'\bfunction\b'
        ]
        for pattern in keyword_list:
            self.highlighting_rules.append((QRegularExpression(pattern), keyword_format))

        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#57A64A"))
        self.highlighting_rules.append((QRegularExpression(r'#[^\n]*'), comment_format))

        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self.highlighting_rules.append((QRegularExpression(r'".*?"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r'\'.*?\''), string_format))

        # Number format
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))
        self.highlighting_rules.append((QRegularExpression(r'\b\d+\b'), number_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


class Html(QSyntaxHighlighter):
    def __init__(self, *args, **kwargs):
        super(QSyntaxHighlighter, self).__init__(*args, **kwargs)
        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.GlobalColor.blue)
        keyword_format.setFontWeight(99)  # Bold

        tag_format = QTextCharFormat()
        tag_format.setForeground(Qt.GlobalColor.magenta)

        attribute_format = QTextCharFormat()
        attribute_format.setForeground(Qt.GlobalColor.darkYellow)

        value_format = QTextCharFormat()
        value_format.setForeground(Qt.GlobalColor.darkGreen)

        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.GlobalColor.darkGray)
        comment_format.setFontItalic(True)

        keyword_patterns = [
            r'\b' + keyword + r'\b' for keyword in
            ['html', 'head', 'body', 'div', 'p', 'h[1-6]', 'span']
        ]

        tag_pattern = r'<\s*\w+\b'
        attribute_pattern = r'\b\w+\s*=\s*\"[^\"]*\"'
        value_pattern = r'\"[^\"]*\"'
        comment_pattern = r'<!--.*-->'

        self.highlighting_rules.extend(
            (QRegularExpression(pattern), keyword_format) for pattern in keyword_patterns
        )
        self.highlighting_rules.append((QRegularExpression(tag_pattern), tag_format))
        self.highlighting_rules.append((QRegularExpression(attribute_pattern), attribute_format))
        self.highlighting_rules.append((QRegularExpression(value_pattern), value_format))
        self.highlighting_rules.append((QRegularExpression(comment_pattern), comment_format))

    def highlightBlock(self, text):
        for pattern, char_format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), char_format)

class Nothing(QSyntaxHighlighter):
    def __init__(self, *args, **kwargs):
        super(QSyntaxHighlighter, self).__init__(*args, *kwargs)
        self.highlighting_rules = []

    def highlightBlock(self, text):
        pass
