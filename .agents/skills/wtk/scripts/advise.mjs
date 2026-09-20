import { createHash } from 'node:crypto';
import { TextDecoder } from 'node:util';

const ENDPOINT = 'https://api.typesafe.ai/v1/systemone';
const MODEL = 'jev-latest';
const MAX_INPUT_BYTES = 32 * 1024;
const MAX_RESPONSE_BYTES = 64 * 1024;
const TIMEOUT_MS = 20_000;
const PHASES = new Set(['plan', 'build', 'verify', 'review', 'qa', 'ship']);
const USAGE = 'Usage: node .agents/skills/wtk/scripts/advise.mjs --phase <plan|build|verify|review|qa|ship> [--send]';

const isRecord = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);
const finiteUnit = (value) => typeof value === 'number' && Number.isFinite(value) && value >= 0 && value <= 1;
const invalid = (reason) => ({ result: { status: 'invalid', reason }, code: 2 });
const unavailable = (reason) => ({ result: { status: 'unavailable', reason }, code: 3 });

function parseArguments(args) {
  if (args.length === 1 && args[0] === '--help') return { help: true };
  if (args[0] !== '--phase' || typeof args[1] !== 'string' || (args.length > 3) || (args[2] !== undefined && args[2] !== '--send')) {
    return { error: 'invalid_arguments' };
  }
  if (!PHASES.has(args[1])) return { error: 'unknown_phase' };
  return { phase: args[1], send: args[2] === '--send' };
}

async function readInput() {
  const chunks = [];
  let bytes = 0;
  for await (const chunk of process.stdin) {
    if (!Buffer.isBuffer(chunk)) return { error: 'invalid_input' };
    if (bytes + chunk.byteLength > MAX_INPUT_BYTES) return { error: 'input_too_large' };
    chunks.push(chunk);
    bytes += chunk.byteLength;
  }
  try {
    return { text: new TextDecoder('utf-8', { fatal: true }).decode(Buffer.concat(chunks, bytes)) };
  } catch {
    return { error: 'invalid_utf8' };
  }
}

function validateInput(value) {
  if (!isRecord(value) || Object.keys(value).sort().join() !== 'decision,evidence,options') return 'invalid_schema';
  if (typeof value.decision !== 'string' || !value.decision.trim() || value.decision.length > 2000) return 'invalid_decision';
  if (!Array.isArray(value.evidence) || value.evidence.length < 1 || value.evidence.length > 16 || value.evidence.some((item) => typeof item !== 'string' || !item.trim() || item.length > 2000)) return 'invalid_evidence';
  if (!isRecord(value.options)) return 'invalid_options';
  const options = Object.entries(value.options);
  if (options.length < 2 || options.length > 8) return 'invalid_options';
  if (options.some(([id, description]) => id === 'insufficient_evidence' || !/^[a-z][a-z0-9_]{0,47}$/.test(id) || typeof description !== 'string' || !description.trim() || description.length > 1000)) return 'invalid_options';
  return null;
}

function makeRequest(phase, input) {
  const options = Object.fromEntries(Object.entries(input.options).sort(([left], [right]) => left < right ? -1 : left > right ? 1 : 0));
  const state = { phase, decision: input.decision, evidence: input.evidence, options };
  const questions = {
    next_step: {
      type: 'choice',
      instructions: 'Which supplied next step best serves the decision given evidence?',
      criteria: { ...options, insufficient_evidence: 'Evidence is insufficient to select a candidate.' },
    },
    evidence_sufficient: {
      type: 'noul',
      instructions: 'Does the supplied evidence support choosing among the provided candidate next steps?',
      criteria: {
        true: 'Evidence supports comparing the candidates for this decision.',
        false: 'Necessary evidence is missing or contradictory.',
      },
    },
  };
  const request = { state, model: MODEL, questions };
  const input_hash = createHash('sha256').update(JSON.stringify({ phase, state, options, questions })).digest('hex');
  return { request, input_hash, optionIds: [...Object.keys(options), 'insufficient_evidence'] };
}

function cancelBody(response) {
  try { void response.body?.cancel().catch(() => {}); } catch { /* Provider errors stay private. */ }
}

async function readResponse(response) {
  if (!response.body) return Buffer.alloc(0);
  const reader = response.body.getReader();
  const chunks = [];
  let bytes = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) return Buffer.concat(chunks, bytes);
      bytes += value.byteLength;
      if (bytes > MAX_RESPONSE_BYTES) {
        void reader.cancel().catch(() => {});
        return null;
      }
      chunks.push(Buffer.from(value));
    }
  } finally {
    reader.releaseLock();
  }
}

function validateResponse(value, optionIds, apiKey) {
  if (!isRecord(value) || !isRecord(value.answers) || !isRecord(value.answers.next_step) || !isRecord(value.answers.evidence_sufficient)) return null;
  const choice = value.answers.next_step;
  const evidence = value.answers.evidence_sufficient;
  if (choice.type !== 'choice' || !optionIds.includes(choice.choice) || !isRecord(choice.probabilities) || choice.confidence === undefined || !finiteUnit(choice.confidence)) return null;
  const probabilityIds = Object.keys(choice.probabilities).sort();
  if (probabilityIds.join() !== [...optionIds].sort().join() || Object.values(choice.probabilities).some((value) => !finiteUnit(value))) return null;
  const probabilityTotal = Object.values(choice.probabilities).reduce((sum, value) => sum + value, 0);
  if (Math.abs(probabilityTotal - 1) > 0.001) return null;
  if (evidence.type !== 'noul' || !finiteUnit(evidence.noul)) return null;
  if (typeof value.model !== 'string' || !value.model.trim()) return null;
  if (!isRecord(value.usage) || !Number.isSafeInteger(value.usage.input_tokens) || value.usage.input_tokens < 0 || !Number.isSafeInteger(value.usage.output_tokens) || value.usage.output_tokens < 0) return null;
  const projected = {
    model: value.model,
    answers: {
      next_step: { type: 'choice', choice: choice.choice, probabilities: choice.probabilities, confidence: choice.confidence },
      evidence_sufficient: { type: 'noul', noul: evidence.noul },
    },
    usage: { input_tokens: value.usage.input_tokens, output_tokens: value.usage.output_tokens },
  };
  return JSON.stringify(projected).includes(apiKey) ? null : projected;
}

async function getAdvice(request, optionIds, inputHash, apiKey) {
  const signal = AbortSignal.timeout(TIMEOUT_MS);
  try {
    const response = await fetch(ENDPOINT, {
      method: 'POST',
      headers: { authorization: `Bearer ${apiKey}`, 'content-type': 'application/json' },
    body: JSON.stringify(request),
      redirect: 'manual',
      signal,
    });
    if (!response.ok) {
      cancelBody(response);
      return unavailable('http_error');
    }
    const body = await readResponse(response);
    if (signal.aborted) return unavailable('timeout');
    if (!body) return unavailable('invalid_response');
    let parsed;
    try { parsed = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(body)); } catch { return unavailable('invalid_response'); }
    const valid = validateResponse(parsed, optionIds, apiKey);
    if (!valid) return unavailable('invalid_response');
    return { result: { status: 'advice', input_hash: inputHash, ...valid }, code: 0 };
  } catch (error) {
    if (signal.aborted || error?.name === 'TimeoutError' || error?.name === 'AbortError') return unavailable('timeout');
    return unavailable('network_error');
  }
}

async function main() {
  const args = parseArguments(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(`${USAGE}\n`);
    return 0;
  }
  if (args.error) {
    process.stdout.write(`${JSON.stringify(invalid(args.error).result)}\n`);
    return 2;
  }

  let read;
  try { read = await readInput(); } catch { read = { error: 'invalid_input' }; }
  if (read.error) {
    process.stdout.write(`${JSON.stringify(invalid(read.error).result)}\n`);
    return 2;
  }
  let input;
  try { input = JSON.parse(read.text); } catch {
    process.stdout.write(`${JSON.stringify(invalid('invalid_json').result)}\n`);
    return 2;
  }
  const error = validateInput(input);
  if (error) {
    process.stdout.write(`${JSON.stringify(invalid(error).result)}\n`);
    return 2;
  }

  const { request, input_hash, optionIds } = makeRequest(args.phase, input);
  if (!args.send) {
    process.stdout.write(`${JSON.stringify({ status: 'preview', input_hash, request })}\n`);
    return 0;
  }
  const apiKey = process.env.TYPESAFE_API_KEY;
  if (!apiKey) {
    process.stdout.write(`${JSON.stringify(unavailable('missing_key').result)}\n`);
    return 3;
  }
  if (JSON.stringify(request).includes(apiKey)) {
    process.stdout.write(`${JSON.stringify(invalid('credential_in_input').result)}\n`);
    return 2;
  }
  const advice = await getAdvice(request, optionIds, input_hash, apiKey);
  process.stdout.write(`${JSON.stringify(advice.result)}\n`);
  return advice.code;
}

process.exitCode = await main();
