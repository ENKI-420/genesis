/**
 * DNA-Lang Compiler
 *
 * Compiles DNA-Lang AST to executable organisms.
 */

import { tokenize } from './lexer';
import { parse, ProgramNode, OrganismNode, GeneNode, ExpressionNode } from './parser';

export interface CompiledOrganism {
  name: string;
  genes: Map<string, CompiledGene>;
  traits: Map<string, any>;
  membrane: {
    permeability: number;
    receptors: string[];
  };
}

export interface CompiledGene {
  name: string;
  parameters: string[];
  execute: (args: Map<string, any>) => any;
}

export class Compiler {
  private builtins: Map<string, (...args: any[]) => any>;

  constructor() {
    this.builtins = new Map([
      ['hadamard', () => ({ type: 'gate', name: 'H' })],
      ['cnot', () => ({ type: 'gate', name: 'CNOT' })],
      ['pauliX', () => ({ type: 'gate', name: 'X' })],
      ['pauliY', () => ({ type: 'gate', name: 'Y' })],
      ['pauliZ', () => ({ type: 'gate', name: 'Z' })],
      ['phase', (angle: number) => ({ type: 'gate', name: 'P', angle })],
      ['measure', () => ({ type: 'measurement' })],
      ['entangle', () => ({ type: 'entanglement' })],
    ]);
  }

  /**
   * Compile source code to organisms.
   */
  compile(source: string): CompiledOrganism[] {
    const tokens = tokenize(source);
    const ast = parse(tokens);
    return this.compileProgram(ast);
  }

  private compileProgram(program: ProgramNode): CompiledOrganism[] {
    return program.organisms.map(org => this.compileOrganism(org));
  }

  private compileOrganism(org: OrganismNode): CompiledOrganism {
    const genes = new Map<string, CompiledGene>();
    const traits = new Map<string, any>();

    for (const gene of org.genes) {
      genes.set(gene.name, this.compileGene(gene));
    }

    for (const trait of org.traits) {
      const value = this.evaluateExpression(trait.value, new Map());
      traits.set(trait.name, value);
    }

    return {
      name: org.name,
      genes,
      traits,
      membrane: {
        permeability: org.membrane?.permeability ?? 1.0,
        receptors: org.membrane?.receptors ?? [],
      },
    };
  }

  private compileGene(gene: GeneNode): CompiledGene {
    const parameters = gene.parameters.map(p => p.name);

    return {
      name: gene.name,
      parameters,
      execute: (args: Map<string, any>) => {
        return this.evaluateExpression(gene.expression, args);
      },
    };
  }

  private evaluateExpression(
    expr: ExpressionNode,
    env: Map<string, any>
  ): any {
    switch (expr.kind) {
      case 'number':
        return expr.value as number;

      case 'string':
        return expr.value as string;

      case 'identifier':
        const name = expr.value as string;
        if (env.has(name)) {
          return env.get(name);
        }
        // Return as symbolic reference
        return { type: 'reference', name };

      case 'bind':
        const left = this.evaluateExpression(expr.left!, env);
        const right = this.evaluateExpression(expr.right!, env);
        return { type: 'bind', left, right };

      case 'transcribe':
        const source = this.evaluateExpression(expr.left!, env);
        const target = this.evaluateExpression(expr.right!, env);
        return { type: 'transcription', source, target };

      case 'call':
        const callee = expr.callee!;
        const args = (expr.arguments || []).map(a =>
          this.evaluateExpression(a, env)
        );

        if (this.builtins.has(callee)) {
          return this.builtins.get(callee)!(...args);
        }

        // Unknown function, return symbolic call
        return { type: 'call', callee, arguments: args };

      default:
        throw new Error(`Unknown expression kind: ${expr.kind}`);
    }
  }

  /**
   * Add a builtin function.
   */
  addBuiltin(name: string, fn: (...args: any[]) => any): void {
    this.builtins.set(name, fn);
  }
}

/**
 * Compile DNA-Lang source code.
 */
export function compile(source: string): CompiledOrganism[] {
  return new Compiler().compile(source);
}

/**
 * Create an organism runtime from compiled code.
 */
export class OrganismRuntime {
  private organism: CompiledOrganism;
  private state: Map<string, any>;

  constructor(organism: CompiledOrganism) {
    this.organism = organism;
    this.state = new Map();
  }

  /**
   * Get the organism name.
   */
  get name(): string {
    return this.organism.name;
  }

  /**
   * Get a trait value.
   */
  getTrait(name: string): any {
    return this.organism.traits.get(name);
  }

  /**
   * Express a gene.
   */
  express(geneName: string, args: Record<string, any> = {}): any {
    const gene = this.organism.genes.get(geneName);
    if (!gene) {
      throw new Error(`Gene not found: ${geneName}`);
    }
    const argMap = new Map(Object.entries(args));
    return gene.execute(argMap);
  }

  /**
   * Set state.
   */
  setState(key: string, value: any): void {
    this.state.set(key, value);
  }

  /**
   * Get state.
   */
  getState(key: string): any {
    return this.state.get(key);
  }

  /**
   * Get all genes.
   */
  getGenes(): string[] {
    return Array.from(this.organism.genes.keys());
  }

  /**
   * Get all traits.
   */
  getTraits(): Map<string, any> {
    return new Map(this.organism.traits);
  }
}
