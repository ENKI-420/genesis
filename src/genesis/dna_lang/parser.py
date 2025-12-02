"""
DNA::}{::Lang Parser

Parses a token stream into an Abstract Syntax Tree (AST).
"""

from __future__ import annotations
from typing import List, Optional, Any
from genesis.dna_lang.lexer import Token, TokenType, Lexer
from genesis.dna_lang.ast import (
    ASTNode, OrganismNode, GeneNode, EvolveNode,
    StatementNode, EmitStatement, TrackStatement, MeasureStatement,
    MutateStatement, AssignmentStatement, IfStatement, WhileStatement,
    ForStatement, ReturnStatement,
    ExpressionNode, LiteralNode, IdentifierNode, BinaryOpNode,
    UnaryOpNode, CallNode, MemberAccessNode, IndexNode,
    IntegralNode, PartialDerivativeNode, LambdaNode,
    ConditionalNode, ArrayNode, DNABindNode,
)


class ParseError(Exception):
    """Exception raised for parse errors."""
    
    def __init__(self, message: str, token: Token) -> None:
        super().__init__(f"Parse error at {token.line}:{token.column}: {message}")
        self.token = token


class Parser:
    """
    DNA::}{::Lang parser.
    
    Produces an AST from a token stream. Implements a recursive
    descent parser with operator precedence parsing for expressions.
    
    Example:
        >>> lexer = Lexer(source)
        >>> parser = Parser(lexer.tokenize())
        >>> ast = parser.parse()
    """
    
    def __init__(self, tokens: List[Token]) -> None:
        """
        Initialize the parser.
        
        Args:
            tokens: List of tokens from the lexer.
        """
        self.tokens = [t for t in tokens if t.type != TokenType.NEWLINE]
        self.pos = 0
    
    @property
    def current(self) -> Token:
        """Get the current token."""
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[self.pos]
    
    def peek(self, offset: int = 1) -> Token:
        """Peek ahead in the token stream."""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def advance(self) -> Token:
        """Advance to the next token."""
        token = self.current
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def check(self, *types: TokenType) -> bool:
        """Check if current token is one of the given types."""
        return self.current.type in types
    
    def match(self, *types: TokenType) -> bool:
        """Match and consume if current token is one of the given types."""
        if self.check(*types):
            self.advance()
            return True
        return False
    
    def expect(self, token_type: TokenType, message: str = "") -> Token:
        """Expect and consume a specific token type."""
        if not self.check(token_type):
            if not message:
                message = f"Expected {token_type.name}"
            raise ParseError(message, self.current)
        return self.advance()
    
    def parse(self) -> List[OrganismNode]:
        """
        Parse the entire program.
        
        Returns:
            List of organism definitions.
        """
        organisms = []
        
        while not self.check(TokenType.EOF):
            if self.check(TokenType.ORGANISM):
                organisms.append(self.parse_organism())
            else:
                raise ParseError(
                    f"Expected 'organism', got {self.current.value!r}",
                    self.current
                )
        
        return organisms
    
    def parse_organism(self) -> OrganismNode:
        """Parse an organism definition."""
        self.expect(TokenType.ORGANISM)
        
        name_token = self.expect(TokenType.IDENTIFIER, "Expected organism name")
        name = name_token.value
        
        self.expect(TokenType.LBRACE, "Expected '{' after organism name")
        
        genes: List[GeneNode] = []
        evolve_block: Optional[EvolveNode] = None
        
        while not self.check(TokenType.RBRACE, TokenType.EOF):
            if self.check(TokenType.GENE):
                genes.append(self.parse_gene())
            elif self.check(TokenType.EVOLVE):
                if evolve_block is not None:
                    raise ParseError("Multiple evolve blocks not allowed", self.current)
                evolve_block = self.parse_evolve()
            else:
                raise ParseError(
                    f"Expected 'gene' or 'evolve', got {self.current.value!r}",
                    self.current
                )
        
        self.expect(TokenType.RBRACE, "Expected '}' to close organism")
        
        return OrganismNode(name=name, genes=genes, evolve_block=evolve_block)
    
    def parse_gene(self) -> GeneNode:
        """Parse a gene definition."""
        self.expect(TokenType.GENE)
        
        name_token = self.expect(TokenType.IDENTIFIER, "Expected gene name")
        name = name_token.value
        
        self.expect(TokenType.DEFINE, "Expected '::=' after gene name")
        
        definition = self.parse_expression()
        
        # Determine gene type based on name or definition
        gene_type = "standard"
        if name.lower() in ("consciousness", "psi", "ψ"):
            gene_type = "consciousness"
        elif name.lower() in ("coherence",):
            gene_type = "coherence"
        elif name.lower() in ("decoherence", "gamma", "γ"):
            gene_type = "decoherence"
        
        return GeneNode(name=name, definition=definition, gene_type=gene_type)
    
    def parse_evolve(self) -> EvolveNode:
        """Parse an evolve block."""
        self.expect(TokenType.EVOLVE)
        self.expect(TokenType.LBRACE, "Expected '{' after evolve")
        
        statements: List[StatementNode] = []
        
        while not self.check(TokenType.RBRACE, TokenType.EOF):
            statements.append(self.parse_statement())
        
        self.expect(TokenType.RBRACE, "Expected '}' to close evolve block")
        
        return EvolveNode(statements=statements)
    
    def parse_statement(self) -> StatementNode:
        """Parse a statement."""
        if self.check(TokenType.EMIT):
            return self.parse_emit()
        elif self.check(TokenType.MUTATE):
            return self.parse_mutate()
        elif self.check(TokenType.IF):
            return self.parse_if()
        elif self.check(TokenType.WHILE):
            return self.parse_while()
        elif self.check(TokenType.FOR):
            return self.parse_for()
        elif self.check(TokenType.RETURN):
            return self.parse_return()
        else:
            return self.parse_expression_statement()
    
    def parse_emit(self) -> EmitStatement:
        """Parse an emit statement."""
        self.expect(TokenType.EMIT)
        expr = self.parse_expression()
        return EmitStatement(expression=expr)
    
    def parse_mutate(self) -> MutateStatement:
        """Parse a mutate statement."""
        self.expect(TokenType.MUTATE)
        gene_token = self.expect(TokenType.IDENTIFIER, "Expected gene name")
        return MutateStatement(gene_name=gene_token.value)
    
    def parse_if(self) -> IfStatement:
        """Parse an if statement."""
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        
        self.expect(TokenType.LBRACE)
        then_block = []
        while not self.check(TokenType.RBRACE, TokenType.EOF):
            then_block.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        else_block = None
        if self.match(TokenType.ELSE):
            self.expect(TokenType.LBRACE)
            else_block = []
            while not self.check(TokenType.RBRACE, TokenType.EOF):
                else_block.append(self.parse_statement())
            self.expect(TokenType.RBRACE)
        
        return IfStatement(condition=condition, then_block=then_block, else_block=else_block)
    
    def parse_while(self) -> WhileStatement:
        """Parse a while statement."""
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        
        self.expect(TokenType.LBRACE)
        body = []
        while not self.check(TokenType.RBRACE, TokenType.EOF):
            body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        return WhileStatement(condition=condition, body=body)
    
    def parse_for(self) -> ForStatement:
        """Parse a for statement."""
        self.expect(TokenType.FOR)
        var_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.IN)
        iterable = self.parse_expression()
        
        self.expect(TokenType.LBRACE)
        body = []
        while not self.check(TokenType.RBRACE, TokenType.EOF):
            body.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        
        return ForStatement(variable=var_token.value, iterable=iterable, body=body)
    
    def parse_return(self) -> ReturnStatement:
        """Parse a return statement."""
        self.expect(TokenType.RETURN)
        
        value = None
        if not self.check(TokenType.RBRACE, TokenType.EOF):
            value = self.parse_expression()
        
        return ReturnStatement(value=value)
    
    def parse_expression_statement(self) -> StatementNode:
        """Parse an expression statement (possibly assignment)."""
        expr = self.parse_expression()
        
        # Check for assignment
        if self.match(TokenType.ASSIGN):
            if isinstance(expr, IdentifierNode):
                value = self.parse_expression()
                return AssignmentStatement(target=expr.name, value=value)
            raise ParseError("Invalid assignment target", self.current)
        
        # Check for method calls that are statements
        if isinstance(expr, CallNode):
            if isinstance(expr.callee, MemberAccessNode):
                member = expr.callee.member
                if member == "track":
                    if isinstance(expr.callee.object, IdentifierNode):
                        return TrackStatement(target=expr.callee.object.name)
                elif member == "measure":
                    if isinstance(expr.callee.object, IdentifierNode):
                        return MeasureStatement(target=expr.callee.object.name)
        
        # Treat as emit for standalone expressions
        return EmitStatement(expression=expr)
    
    def parse_expression(self) -> ExpressionNode:
        """Parse an expression."""
        return self.parse_arrow()
    
    def parse_arrow(self) -> ExpressionNode:
        """Parse arrow expressions (lowest precedence)."""
        left = self.parse_or()
        
        while self.match(TokenType.ARROW, TokenType.FAT_ARROW):
            op = self.tokens[self.pos - 1].value
            right = self.parse_or()
            left = BinaryOpNode(left=left, operator=op, right=right)
        
        return left
    
    def parse_or(self) -> ExpressionNode:
        """Parse logical or."""
        left = self.parse_and()
        
        while self.current.value == "or":
            self.advance()
            right = self.parse_and()
            left = BinaryOpNode(left=left, operator="or", right=right)
        
        return left
    
    def parse_and(self) -> ExpressionNode:
        """Parse logical and."""
        left = self.parse_equality()
        
        while self.current.value == "and":
            self.advance()
            right = self.parse_equality()
            left = BinaryOpNode(left=left, operator="and", right=right)
        
        return left
    
    def parse_equality(self) -> ExpressionNode:
        """Parse equality comparison."""
        left = self.parse_comparison()
        
        while self.match(TokenType.EQ, TokenType.NEQ):
            op = self.tokens[self.pos - 1].value
            right = self.parse_comparison()
            left = BinaryOpNode(left=left, operator=op, right=right)
        
        return left
    
    def parse_comparison(self) -> ExpressionNode:
        """Parse comparison operators."""
        left = self.parse_term()
        
        while self.match(TokenType.LT, TokenType.GT, TokenType.LEQ, TokenType.GEQ):
            op = self.tokens[self.pos - 1].value
            right = self.parse_term()
            left = BinaryOpNode(left=left, operator=op, right=right)
        
        return left
    
    def parse_term(self) -> ExpressionNode:
        """Parse addition/subtraction."""
        left = self.parse_factor()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.tokens[self.pos - 1].value
            right = self.parse_factor()
            left = BinaryOpNode(left=left, operator=op, right=right)
        
        return left
    
    def parse_factor(self) -> ExpressionNode:
        """Parse multiplication/division."""
        left = self.parse_power()
        
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.tokens[self.pos - 1].value
            right = self.parse_power()
            left = BinaryOpNode(left=left, operator=op, right=right)
        
        return left
    
    def parse_power(self) -> ExpressionNode:
        """Parse exponentiation (right associative)."""
        left = self.parse_unary()
        
        if self.match(TokenType.CARET):
            right = self.parse_power()  # Right associative
            left = BinaryOpNode(left=left, operator="^", right=right)
        
        return left
    
    def parse_unary(self) -> ExpressionNode:
        """Parse unary operators."""
        if self.match(TokenType.MINUS):
            operand = self.parse_unary()
            return UnaryOpNode(operator="-", operand=operand)
        
        if self.match(TokenType.PARTIAL):
            operand = self.parse_unary()
            # Default variable is τ for partial derivatives
            return PartialDerivativeNode(function=operand, variable="τ")
        
        if self.match(TokenType.INTEGRAL):
            integrand = self.parse_primary()
            return IntegralNode(integrand=integrand, variable="τ")
        
        return self.parse_call()
    
    def parse_call(self) -> ExpressionNode:
        """Parse function calls and member access."""
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.LPAREN):
                args = []
                if not self.check(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                expr = CallNode(callee=expr, arguments=args)
            elif self.match(TokenType.DOT):
                member = self.expect(TokenType.IDENTIFIER).value
                expr = MemberAccessNode(object=expr, member=member)
            elif self.match(TokenType.LBRACKET):
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = IndexNode(object=expr, index=index)
            elif self.match(TokenType.DNA_BIND):
                right = self.parse_call()
                expr = DNABindNode(left=expr, right=right)
            else:
                break
        
        return expr
    
    def parse_primary(self) -> ExpressionNode:
        """Parse primary expressions."""
        # Literals
        if self.match(TokenType.INTEGER):
            value = int(self.tokens[self.pos - 1].value)
            return LiteralNode(value=value, literal_type="integer")
        
        if self.match(TokenType.FLOAT):
            value = float(self.tokens[self.pos - 1].value)
            return LiteralNode(value=value, literal_type="float")
        
        if self.match(TokenType.STRING):
            value = self.tokens[self.pos - 1].value
            return LiteralNode(value=value, literal_type="string")
        
        if self.match(TokenType.TRUE):
            return LiteralNode(value=True, literal_type="boolean")
        
        if self.match(TokenType.FALSE):
            return LiteralNode(value=False, literal_type="boolean")
        
        if self.match(TokenType.NULL):
            return LiteralNode(value=None, literal_type="null")
        
        # Special symbols
        if self.match(TokenType.PSI_SYMBOL):
            return IdentifierNode(name="Ψ")
        
        if self.match(TokenType.PHI_SYMBOL):
            return IdentifierNode(name="Φ")
        
        if self.match(TokenType.GAMMA_SYMBOL):
            return IdentifierNode(name="Γ")
        
        if self.match(TokenType.LAMBDA_SYMBOL):
            return IdentifierNode(name="Λ")
        
        if self.match(TokenType.XI_SYMBOL):
            return IdentifierNode(name="Ξ")
        
        if self.match(TokenType.TAU_SYMBOL):
            return IdentifierNode(name="τ")
        
        # Identifiers
        if self.match(TokenType.IDENTIFIER):
            return IdentifierNode(name=self.tokens[self.pos - 1].value)
        
        # Keywords as identifiers
        if self.match(
            TokenType.CONSCIOUSNESS, TokenType.COHERENCE, 
            TokenType.DECOHERENCE, TokenType.CCCE,
            TokenType.PSI, TokenType.LAMBDA_PHI, TokenType.GAMMA
        ):
            return IdentifierNode(name=self.tokens[self.pos - 1].value)
        
        # Grouped expression
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # Array literal
        if self.match(TokenType.LBRACKET):
            elements = []
            if not self.check(TokenType.RBRACKET):
                elements.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    elements.append(self.parse_expression())
            self.expect(TokenType.RBRACKET)
            return ArrayNode(elements=elements)
        
        raise ParseError(f"Unexpected token: {self.current.value!r}", self.current)


def parse(source: str) -> List[OrganismNode]:
    """
    Parse DNA-Lang source code.
    
    Args:
        source: The source code to parse.
        
    Returns:
        List of organism AST nodes.
    """
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
