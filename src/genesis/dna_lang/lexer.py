"""
DNA::}{::Lang Lexer

Tokenizes DNA-Lang source code into a stream of tokens for parsing.
The lexer recognizes the novel syntax elements of DNA-Lang including
gene definitions, evolution blocks, and consciousness expressions.
"""

from __future__ import annotations
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Iterator


class TokenType(Enum):
    """Token types for DNA-Lang."""
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Keywords
    ORGANISM = auto()
    GENE = auto()
    EVOLVE = auto()
    EMIT = auto()
    TRACK = auto()
    MEASURE = auto()
    MUTATE = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    
    # Special DNA-Lang keywords
    CONSCIOUSNESS = auto()
    COHERENCE = auto()
    DECOHERENCE = auto()
    CCCE = auto()
    PSI = auto()
    LAMBDA_PHI = auto()
    GAMMA = auto()
    
    # Operators
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /
    CARET = auto()       # ^
    PERCENT = auto()     # %
    
    # Comparison
    EQ = auto()          # ==
    NEQ = auto()         # !=
    LT = auto()          # <
    GT = auto()          # >
    LEQ = auto()         # <=
    GEQ = auto()         # >=
    
    # Assignment and definition
    ASSIGN = auto()      # =
    DEFINE = auto()      # ::=
    ARROW = auto()       # ->
    FAT_ARROW = auto()   # =>
    
    # Delimiters
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    LBRACKET = auto()    # [
    RBRACKET = auto()    # ]
    COMMA = auto()       # ,
    DOT = auto()         # .
    COLON = auto()       # :
    SEMICOLON = auto()   # ;
    
    # Special DNA symbols
    DNA_BIND = auto()    # }{
    INTEGRAL = auto()    # ∫
    PARTIAL = auto()     # ∂
    PSI_SYMBOL = auto()  # Ψ
    PHI_SYMBOL = auto()  # Φ
    GAMMA_SYMBOL = auto()  # Γ
    LAMBDA_SYMBOL = auto() # Λ
    XI_SYMBOL = auto()   # Ξ
    TAU_SYMBOL = auto()  # τ
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    
    # Comments
    COMMENT = auto()


KEYWORDS = {
    "organism": TokenType.ORGANISM,
    "gene": TokenType.GENE,
    "evolve": TokenType.EVOLVE,
    "emit": TokenType.EMIT,
    "track": TokenType.TRACK,
    "measure": TokenType.MEASURE,
    "mutate": TokenType.MUTATE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,
    "consciousness": TokenType.CONSCIOUSNESS,
    "coherence": TokenType.COHERENCE,
    "decoherence": TokenType.DECOHERENCE,
    "ccce": TokenType.CCCE,
    "psi": TokenType.PSI,
    "lambda_phi": TokenType.LAMBDA_PHI,
    "gamma": TokenType.GAMMA,
}


SPECIAL_SYMBOLS = {
    "Ψ": TokenType.PSI_SYMBOL,
    "Φ": TokenType.PHI_SYMBOL,
    "Γ": TokenType.GAMMA_SYMBOL,
    "Λ": TokenType.LAMBDA_SYMBOL,
    "Ξ": TokenType.XI_SYMBOL,
    "τ": TokenType.TAU_SYMBOL,
    "∫": TokenType.INTEGRAL,
    "∂": TokenType.PARTIAL,
}


@dataclass
class Token:
    """
    A lexical token from DNA-Lang source.
    
    Attributes:
        type: The token type.
        value: The token value.
        line: Source line number.
        column: Source column number.
    """
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class LexerError(Exception):
    """Exception raised for lexer errors."""
    
    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"Lexer error at {line}:{column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    """
    DNA::}{::Lang lexer.
    
    Tokenizes source code into a sequence of tokens. Supports the
    full DNA-Lang syntax including Unicode mathematical symbols.
    
    Example:
        >>> lexer = Lexer("organism Test { gene x ::= 1 }")
        >>> tokens = lexer.tokenize()
    """
    
    def __init__(self, source: str) -> None:
        """
        Initialize the lexer.
        
        Args:
            source: The source code to tokenize.
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    @property
    def current_char(self) -> Optional[str]:
        """Get the current character or None if at end."""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """Peek ahead in the source."""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Advance to the next character."""
        char = self.current_char
        if char is not None:
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        return char
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters."""
        while self.current_char is not None and self.current_char in ' \t\r':
            self.advance()
    
    def skip_comment(self) -> None:
        """Skip a comment."""
        if self.current_char == '#':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
        elif self.current_char == '/' and self.peek() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
        elif self.current_char == '/' and self.peek() == '*':
            self.advance()  # /
            self.advance()  # *
            while self.current_char is not None:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # *
                    self.advance()  # /
                    break
                self.advance()
    
    def read_string(self) -> Token:
        """Read a string literal."""
        quote = self.current_char
        start_line = self.line
        start_col = self.column
        self.advance()  # Opening quote
        
        value = ""
        while self.current_char is not None and self.current_char != quote:
            if self.current_char == '\\':
                self.advance()
                escape_char = self.current_char
                if escape_char == 'n':
                    value += '\n'
                elif escape_char == 't':
                    value += '\t'
                elif escape_char == 'r':
                    value += '\r'
                elif escape_char == '\\':
                    value += '\\'
                elif escape_char == quote:
                    value += quote
                else:
                    value += escape_char or ''
                self.advance()
            else:
                value += self.current_char
                self.advance()
        
        if self.current_char is None:
            raise LexerError("Unterminated string", start_line, start_col)
        
        self.advance()  # Closing quote
        return Token(TokenType.STRING, value, start_line, start_col)
    
    def read_number(self) -> Token:
        """Read a numeric literal."""
        start_line = self.line
        start_col = self.column
        value = ""
        
        # Integer part
        while self.current_char is not None and self.current_char.isdigit():
            value += self.current_char
            self.advance()
        
        # Check for float
        if self.current_char == '.' and self.peek() is not None and self.peek().isdigit():
            value += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                value += self.current_char
                self.advance()
            
            # Scientific notation
            if self.current_char in 'eE':
                value += self.current_char
                self.advance()
                if self.current_char in '+-':
                    value += self.current_char
                    self.advance()
                while self.current_char is not None and self.current_char.isdigit():
                    value += self.current_char
                    self.advance()
            
            return Token(TokenType.FLOAT, value, start_line, start_col)
        
        # Scientific notation for integers
        if self.current_char in 'eE':
            value += self.current_char
            self.advance()
            if self.current_char in '+-':
                value += self.current_char
                self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                value += self.current_char
                self.advance()
            return Token(TokenType.FLOAT, value, start_line, start_col)
        
        return Token(TokenType.INTEGER, value, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword."""
        start_line = self.line
        start_col = self.column
        value = ""
        
        while (self.current_char is not None and 
               (self.current_char.isalnum() or self.current_char == '_')):
            value += self.current_char
            self.advance()
        
        # Check for keywords
        token_type = KEYWORDS.get(value.lower(), TokenType.IDENTIFIER)
        return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source.
        
        Returns:
            List of tokens.
        """
        self.tokens = []
        
        while self.current_char is not None:
            start_line = self.line
            start_col = self.column
            char = self.current_char
            
            # Whitespace
            if char in ' \t\r':
                self.skip_whitespace()
                continue
            
            # Newline
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', start_line, start_col))
                self.advance()
                continue
            
            # Comments
            if char == '#' or (char == '/' and self.peek() in '/*'):
                self.skip_comment()
                continue
            
            # Strings
            if char in '"\'':
                self.tokens.append(self.read_string())
                continue
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Special Unicode symbols
            if char in SPECIAL_SYMBOLS:
                self.tokens.append(Token(SPECIAL_SYMBOLS[char], char, start_line, start_col))
                self.advance()
                continue
            
            # Two-character operators
            two_char = char + (self.peek() or '')
            if two_char == '::' and self.peek(2) == '=':
                self.tokens.append(Token(TokenType.DEFINE, '::=', start_line, start_col))
                self.advance()
                self.advance()
                self.advance()
                continue
            
            if two_char == '}{':
                self.tokens.append(Token(TokenType.DNA_BIND, '}{', start_line, start_col))
                self.advance()
                self.advance()
                continue
            
            if two_char == '->':
                self.tokens.append(Token(TokenType.ARROW, '->', start_line, start_col))
                self.advance()
                self.advance()
                continue
            
            if two_char == '=>':
                self.tokens.append(Token(TokenType.FAT_ARROW, '=>', start_line, start_col))
                self.advance()
                self.advance()
                continue
            
            if two_char == '==':
                self.tokens.append(Token(TokenType.EQ, '==', start_line, start_col))
                self.advance()
                self.advance()
                continue
            
            if two_char == '!=':
                self.tokens.append(Token(TokenType.NEQ, '!=', start_line, start_col))
                self.advance()
                self.advance()
                continue
            
            if two_char == '<=':
                self.tokens.append(Token(TokenType.LEQ, '<=', start_line, start_col))
                self.advance()
                self.advance()
                continue
            
            if two_char == '>=':
                self.tokens.append(Token(TokenType.GEQ, '>=', start_line, start_col))
                self.advance()
                self.advance()
                continue
            
            # Single-character tokens
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.STAR,
                '/': TokenType.SLASH,
                '^': TokenType.CARET,
                '%': TokenType.PERCENT,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '=': TokenType.ASSIGN,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                ':': TokenType.COLON,
                ';': TokenType.SEMICOLON,
            }
            
            if char in single_char_tokens:
                self.tokens.append(Token(single_char_tokens[char], char, start_line, start_col))
                self.advance()
                continue
            
            # Unknown character
            raise LexerError(f"Unexpected character: {char!r}", start_line, start_col)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def __iter__(self) -> Iterator[Token]:
        """Iterate over tokens."""
        if not self.tokens:
            self.tokenize()
        return iter(self.tokens)
