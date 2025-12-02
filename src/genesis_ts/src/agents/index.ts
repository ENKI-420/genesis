/**
 * GENESIS Agents - Index
 *
 * Exports all agent classes.
 */

export {
  Agent,
  AgentType,
  AgentConfig,
  AgentResult,
  AIDENAgent,
  AURAAgent,
  PALSAgent,
  CHRONOSAgent,
  AEGISAgent,
} from './base';

/**
 * Create all agents.
 */
export function createAllAgents(): {
  AIDEN: import('./base').AIDENAgent;
  AURA: import('./base').AURAAgent;
  PALS: import('./base').PALSAgent;
  CHRONOS: import('./base').CHRONOSAgent;
  AEGIS: import('./base').AEGISAgent;
} {
  const { AIDENAgent, AURAAgent, PALSAgent, CHRONOSAgent, AEGISAgent } = require('./base');
  return {
    AIDEN: new AIDENAgent(),
    AURA: new AURAAgent(),
    PALS: new PALSAgent(),
    CHRONOS: new CHRONOSAgent(),
    AEGIS: new AEGISAgent(),
  };
}

/**
 * Initialize all agents.
 */
export async function initializeAgents(agents: {
  AIDEN: import('./base').Agent;
  AURA: import('./base').Agent;
  PALS: import('./base').Agent;
  CHRONOS: import('./base').Agent;
  AEGIS: import('./base').Agent;
}): Promise<void> {
  await Promise.all([
    agents.AIDEN.initialize(),
    agents.AURA.initialize(),
    agents.PALS.initialize(),
    agents.CHRONOS.initialize(),
    agents.AEGIS.initialize(),
  ]);
}
