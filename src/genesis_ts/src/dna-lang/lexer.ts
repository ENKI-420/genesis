/**
 * DNA-Lang Lexer
 *
 * Tokenizes DNA-Lang source code into tokens for parsing.
 */

export enum TokenType {
  // Keywords
  ORGANISM = 'ORGANISM',
  GENE = 'GENE',
  TRAIT = 'TRAIT',
  EXPRESS = 'EXPRESS',
  MUTATE = 'MUTATE',
  EVOLVE = 'EVOLVE',
  MEMBRANE = 'MEMBRANE',
  NUCLEUS = 'NUCLEUS',
  MITOCHONDRIA = 'MITOCHONDRIA',
  
  // Operators
  BIND = 'BIND',         // }{
  TRANSCRIBE = 'TRANSCRIBE', // ->
  TRANSLATE = 'TRANSLATE',   // =>
  REPLICATE = 'REPLICATE',   // ><
  SPLICE = 'SPLICE',     // |
  CODON = 'CODON',       // :
  HELIX = 'HELIX',       // ~
  
  // Literals
  IDENTIFIER = 'IDENTIFIER',
  NUMBER = 'NUMBER',
  STRING = 'STRING',
  
  // Delimiters
  LPAREN = 'LPAREN',     // (
  RPAREN = 'RPAREN',     // )
  LBRACE = 'LBRACE',     // {
  RBRACE = 'RBRACE',     // }
  LBRACKET = 'LBRACKET', // [
  RBRACKET = 'RBRACKET', // ]
  COMMA = 'COMMA',       // ,
  SEMICOLON = 'SEMICOLON', // ;
  
  // Special
  COMMENT = 'COMMENT',
  NEWLINE = 'NEWLINE',
  EOF = 'EOF',
  ERROR = 'ERROR',
}

export interface Token {
  type: TokenType;
  value: string;
  line: number;
  column: number;
}

const KEYWORDS: Record<string, TokenType> = {
  'organism': TokenType.ORGANISM,
  'gene': TokenType.GENE,
  'trait': TokenType.TRAIT,
  'express': TokenType.EXPRESS,
  'mutate': TokenType.MUTATE,
  'evolve': TokenType.EVOLVE,
  'membrane': TokenType.MEMBRANE,
  'nucleus': TokenType.NUCLEUS,
  'mitochondria': TokenType.MITOCHONDRIA,
};

export class Lexer {
  private source: string;
  private pos: number = 0;
  private line: number = 1;
  private column: number = 1;
  private tokens: Token[] = [];

  constructor(source: string) {
    this.source = source;
  }

  /**
   * Tokenize the entire source.
   */
  tokenize(): Token[] {
    while (!this.isAtEnd()) {
      this.scanToken();
    }
    this.tokens.push({
      type: TokenType.EOF,
      value: '',
      line: this.line,
      column: this.column,
    });
    return this.tokens;
  }

  private isAtEnd(): boolean {
    return this.pos >= this.source.length;
  }

  private peek(): string {
    if (this.isAtEnd()) return '\0';
    return this.source[this.pos];
  }

  private peekNext(): string {
    if (this.pos + 1 >= this.source.length) return '\0';
    return this.source[this.pos + 1];
  }

  private advance(): string {
    const ch = this.source[this.pos];
    this.pos++;
    if (ch === '\n') {
      this.line++;
      this.column = 1;
    } else {
      this.column++;
    }
    return ch;
  }

  private addToken(type: TokenType, value: string): void {
    this.tokens.push({
      type,
      value,
      line: this.line,
      column: this.column - value.length,
    });
  }

  private scanToken(): void {
    const ch = this.advance();

    switch (ch) {
      // Single character tokens
      case '(': this.addToken(TokenType.LPAREN, ch); break;
      case ')': this.addToken(TokenType.RPAREN, ch); break;
      case '[': this.addToken(TokenType.LBRACKET, ch); break;
      case ']': this.addToken(TokenType.RBRACKET, ch); break;
      case ',': this.addToken(TokenType.COMMA, ch); break;
      case ';': this.addToken(TokenType.SEMICOLON, ch); break;
      case ':': this.addToken(TokenType.CODON, ch); break;
      case '~': this.addToken(TokenType.HELIX, ch); break;
      case '|': this.addToken(TokenType.SPLICE, ch); break;

      // Two-character tokens
      case '}':
        if (this.peek() === '{') {
          this.advance();
          this.addToken(TokenType.BIND, '}{');
        } else {
          this.addToken(TokenType.RBRACE, ch);
        }
        break;

      case '{':
        this.addToken(TokenType.LBRACE, ch);
        break;

      case '-':
        if (this.peek() === '>') {
          this.advance();
          this.addToken(TokenType.TRANSCRIBE, '->');
        } else {
          // Might be part of a number
          if (this.isDigit(this.peek())) {
            this.scanNumber('-');
          } else {
            this.addToken(TokenType.ERROR, ch);
          }
        }
        break;

      case '=':
        if (this.peek() === '>') {
          this.advance();
          this.addToken(TokenType.TRANSLATE, '=>');
        } else {
          this.addToken(TokenType.ERROR, ch);
        }
        break;

      case '>':
        if (this.peek() === '<') {
          this.advance();
          this.addToken(TokenType.REPLICATE, '><');
        } else {
          this.addToken(TokenType.ERROR, ch);
        }
        break;

      // Comments
      case '#':
        this.scanComment();
        break;

      // Whitespace
      case ' ':
      case '\r':
      case '\t':
        // Ignore whitespace
        break;

      case '\n':
        this.addToken(TokenType.NEWLINE, ch);
        break;

      // String literals
      case '"':
        this.scanString();
        break;

      default:
        if (this.isDigit(ch)) {
          this.scanNumber(ch);
        } else if (this.isAlpha(ch)) {
          this.scanIdentifier(ch);
        } else {
          this.addToken(TokenType.ERROR, ch);
        }
        break;
    }
  }

  private isDigit(ch: string): boolean {
    return ch >= '0' && ch <= '9';
  }

  private isAlpha(ch: string): boolean {
    return (ch >= 'a' && ch <= 'z') ||
           (ch >= 'A' && ch <= 'Z') ||
           ch === '_';
  }

  private isAlphaNumeric(ch: string): boolean {
    return this.isAlpha(ch) || this.isDigit(ch);
  }

  private scanComment(): void {
    let value = '#';
    while (!this.isAtEnd() && this.peek() !== '\n') {
      value += this.advance();
    }
    this.addToken(TokenType.COMMENT, value);
  }

  private scanString(): void {
    let value = '';
    while (!this.isAtEnd() && this.peek() !== '"') {
      if (this.peek() === '\\' && this.peekNext() === '"') {
        this.advance();
        value += this.advance();
      } else {
        value += this.advance();
      }
    }
    if (this.isAtEnd()) {
      this.addToken(TokenType.ERROR, 'Unterminated string');
      return;
    }
    this.advance(); // Closing quote
    this.addToken(TokenType.STRING, value);
  }

  private scanNumber(first: string): void {
    let value = first;
    while (this.isDigit(this.peek())) {
      value += this.advance();
    }
    if (this.peek() === '.' && this.isDigit(this.peekNext())) {
      value += this.advance(); // .
      while (this.isDigit(this.peek())) {
        value += this.advance();
      }
    }
    // Scientific notation
    if (this.peek() === 'e' || this.peek() === 'E') {
      value += this.advance();
      if (this.peek() === '+' || this.peek() === '-') {
        value += this.advance();
      }
      while (this.isDigit(this.peek())) {
        value += this.advance();
      }
    }
    this.addToken(TokenType.NUMBER, value);
  }

  private scanIdentifier(first: string): void {
    let value = first;
    while (this.isAlphaNumeric(this.peek())) {
      value += this.advance();
    }
    const type = KEYWORDS[value.toLowerCase()] || TokenType.IDENTIFIER;
    this.addToken(type, value);
  }
}

/**
 * Tokenize DNA-Lang source code.
 */
export function tokenize(source: string): Token[] {
  return new Lexer(source).tokenize();
}
