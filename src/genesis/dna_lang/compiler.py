"""
DNA::}{::Lang Compiler

Compiles DNA-Lang AST into executable organisms.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional, Callable
from genesis.dna_lang.ast import (
    ASTNode, ASTVisitor, OrganismNode, GeneNode, EvolveNode,
    StatementNode, EmitStatement, TrackStatement, MeasureStatement,
    MutateStatement, AssignmentStatement, IfStatement, WhileStatement,
    ForStatement, ReturnStatement,
    ExpressionNode, LiteralNode, IdentifierNode, BinaryOpNode,
    UnaryOpNode, CallNode, MemberAccessNode, IndexNode,
    IntegralNode, PartialDerivativeNode, LambdaNode,
    ConditionalNode, ArrayNode, DNABindNode,
)
from genesis.constants import LAMBDA_PHI, PSI_STAR


class CompileError(Exception):
    """Exception raised for compilation errors."""
    pass


class CompiledGene:
    """
    A compiled gene ready for execution.
    
    Attributes:
        name: Gene name.
        gene_type: Type of gene (standard, consciousness, etc.).
        code: Compiled code (callable or value).
        metadata: Additional metadata.
    """
    
    def __init__(
        self,
        name: str,
        gene_type: str,
        code: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        self.name = name
        self.gene_type = gene_type
        self.code = code
        self.metadata = metadata or {}
    
    def __repr__(self) -> str:
        return f"CompiledGene({self.name}, {self.gene_type})"


class CompiledOrganism:
    """
    A compiled organism ready for execution.
    
    Attributes:
        name: Organism name.
        genes: Dictionary of compiled genes.
        evolve_code: Compiled evolution code.
    """
    
    def __init__(
        self,
        name: str,
        genes: Dict[str, CompiledGene],
        evolve_code: Optional[Callable[..., None]] = None
    ) -> None:
        self.name = name
        self.genes = genes
        self.evolve_code = evolve_code
    
    def __repr__(self) -> str:
        return f"CompiledOrganism({self.name}, genes={list(self.genes.keys())})"


class CompilerContext:
    """
    Compilation context tracking variables and state.
    """
    
    def __init__(self) -> None:
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Callable[..., Any]] = {}
        self.current_organism: Optional[str] = None
        
        # Register built-in functions
        self._register_builtins()
    
    def _register_builtins(self) -> None:
        """Register built-in functions."""
        import genesis.core.math as gmath
        
        self.functions.update({
            "sin": gmath.sin,
            "cos": gmath.cos,
            "tan": gmath.tan,
            "exp": gmath.exp,
            "ln": gmath.ln,
            "log": gmath.log,
            "sqrt": gmath.sqrt,
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "len": len,
            "range": range,
            "print": print,
        })
        
        # Add constants
        self.variables.update({
            "Λ_Φ": LAMBDA_PHI,
            "LAMBDA_PHI": LAMBDA_PHI,
            "Ψ*": PSI_STAR,
            "PSI_STAR": PSI_STAR,
            "PI": 3.141592653589793,
            "E": 2.718281828459045,
        })


class ExpressionCompiler(ASTVisitor):
    """
    Compiles expressions to Python callables.
    """
    
    def __init__(self, context: CompilerContext) -> None:
        self.context = context
    
    def compile(self, node: ExpressionNode) -> Any:
        """Compile an expression node."""
        return node.accept(self)
    
    def visit_organism(self, node: OrganismNode) -> Any:
        raise CompileError("Cannot compile organism as expression")
    
    def visit_gene(self, node: GeneNode) -> Any:
        raise CompileError("Cannot compile gene as expression")
    
    def visit_evolve(self, node: EvolveNode) -> Any:
        raise CompileError("Cannot compile evolve as expression")
    
    def visit_statement(self, node: StatementNode) -> Any:
        raise CompileError("Cannot compile statement as expression")
    
    def visit_expression(self, node: ExpressionNode) -> Any:
        """Visit expression nodes by type."""
        if isinstance(node, LiteralNode):
            return node.value
        
        elif isinstance(node, IdentifierNode):
            name = node.name
            if name in self.context.variables:
                return self.context.variables[name]
            if name in self.context.functions:
                return self.context.functions[name]
            # Return as symbol for later resolution
            return lambda ctx=None: ctx.get(name, 0) if ctx else 0
        
        elif isinstance(node, BinaryOpNode):
            left = self.compile(node.left)
            right = self.compile(node.right)
            
            ops = {
                "+": lambda a, b: a + b,
                "-": lambda a, b: a - b,
                "*": lambda a, b: a * b,
                "/": lambda a, b: a / b if b != 0 else float('inf'),
                "^": lambda a, b: a ** b,
                "%": lambda a, b: a % b,
                "==": lambda a, b: a == b,
                "!=": lambda a, b: a != b,
                "<": lambda a, b: a < b,
                ">": lambda a, b: a > b,
                "<=": lambda a, b: a <= b,
                ">=": lambda a, b: a >= b,
                "and": lambda a, b: a and b,
                "or": lambda a, b: a or b,
                "->": lambda a, b: (a, b),  # Arrow creates tuple/mapping
                "=>": lambda a, b: (a, b),  # Fat arrow for lambdas
            }
            
            if node.operator in ops:
                return ops[node.operator](left, right)
            raise CompileError(f"Unknown operator: {node.operator}")
        
        elif isinstance(node, UnaryOpNode):
            operand = self.compile(node.operand)
            
            if node.operator == "-":
                return -operand
            elif node.operator == "!":
                return not operand
            raise CompileError(f"Unknown unary operator: {node.operator}")
        
        elif isinstance(node, CallNode):
            callee = self.compile(node.callee)
            args = [self.compile(arg) for arg in node.arguments]
            
            if callable(callee):
                return callee(*args)
            raise CompileError(f"Cannot call non-callable: {callee}")
        
        elif isinstance(node, MemberAccessNode):
            obj = self.compile(node.object)
            
            if isinstance(obj, dict):
                return obj.get(node.member)
            if hasattr(obj, node.member):
                return getattr(obj, node.member)
            raise CompileError(f"Cannot access member {node.member}")
        
        elif isinstance(node, IndexNode):
            obj = self.compile(node.object)
            index = self.compile(node.index)
            return obj[index]
        
        elif isinstance(node, ArrayNode):
            return [self.compile(elem) for elem in node.elements]
        
        elif isinstance(node, IntegralNode):
            # Simplified numerical integration
            integrand = node.integrand
            variable = node.variable
            
            def integrate(f: Callable[[float], float], a: float = 0, b: float = 1, n: int = 100) -> float:
                """Simple trapezoidal integration."""
                h = (b - a) / n
                result = 0.5 * (f(a) + f(b))
                for i in range(1, n):
                    result += f(a + i * h)
                return result * h
            
            return integrate
        
        elif isinstance(node, PartialDerivativeNode):
            # Simplified numerical differentiation
            func = self.compile(node.function)
            
            def derivative(f: Callable[[float], float], x: float, h: float = 1e-7) -> float:
                """Numerical derivative."""
                return (f(x + h) - f(x - h)) / (2 * h)
            
            if callable(func):
                return lambda x: derivative(func, x)
            return 0
        
        elif isinstance(node, DNABindNode):
            left = self.compile(node.left)
            right = self.compile(node.right)
            # DNA binding creates a linked structure
            return {"left": left, "right": right, "bound": True}
        
        raise CompileError(f"Unknown expression type: {type(node).__name__}")


class Compiler:
    """
    DNA::}{::Lang compiler.
    
    Compiles DNA-Lang AST into executable organisms.
    
    Example:
        >>> compiler = Compiler()
        >>> compiled = compiler.compile(ast)
    """
    
    def __init__(self) -> None:
        self.context = CompilerContext()
        self.expr_compiler = ExpressionCompiler(self.context)
    
    def compile(self, nodes: List[OrganismNode]) -> List[CompiledOrganism]:
        """
        Compile a list of organism AST nodes.
        
        Args:
            nodes: List of organism AST nodes.
            
        Returns:
            List of compiled organisms.
        """
        return [self.compile_organism(node) for node in nodes]
    
    def compile_organism(self, node: OrganismNode) -> CompiledOrganism:
        """Compile a single organism."""
        self.context.current_organism = node.name
        
        genes: Dict[str, CompiledGene] = {}
        for gene_node in node.genes:
            gene = self.compile_gene(gene_node)
            genes[gene.name] = gene
        
        evolve_code = None
        if node.evolve_block:
            evolve_code = self.compile_evolve(node.evolve_block)
        
        return CompiledOrganism(
            name=node.name,
            genes=genes,
            evolve_code=evolve_code
        )
    
    def compile_gene(self, node: GeneNode) -> CompiledGene:
        """Compile a gene definition."""
        code = self.expr_compiler.compile(node.definition)
        
        return CompiledGene(
            name=node.name,
            gene_type=node.gene_type,
            code=code,
            metadata=node.metadata
        )
    
    def compile_evolve(self, node: EvolveNode) -> Callable[..., None]:
        """Compile an evolve block."""
        statements = node.statements
        
        def evolve_function(organism: Any) -> None:
            """Execute the evolution block."""
            for stmt in statements:
                self.execute_statement(stmt, organism)
        
        return evolve_function
    
    def execute_statement(self, stmt: StatementNode, organism: Any) -> None:
        """Execute a statement."""
        if isinstance(stmt, EmitStatement):
            value = self.expr_compiler.compile(stmt.expression)
            if hasattr(organism, 'emit'):
                organism.emit(value)
            else:
                print(f"[EMIT] {value}")
        
        elif isinstance(stmt, TrackStatement):
            if hasattr(organism, 'track'):
                organism.track(stmt.target)
        
        elif isinstance(stmt, MeasureStatement):
            if hasattr(organism, 'measure'):
                organism.measure(stmt.target)
        
        elif isinstance(stmt, MutateStatement):
            if hasattr(organism, 'mutate'):
                organism.mutate(stmt.gene_name)
        
        elif isinstance(stmt, AssignmentStatement):
            value = self.expr_compiler.compile(stmt.value)
            self.context.variables[stmt.target] = value
        
        elif isinstance(stmt, IfStatement):
            condition = self.expr_compiler.compile(stmt.condition)
            if condition:
                for s in stmt.then_block:
                    self.execute_statement(s, organism)
            elif stmt.else_block:
                for s in stmt.else_block:
                    self.execute_statement(s, organism)
        
        elif isinstance(stmt, WhileStatement):
            max_iterations = 10000  # Prevent infinite loops
            iterations = 0
            while self.expr_compiler.compile(stmt.condition):
                for s in stmt.body:
                    self.execute_statement(s, organism)
                iterations += 1
                if iterations >= max_iterations:
                    raise CompileError("While loop exceeded maximum iterations")
        
        elif isinstance(stmt, ForStatement):
            iterable = self.expr_compiler.compile(stmt.iterable)
            for item in iterable:
                self.context.variables[stmt.variable] = item
                for s in stmt.body:
                    self.execute_statement(s, organism)
        
        elif isinstance(stmt, ReturnStatement):
            if stmt.value:
                return self.expr_compiler.compile(stmt.value)
            return None


def compile_source(source: str) -> List[CompiledOrganism]:
    """
    Compile DNA-Lang source code.
    
    Args:
        source: DNA-Lang source code.
        
    Returns:
        List of compiled organisms.
    """
    from genesis.dna_lang.parser import parse
    
    ast = parse(source)
    compiler = Compiler()
    return compiler.compile(ast)
