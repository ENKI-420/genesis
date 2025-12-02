/**
 * DNA-Lang Parser
 *
 * Parses DNA-Lang tokens into an Abstract Syntax Tree (AST).
 */

import { Token, TokenType } from './lexer';

// AST Node Types
export interface ASTNode {
  type: string;
  line: number;
  column: number;
}

export interface ProgramNode extends ASTNode {
  type: 'Program';
  organisms: OrganismNode[];
}

export interface OrganismNode extends ASTNode {
  type: 'Organism';
  name: string;
  genes: GeneNode[];
  traits: TraitNode[];
  membrane?: MembraneNode;
}

export interface GeneNode extends ASTNode {
  type: 'Gene';
  name: string;
  parameters: ParameterNode[];
  expression: ExpressionNode;
}

export interface TraitNode extends ASTNode {
  type: 'Trait';
  name: string;
  value: ExpressionNode;
}

export interface MembraneNode extends ASTNode {
  type: 'Membrane';
  permeability: number;
  receptors: string[];
}

export interface ParameterNode extends ASTNode {
  type: 'Parameter';
  name: string;
  defaultValue?: ExpressionNode;
}

export interface ExpressionNode extends ASTNode {
  type: 'Expression';
  kind: 'number' | 'string' | 'identifier' | 'bind' | 'transcribe' | 'call';
  value?: string | number;
  left?: ExpressionNode;
  right?: ExpressionNode;
  callee?: string;
  arguments?: ExpressionNode[];
}

export class Parser {
  private tokens: Token[];
  private pos: number = 0;

  constructor(tokens: Token[]) {
    // Filter out comments and newlines for simpler parsing
    this.tokens = tokens.filter(t =>
      t.type !== TokenType.COMMENT &&
      t.type !== TokenType.NEWLINE
    );
  }

  /**
   * Parse the token stream into an AST.
   */
  parse(): ProgramNode {
    const organisms: OrganismNode[] = [];

    while (!this.isAtEnd()) {
      if (this.check(TokenType.ORGANISM)) {
        organisms.push(this.parseOrganism());
      } else {
        this.advance();
      }
    }

    return {
      type: 'Program',
      organisms,
      line: 1,
      column: 1,
    };
  }

  private isAtEnd(): boolean {
    return this.peek().type === TokenType.EOF;
  }

  private peek(): Token {
    return this.tokens[this.pos];
  }

  private previous(): Token {
    return this.tokens[this.pos - 1];
  }

  private check(type: TokenType): boolean {
    if (this.isAtEnd()) return false;
    return this.peek().type === type;
  }

  private advance(): Token {
    if (!this.isAtEnd()) this.pos++;
    return this.previous();
  }

  private consume(type: TokenType, message: string): Token {
    if (this.check(type)) return this.advance();
    throw new Error(`${message} at line ${this.peek().line}, column ${this.peek().column}`);
  }

  private parseOrganism(): OrganismNode {
    const orgToken = this.consume(TokenType.ORGANISM, 'Expected organism keyword');
    const nameToken = this.consume(TokenType.IDENTIFIER, 'Expected organism name');

    this.consume(TokenType.LBRACE, 'Expected { after organism name');

    const genes: GeneNode[] = [];
    const traits: TraitNode[] = [];
    let membrane: MembraneNode | undefined;

    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      if (this.check(TokenType.GENE)) {
        genes.push(this.parseGene());
      } else if (this.check(TokenType.TRAIT)) {
        traits.push(this.parseTrait());
      } else if (this.check(TokenType.MEMBRANE)) {
        membrane = this.parseMembrane();
      } else {
        this.advance();
      }
    }

    this.consume(TokenType.RBRACE, 'Expected } after organism body');

    return {
      type: 'Organism',
      name: nameToken.value,
      genes,
      traits,
      membrane,
      line: orgToken.line,
      column: orgToken.column,
    };
  }

  private parseGene(): GeneNode {
    const geneToken = this.consume(TokenType.GENE, 'Expected gene keyword');
    const nameToken = this.consume(TokenType.IDENTIFIER, 'Expected gene name');

    const parameters: ParameterNode[] = [];

    if (this.check(TokenType.LPAREN)) {
      this.advance();
      if (!this.check(TokenType.RPAREN)) {
        do {
          parameters.push(this.parseParameter());
        } while (this.check(TokenType.COMMA) && this.advance());
      }
      this.consume(TokenType.RPAREN, 'Expected ) after parameters');
    }

    this.consume(TokenType.CODON, 'Expected : after gene declaration');

    const expression = this.parseExpression();

    return {
      type: 'Gene',
      name: nameToken.value,
      parameters,
      expression,
      line: geneToken.line,
      column: geneToken.column,
    };
  }

  private parseTrait(): TraitNode {
    const traitToken = this.consume(TokenType.TRAIT, 'Expected trait keyword');
    const nameToken = this.consume(TokenType.IDENTIFIER, 'Expected trait name');
    this.consume(TokenType.CODON, 'Expected : after trait name');
    const value = this.parseExpression();

    return {
      type: 'Trait',
      name: nameToken.value,
      value,
      line: traitToken.line,
      column: traitToken.column,
    };
  }

  private parseMembrane(): MembraneNode {
    const memToken = this.consume(TokenType.MEMBRANE, 'Expected membrane keyword');
    this.consume(TokenType.LBRACE, 'Expected { after membrane');

    let permeability = 1.0;
    const receptors: string[] = [];

    while (!this.check(TokenType.RBRACE) && !this.isAtEnd()) {
      if (this.check(TokenType.IDENTIFIER)) {
        const id = this.advance();
        if (id.value.toLowerCase() === 'permeability') {
          this.consume(TokenType.CODON, 'Expected :');
          const num = this.consume(TokenType.NUMBER, 'Expected number');
          permeability = parseFloat(num.value);
        } else if (id.value.toLowerCase() === 'receptors') {
          this.consume(TokenType.CODON, 'Expected :');
          this.consume(TokenType.LBRACKET, 'Expected [');
          while (!this.check(TokenType.RBRACKET) && !this.isAtEnd()) {
            const rec = this.consume(TokenType.IDENTIFIER, 'Expected receptor name');
            receptors.push(rec.value);
            if (this.check(TokenType.COMMA)) this.advance();
          }
          this.consume(TokenType.RBRACKET, 'Expected ]');
        }
      } else {
        this.advance();
      }
    }

    this.consume(TokenType.RBRACE, 'Expected } after membrane body');

    return {
      type: 'Membrane',
      permeability,
      receptors,
      line: memToken.line,
      column: memToken.column,
    };
  }

  private parseParameter(): ParameterNode {
    const nameToken = this.consume(TokenType.IDENTIFIER, 'Expected parameter name');

    return {
      type: 'Parameter',
      name: nameToken.value,
      line: nameToken.line,
      column: nameToken.column,
    };
  }

  private parseExpression(): ExpressionNode {
    return this.parseBind();
  }

  private parseBind(): ExpressionNode {
    let left = this.parseTranscribe();

    while (this.check(TokenType.BIND)) {
      const op = this.advance();
      const right = this.parseTranscribe();
      left = {
        type: 'Expression',
        kind: 'bind',
        left,
        right,
        line: op.line,
        column: op.column,
      };
    }

    return left;
  }

  private parseTranscribe(): ExpressionNode {
    let left = this.parsePrimary();

    while (this.check(TokenType.TRANSCRIBE)) {
      const op = this.advance();
      const right = this.parsePrimary();
      left = {
        type: 'Expression',
        kind: 'transcribe',
        left,
        right,
        line: op.line,
        column: op.column,
      };
    }

    return left;
  }

  private parsePrimary(): ExpressionNode {
    if (this.check(TokenType.NUMBER)) {
      const token = this.advance();
      return {
        type: 'Expression',
        kind: 'number',
        value: parseFloat(token.value),
        line: token.line,
        column: token.column,
      };
    }

    if (this.check(TokenType.STRING)) {
      const token = this.advance();
      return {
        type: 'Expression',
        kind: 'string',
        value: token.value,
        line: token.line,
        column: token.column,
      };
    }

    if (this.check(TokenType.IDENTIFIER)) {
      const token = this.advance();

      // Check for function call
      if (this.check(TokenType.LPAREN)) {
        this.advance();
        const args: ExpressionNode[] = [];
        if (!this.check(TokenType.RPAREN)) {
          do {
            args.push(this.parseExpression());
          } while (this.check(TokenType.COMMA) && this.advance());
        }
        this.consume(TokenType.RPAREN, 'Expected )');

        return {
          type: 'Expression',
          kind: 'call',
          callee: token.value,
          arguments: args,
          line: token.line,
          column: token.column,
        };
      }

      return {
        type: 'Expression',
        kind: 'identifier',
        value: token.value,
        line: token.line,
        column: token.column,
      };
    }

    if (this.check(TokenType.LPAREN)) {
      this.advance();
      const expr = this.parseExpression();
      this.consume(TokenType.RPAREN, 'Expected )');
      return expr;
    }

    throw new Error(
      `Unexpected token ${this.peek().type} at line ${this.peek().line}, column ${this.peek().column}`
    );
  }
}

/**
 * Parse DNA-Lang tokens into an AST.
 */
export function parse(tokens: Token[]): ProgramNode {
  return new Parser(tokens).parse();
}
