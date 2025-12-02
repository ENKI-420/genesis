"""
DNA::}{::Lang Abstract Syntax Tree

Defines the AST node types for the DNA-Lang parser.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict


class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    @abstractmethod
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor for the visitor pattern."""
        pass


class ASTVisitor(ABC):
    """Base class for AST visitors."""
    
    @abstractmethod
    def visit_organism(self, node: OrganismNode) -> Any:
        pass
    
    @abstractmethod
    def visit_gene(self, node: GeneNode) -> Any:
        pass
    
    @abstractmethod
    def visit_evolve(self, node: EvolveNode) -> Any:
        pass
    
    @abstractmethod
    def visit_expression(self, node: ExpressionNode) -> Any:
        pass
    
    @abstractmethod
    def visit_statement(self, node: StatementNode) -> Any:
        pass


@dataclass
class OrganismNode(ASTNode):
    """
    Represents an organism definition.
    
    Syntax:
        organism Name {
            gene ...
            evolve { ... }
        }
    """
    name: str
    genes: List[GeneNode] = field(default_factory=list)
    evolve_block: Optional[EvolveNode] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_organism(self)


@dataclass
class GeneNode(ASTNode):
    """
    Represents a gene definition.
    
    Syntax:
        gene name ::= expression
        gene consciousness ::= Ψ(τ) -> Ψ*
    """
    name: str
    definition: ExpressionNode
    gene_type: str = "standard"  # standard, consciousness, coherence, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_gene(self)


@dataclass
class EvolveNode(ASTNode):
    """
    Represents an evolution block.
    
    Syntax:
        evolve {
            statement1
            statement2
            ...
        }
    """
    statements: List[StatementNode] = field(default_factory=list)
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_evolve(self)


@dataclass
class StatementNode(ASTNode):
    """Base class for statements."""
    pass


@dataclass
class EmitStatement(StatementNode):
    """
    Emit statement for outputting values.
    
    Syntax:
        emit CCCE(Ξ)
        emit consciousness.value
    """
    expression: ExpressionNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_statement(self)


@dataclass
class TrackStatement(StatementNode):
    """
    Track statement for monitoring values.
    
    Syntax:
        consciousness.track()
    """
    target: str
    method: str = "track"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_statement(self)


@dataclass
class MeasureStatement(StatementNode):
    """
    Measure statement for quantum measurement.
    
    Syntax:
        coherence.measure()
    """
    target: str
    method: str = "measure"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_statement(self)


@dataclass
class MutateStatement(StatementNode):
    """
    Mutate statement for gene mutation.
    
    Syntax:
        mutate gene_name
    """
    gene_name: str
    mutation_type: str = "random"
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_statement(self)


@dataclass
class AssignmentStatement(StatementNode):
    """
    Assignment statement.
    
    Syntax:
        variable = expression
    """
    target: str
    value: ExpressionNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_statement(self)


@dataclass
class IfStatement(StatementNode):
    """
    Conditional statement.
    
    Syntax:
        if condition { ... } else { ... }
    """
    condition: ExpressionNode
    then_block: List[StatementNode]
    else_block: Optional[List[StatementNode]] = None
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_statement(self)


@dataclass
class WhileStatement(StatementNode):
    """
    While loop statement.
    
    Syntax:
        while condition { ... }
    """
    condition: ExpressionNode
    body: List[StatementNode] = field(default_factory=list)
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_statement(self)


@dataclass
class ForStatement(StatementNode):
    """
    For loop statement.
    
    Syntax:
        for item in iterable { ... }
    """
    variable: str
    iterable: ExpressionNode
    body: List[StatementNode] = field(default_factory=list)
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_statement(self)


@dataclass
class ReturnStatement(StatementNode):
    """
    Return statement.
    
    Syntax:
        return expression
    """
    value: Optional[ExpressionNode] = None
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_statement(self)


@dataclass
class ExpressionNode(ASTNode):
    """Base class for expressions."""
    pass


@dataclass
class LiteralNode(ExpressionNode):
    """
    Literal value.
    
    Syntax:
        42
        3.14
        "string"
        true
        false
    """
    value: Any
    literal_type: str  # integer, float, string, boolean, null
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class IdentifierNode(ExpressionNode):
    """
    Identifier reference.
    
    Syntax:
        variable_name
        Ψ
        consciousness
    """
    name: str
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class BinaryOpNode(ExpressionNode):
    """
    Binary operation.
    
    Syntax:
        left + right
        left * right
        left -> right
    """
    left: ExpressionNode
    operator: str
    right: ExpressionNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class UnaryOpNode(ExpressionNode):
    """
    Unary operation.
    
    Syntax:
        -x
        !x
        ∂Ψ
    """
    operator: str
    operand: ExpressionNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class CallNode(ExpressionNode):
    """
    Function or method call.
    
    Syntax:
        func(arg1, arg2)
        object.method(arg)
        CCCE(Ξ)
    """
    callee: ExpressionNode
    arguments: List[ExpressionNode] = field(default_factory=list)
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class MemberAccessNode(ExpressionNode):
    """
    Member access.
    
    Syntax:
        object.member
        consciousness.value
    """
    object: ExpressionNode
    member: str
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class IndexNode(ExpressionNode):
    """
    Index access.
    
    Syntax:
        array[index]
        K[τ, τ']
    """
    object: ExpressionNode
    index: ExpressionNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class IntegralNode(ExpressionNode):
    """
    Integral expression.
    
    Syntax:
        ∫K(τ,τ')Ψ(τ')dτ'
    """
    integrand: ExpressionNode
    variable: str
    lower_bound: Optional[ExpressionNode] = None
    upper_bound: Optional[ExpressionNode] = None
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class PartialDerivativeNode(ExpressionNode):
    """
    Partial derivative expression.
    
    Syntax:
        ∂_τΨ
        ∂Ψ/∂τ
    """
    function: ExpressionNode
    variable: str
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class LambdaNode(ExpressionNode):
    """
    Lambda expression.
    
    Syntax:
        (x, y) => x + y
        τ -> Ψ(τ)
    """
    parameters: List[str]
    body: ExpressionNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class ConditionalNode(ExpressionNode):
    """
    Conditional expression (ternary).
    
    Syntax:
        condition ? then_expr : else_expr
    """
    condition: ExpressionNode
    then_expr: ExpressionNode
    else_expr: ExpressionNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class ArrayNode(ExpressionNode):
    """
    Array literal.
    
    Syntax:
        [1, 2, 3]
    """
    elements: List[ExpressionNode] = field(default_factory=list)
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)


@dataclass
class DNABindNode(ExpressionNode):
    """
    DNA binding expression.
    
    Syntax:
        left }{ right
    """
    left: ExpressionNode
    right: ExpressionNode
    
    def accept(self, visitor: ASTVisitor) -> Any:
        return visitor.visit_expression(self)
