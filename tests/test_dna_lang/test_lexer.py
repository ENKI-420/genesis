"""Tests for DNA-Lang lexer."""

import pytest
from genesis.dna_lang.lexer import Lexer, TokenType


class TestLexer:
    def test_tokenize_organism(self):
        lexer = Lexer("organism Test {}")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.ORGANISM
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "Test"

    def test_tokenize_bind(self):
        lexer = Lexer("a }{ b")
        tokens = lexer.tokenize()
        assert any(t.type == TokenType.BIND for t in tokens)

    def test_tokenize_number(self):
        lexer = Lexer("42 3.14 1e-8")
        tokens = lexer.tokenize()
        numbers = [t for t in tokens if t.type == TokenType.NUMBER]
        assert len(numbers) == 3
