import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'smol-toml';

export const PROVIDERS = ['claude', 'codex', 'cursor'];
export const ROLES = ['planner', 'implementer', 'verifier', 'explorer', 'deep_reviewer', 'designer'];
export const AGENT_NAMES = { deep_reviewer: 'deep-reviewer' };
const QA_BROWSER_ADAPTERS = ['auto', 'jev', 'playwright-mcp', 'orca', 'maestri', 'manual'];
const EFFORTS = ['low', 'medium', 'high', 'xhigh', 'max', 'ultra'];
const modelRe = /^[^\\\s[\]"\x00-\x1f\x7f]+$/;
const runtimePath = (provider, role) => `.${provider}/agents/${AGENT_NAMES[role] || role}.${provider === 'codex' ? 'toml' : 'md'}`;
const templatePath = (root, provider, role) => path.join(root, '.agents', 'skills', 'wtk-config', 'assets', 'agents', provider, `${AGENT_NAMES[role] || role}.${provider === 'codex' ? 'toml' : 'md'}`);
const error = (message) => { throw new Error(`wtk-config: ${message}`); };

function safePath(root, relative, label = 'path') {
  const targetRoot = path.resolve(root);
  const target = path.join(targetRoot, ...relative.split('/'));
  let current = targetRoot;
  for (const part of relative.split('/')) {
    current = path.join(current, part);
    if (fs.existsSync(current) && fs.lstatSync(current).isSymbolicLink()) throw new Error('wtk-config: ' + label + ' ' + relative + ' uses symlink');
    if (current !== target && fs.existsSync(current) && !fs.lstatSync(current).isDirectory()) throw new Error('wtk-config: ' + label + ' parent must be a directory');
  }
  if (fs.existsSync(target) && !fs.lstatSync(target).isFile()) throw new Error('wtk-config: ' + label + ' must be a file');
  return target;
}

export function validateWorkflowConfig(config) {
  if (!config || typeof config !== 'object' || Array.isArray(config)) error('configuration must contain a table');
  if (config.version !== 3) error('version must be integer 3; refresh the project configuration');
  const allowed = new Set(['version', 'deep_review', 'parallelization', 'profiles', 'models', 'remediation', 'qa']);
  const unknown = Object.keys(config).find((key) => !allowed.has(key)); if (unknown) error(`contains unknown top-level key '${unknown}'`);
  if (config.qa === undefined) config.qa = {};
  const validQaValues = QA_BROWSER_ADAPTERS.join(', ');
  if (!config.qa || typeof config.qa !== 'object' || Array.isArray(config.qa)) error(`qa must be a table; browser_adapter must be one of: ${validQaValues}`);
  const unknownQaKey = Object.keys(config.qa).find((key) => key !== 'browser_adapter');
  if (unknownQaKey) error(`qa contains unknown key '${unknownQaKey}'; browser_adapter must be one of: ${validQaValues}`);
  if (config.qa.browser_adapter === undefined) config.qa.browser_adapter = 'auto';
  if (typeof config.qa.browser_adapter !== 'string' || !QA_BROWSER_ADAPTERS.includes(config.qa.browser_adapter)) error(`qa.browser_adapter must be one of: ${validQaValues}`);
  if (!config.models || typeof config.models !== 'object') error('models must be a table containing every provider');
  for (const provider of PROVIDERS) {
    const values = config.models[provider]; if (!values || typeof values !== 'object') error(`models.${provider} must be a table`);
    for (const role of ROLES) {
      const setting = values[role]; const name = `models.${provider}.${role}`;
      if (!setting || typeof setting !== 'object') error(`${name} must be a table`);
      if (typeof setting.model !== 'string' || !setting.model.trim() || !modelRe.test(setting.model)) error(`${name}.model must be a valid native model identifier`);
      if (typeof setting.effort !== 'string' || !EFFORTS.includes(setting.effort)) error(`${name}.effort must be one of: ${EFFORTS.join(', ')}`);
      if (provider === 'claude' && setting.effort === 'ultra') error(`${name}.effort 'ultra' is not supported by claude`);
    }
  }
  return config;
}

export function readWorkflowConfig(root) {
  const local = safePath(root, '.wtk.toml', 'workflow config'); const example = safePath(root, '.wtk.toml.example', 'workflow config'); const configPath = fs.existsSync(local) ? local : example;
  if (!fs.existsSync(configPath)) error('.wtk.toml is missing');
  let config; try { config = parse(fs.readFileSync(configPath, 'utf8')); } catch (cause) { error(`invalid .wtk.toml: ${cause.message}`); }
  return validateWorkflowConfig(config);
}

function one(regex, content, label) { const matches = [...content.matchAll(regex)]; if (matches.length !== 1) error(`packet must contain exactly one ${label} metadata field`); return matches[0]; }
export function packetSetting(provider, content) {
  const text = Buffer.isBuffer(content) ? content.toString('utf8') : content;
  let model, effort;
  if (provider === 'claude') { const header = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(text)?.[1]; if (header === undefined) error('packet must contain a native YAML frontmatter header'); model = one(/^model:\s*([^\r\n]+)$/gm, header, 'model')[1].trim(); effort = one(/^effort:\s*([^\r\n]+)$/gm, header, 'effort')[1].trim(); }
  else if (provider === 'cursor') { const header = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(text)?.[1]; if (header === undefined) error('packet must contain a native YAML frontmatter header'); const match = one(/^model:\s*([^\[\r\n]+)\[effort=([^\]\r\n]+)\]$/gm, header, 'model/effort'); model = match[1].trim(); effort = match[2].trim(); }
  else { const modelMatch = one(/^model\s*=\s*"((?:\\.|[^"\\])*)"/gm, text, 'model'); const effortMatch = one(/^model_reasoning_effort\s*=\s*"((?:\\.|[^"\\])*)"/gm, text, 'model_reasoning_effort'); model = JSON.parse(`"${modelMatch[1]}"`); effort = JSON.parse(`"${effortMatch[1]}"`); }
  if (!modelRe.test(model)) error('packet contains an invalid model identifier'); return { model, effort };
}

export function renderAgentPacket(provider, content, setting) {
  const text = Buffer.isBuffer(content) ? content.toString('utf8') : content; let rendered;
  if (provider === 'claude') {
    rendered = text.replace(/^(model:)\s*[^\r\n]+$/m, `$1 ${setting.model}`).replace(/^(effort:)\s*[^\r\n]+$/m, `$1 ${setting.effort}`);
  } else if (provider === 'cursor') {
    rendered = text.replace(/^(model:)\s*[^\[\r\n]+\[effort=[^\]\r\n]+\]/m, `$1 ${setting.model}[effort=${setting.effort}]`);
  } else {
    const quote = JSON.stringify(setting.model).slice(1, -1); const effort = JSON.stringify(setting.effort).slice(1, -1);
    rendered = text.replace(/^(model\s*=\s*")[^"\\]*(?:\\.[^"\\]*)*(")/m, `$1${quote}$2`).replace(/^(model_reasoning_effort\s*=\s*")[^"\\]*(?:\\.[^"\\]*)*(")/m, `$1${effort}$2`);
  }
  packetSetting(provider, rendered); return Buffer.isBuffer(content) ? Buffer.from(rendered) : rendered;
}

export function stageAgentPackets(stageRoot, targetRoot = stageRoot) {
  const root = path.resolve(stageRoot); const target = path.resolve(targetRoot); let config;
  if (fs.existsSync(path.join(target, '.wtk.toml')) || fs.existsSync(path.join(target, '.wtk.toml.example'))) config = readWorkflowConfig(target);
  else config = validateWorkflowConfig(parse(fs.readFileSync(path.join(root, '.wtk.toml.example'), 'utf8')));
  const generated = {};
  for (const provider of PROVIDERS) for (const role of ROLES) {
    const template = templatePath(root, provider, role); if (!fs.existsSync(template) || !fs.lstatSync(template).isFile()) error(`missing agent template ${path.relative(root, template)}`);
    const content = fs.readFileSync(template); packetSetting(provider, content); generated[runtimePath(provider, role)] = renderAgentPacket(provider, content, config.models[provider][role]);
  }
  if (!fs.existsSync(path.join(target, '.wtk.toml')) && fs.existsSync(path.join(root, '.wtk.toml.example'))) generated['.wtk.toml'] = fs.readFileSync(path.join(root, '.wtk.toml.example'));
  return generated;
}

export default { stageAgentPackets, readWorkflowConfig, validateWorkflowConfig, packetSetting, renderAgentPacket, PROVIDERS, ROLES };
