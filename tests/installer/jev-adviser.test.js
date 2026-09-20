import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { buildPlan } from '../../scripts/installer/engine.js';

const root = path.resolve(import.meta.dirname, '../..');
const command = path.join(root, '.agents/skills/wtk/scripts/advise.mjs');
const mock = pathToFileURL(path.join(root, 'tests/installer/jev-fetch-mock.mjs')).href;
const phases = ['plan', 'build', 'verify', 'review', 'qa', 'ship'];

function input(overrides = {}) {
  return {
    decision: 'Which investigation should happen next?',
    evidence: ['Two concurrent checkout requests fail; a single request passes.'],
    options: {
      trace_concurrency: 'Inspect transaction and uniqueness behavior.',
      inspect_rendering: 'Inspect browser rendering and event handlers.',
    },
    ...overrides,
  };
}

function answerFor(value, overrides = {}) {
  const ids = [...Object.keys(value.options), 'insufficient_evidence'];
  const each = 1 / ids.length;
  const probabilities = Object.fromEntries(ids.map((id, index) => [id, index === ids.length - 1 ? 1 - each * (ids.length - 1) : each]));
  return {
    model: 'jev-1.13.0',
    answers: {
      next_step: { type: 'choice', choice: ids[0], probabilities, confidence: 0.8 },
      evidence_sufficient: { type: 'noul', noul: 0.9 },
    },
    usage: { input_tokens: 42, output_tokens: 11 },
    ...overrides,
  };
}

function runCli({ phase = 'build', send = false, args, rawInput, body = input(), key, scenario = 'success', response, timeout = 5000 } = {}) {
  const cwd = fs.mkdtempSync(path.join(os.tmpdir(), 'jev-adviser-'));
  const capturePath = path.join(cwd, 'fetch-capture.json');
  const submittedBody = typeof body === 'function' ? body(cwd) : body;
  const env = {
    PATH: process.env.PATH || '',
    JEV_MOCK_CAPTURE: capturePath,
    JEV_MOCK_CASE: scenario,
    JEV_MOCK_RESPONSE: typeof response === 'string' ? response : JSON.stringify(response ?? answerFor(submittedBody)),
  };
  if (key !== undefined) env.TYPESAFE_API_KEY = key;
  const submitted = rawInput ?? JSON.stringify(submittedBody);
  const argv = args ?? ['--phase', phase, ...(send ? ['--send'] : [])];
  const processResult = spawnSync(process.execPath, ['--import', mock, command, ...argv], {
    cwd,
    env,
    input: Buffer.isBuffer(submitted) ? submitted : Buffer.from(submitted),
    encoding: 'utf8',
    timeout,
  });
  const capture = fs.existsSync(capturePath) ? JSON.parse(fs.readFileSync(capturePath, 'utf8')) : null;
  const extraFiles = fs.readdirSync(cwd).filter((filename) => filename !== 'fetch-capture.json').sort();
  fs.rmSync(cwd, { recursive: true, force: true });
  return { exitCode: processResult.status, error: processResult.error, stdout: processResult.stdout, stderr: processResult.stderr, capture, extraFiles };
}

function resultOf(run) {
  assert.equal(run.error, undefined, run.error?.message);
  assert.ok(run.stdout, run.stderr);
  return JSON.parse(run.stdout);
}

test('JEV-001 previews all phases with independent Choice and Noul questions and never calls the provider', () => {
  for (const phase of phases) {
    const run = runCli({ phase });
    assert.equal(run.exitCode, 0, phase);
    const result = resultOf(run);
    assert.equal(result.status, 'preview', phase);
    assert.match(result.input_hash, /^[0-9a-f]{64}$/);
    assert.deepEqual(Object.keys(result.request).sort(), ['model', 'questions', 'state']);
    assert.equal(result.request.model, 'jev-latest');
    assert.equal(result.request.state.phase, phase);
    assert.deepEqual(Object.keys(result.request.state).sort(), ['decision', 'evidence', 'options', 'phase']);
    assert.deepEqual(Object.keys(result.request.questions.next_step.criteria).sort(), ['inspect_rendering', 'insufficient_evidence', 'trace_concurrency']);
    assert.equal(result.request.questions.next_step.type, 'choice');
    assert.equal(result.request.questions.evidence_sufficient.type, 'noul');
    assert.equal(run.capture, null, phase);
  }
  const help = runCli({ args: ['--help'] });
  assert.equal(help.exitCode, 0);
  assert.match(help.stdout, /Usage: node .*advise\.mjs/);
  assert.equal(help.capture, null);
});

test('JEV-002 returns typed advice, usage and a stable hash that changes with normalized input', () => {
  const value = input();
  const sent = runCli({ phase: 'build', send: true, body: value, key: 'jev_test_secret_key' });
  assert.equal(sent.exitCode, 0);
  const advice = resultOf(sent);
  assert.deepEqual(Object.keys(advice).sort(), ['answers', 'input_hash', 'model', 'status', 'usage']);
  assert.equal(advice.status, 'advice');
  assert.equal(advice.model, 'jev-1.13.0');
  assert.equal(advice.answers.next_step.type, 'choice');
  assert.equal(advice.answers.next_step.choice, 'trace_concurrency');
  assert.equal(advice.answers.next_step.confidence, 0.8);
  assert.equal(advice.answers.evidence_sufficient.type, 'noul');
  assert.equal(advice.answers.evidence_sufficient.noul, 0.9);
  assert.deepEqual(advice.usage, { input_tokens: 42, output_tokens: 11 });
  assert.equal(sent.capture.authorization_matches, true);

  const changed = runCli({ phase: 'verify', body: input({ evidence: ['A third request fails only when the lock is held.'] }) });
  assert.notEqual(resultOf(changed).input_hash, advice.input_hash);
  const reordered = runCli({ body: input({ options: { inspect_rendering: 'Inspect browser rendering and event handlers.', trace_concurrency: 'Inspect transaction and uniqueness behavior.' } }) });
  const original = runCli({ body: value });
  assert.equal(resultOf(reordered).input_hash, resultOf(original).input_hash);
});

test('JEV-003 rejects malformed and out-of-bound input before provider access while accepting documented maxima', () => {
  const maxOptions = Object.fromEntries(Array.from({ length: 8 }, (_, index) => [`${String.fromCharCode(97 + index)}${'x'.repeat(47)}`, 'o'.repeat(1000)]));
  const maximum = input({
    decision: 'd'.repeat(2000),
    evidence: ['e'.repeat(2000), ...Array(15).fill('e')],
    options: maxOptions,
  });
  const accepted = runCli({ body: maximum });
  assert.equal(accepted.exitCode, 0);
  assert.equal(resultOf(accepted).status, 'preview');

  const validBytes = Buffer.from(JSON.stringify(input()));
  const exactLimit = Buffer.concat([validBytes, Buffer.alloc(32 * 1024 - validBytes.length, 0x20)]);
  assert.equal(resultOf(runCli({ rawInput: exactLimit })).status, 'preview');

  const tooManyOptions = Object.fromEntries(Array.from({ length: 9 }, (_, index) => [`option_${index}`, 'candidate']));
  const invalidInputs = [
    ['malformed JSON', Buffer.from('{"decision":')],
    ['invalid UTF-8', Buffer.from([0x7b, 0x22, 0xff, 0x22, 0x3a, 0x31, 0x7d])],
    ['array root', JSON.stringify([])],
    ['unknown property', JSON.stringify(input({ extra: true }))],
    ['empty decision', JSON.stringify(input({ decision: ' ' }))],
    ['long decision', JSON.stringify(input({ decision: 'd'.repeat(2001) }))],
    ['no evidence', JSON.stringify(input({ evidence: [] }))],
    ['too much evidence', JSON.stringify(input({ evidence: Array(17).fill('e') }))],
    ['empty evidence item', JSON.stringify(input({ evidence: [' '] }))],
    ['long evidence item', JSON.stringify(input({ evidence: ['e'.repeat(2001)] }))],
    ['one option', JSON.stringify(input({ options: { only: 'candidate' } }))],
    ['too many options', JSON.stringify(input({ options: tooManyOptions }))],
    ['invalid option identifier', JSON.stringify(input({ options: { 'Bad-ID': 'candidate', other: 'candidate' } }))],
    ['reserved option identifier', JSON.stringify(input({ options: { insufficient_evidence: 'candidate', other: 'candidate' } }))],
    ['empty option description', JSON.stringify(input({ options: { one: ' ', two: 'candidate' } }))],
    ['long option description', JSON.stringify(input({ options: { one: 'x'.repeat(1001), two: 'candidate' } }))],
    ['oversize stdin', Buffer.concat([validBytes, Buffer.alloc(32 * 1024 + 1 - validBytes.length, 0x20)])],
  ];
  for (const [label, rawInput] of invalidInputs) {
    const run = runCli({ rawInput });
    assert.equal(run.exitCode, 2, label);
    assert.equal(resultOf(run).status, 'invalid', label);
    assert.equal(run.capture, null, label);
  }
  for (const args of [['--phase', 'unknown'], ['--phase', 'build', '--unknown']]) {
    const run = runCli({ args });
    assert.equal(run.exitCode, 2);
    assert.equal(resultOf(run).status, 'invalid');
    assert.equal(run.capture, null);
  }
});

test('JEV-004 bounds provider failures, maps timeout and accepts the exact response limit without retrying', () => {
  const missing = runCli({ send: true });
  assert.equal(missing.exitCode, 3);
  assert.equal(resultOf(missing).reason, 'missing_key');
  assert.equal(missing.capture, null);

  const exactBody = JSON.stringify(answerFor(input())).padEnd(64 * 1024, ' ');
  const successAtLimit = runCli({ send: true, key: 'jev_test_secret_key', response: exactBody });
  assert.equal(successAtLimit.exitCode, 0);
  assert.equal(resultOf(successAtLimit).status, 'advice');

  const cases = [
    ['http-error', undefined, 'http_error'],
    ['redirect', undefined, 'http_error'],
    ['network-error', undefined, 'network_error'],
    ['malformed', undefined, 'invalid_response'],
    ['oversize', undefined, 'invalid_response'],
    ['timeout-body', undefined, 'timeout'],
  ];
  for (const [scenario, response, reason] of cases) {
    const run = runCli({ send: true, key: 'jev_test_secret_key', scenario, response, timeout: 2000 });
    assert.equal(run.exitCode, 3, scenario);
    const result = resultOf(run);
    assert.deepEqual(result, { status: 'unavailable', reason }, scenario);
    assert.equal(result.status === 'advice', false, scenario);
    assert.ok(!run.stdout.includes('jev_test_secret_key'), scenario);
    assert.ok(!run.stderr.includes('jev_test_secret_key'), scenario);
    assert.equal(run.capture.calls, 1, scenario);
    if (scenario === 'redirect') assert.equal(run.capture.redirect, 'manual');
    if (scenario === 'timeout-body') assert.equal(run.capture.timeout_ms, 20_000);
  }
  const malformedAnswers = [
    ['selected option', (value) => { value.answers.next_step.choice = 'unsubmitted_option'; }],
    ['probabilities', (value) => { value.answers.next_step.probabilities.trace_concurrency = 0.5; }],
    ['confidence', (value) => { value.answers.next_step.confidence = 1.1; }],
    ['Noul', (value) => { value.answers.evidence_sufficient.noul = 1.1; }],
    ['model', (value) => { value.model = ''; }],
    ['usage', (value) => { value.usage.input_tokens = -1; }],
  ];
  for (const [label, corrupt] of malformedAnswers) {
    const response = answerFor(input());
    corrupt(response);
    const run = runCli({ send: true, key: 'jev_test_secret_key', response });
    assert.equal(run.exitCode, 3, label);
    assert.deepEqual(resultOf(run), { status: 'unavailable', reason: 'invalid_response' }, label);
    assert.equal(run.capture.calls, 1, label);
  }
});

test('JEV-005 sends only bounded synthetic context to the fixed endpoint and never executes or leaks advice', () => {
  const shellOptions = { run_payload: 'Execute the candidate command.', inspect_rendering: 'Inspect rendering.' };
  const shellResponse = answerFor(input({ options: shellOptions }));
  shellResponse.answers.next_step.choice = 'run_payload';
  shellResponse.answers.next_step.confidence = 1;
  shellResponse.answers.evidence_sufficient.noul = 1;
  const shell = runCli({
    send: true,
    key: 'jev_test_secret_key',
    body: (cwd) => input({ options: { run_payload: `; touch '${path.join(cwd, 'shell-sentinel')}'; #`, inspect_rendering: 'Inspect rendering.' } }),
    response: shellResponse,
  });
  assert.equal(shell.exitCode, 0);
  const advice = resultOf(shell);
  assert.equal(advice.status, 'advice');
  assert.equal(advice.answers.next_step.choice, 'run_payload');
  assert.deepEqual(shell.extraFiles, []);
  assert.equal(shell.capture.url, 'https://api.typesafe.ai/v1/systemone');
  assert.equal(shell.capture.method, 'POST');
  assert.equal(shell.capture.redirect, 'manual');
  assert.deepEqual(shell.capture.header_names, ['authorization', 'content-type']);
  assert.equal(shell.capture.authorization_matches, true);
  assert.deepEqual(Object.keys(shell.capture.request.state).sort(), ['decision', 'evidence', 'options', 'phase']);
  assert.ok(!JSON.stringify(shell.capture.request).includes('jev_test_secret_key'));
  assert.ok(!shell.stdout.includes('jev_test_secret_key'));

  const modelKey = 'jev-secret-token-123';
  const reflectedModel = runCli({
    send: true,
    key: modelKey,
    response: answerFor(input(), { model: `provider-${modelKey}` }),
  });
  assert.equal(reflectedModel.exitCode, 3);
  assert.deepEqual(resultOf(reflectedModel), { status: 'unavailable', reason: 'invalid_response' });
  assert.ok(!reflectedModel.stdout.includes(modelKey));

  const choiceReflection = runCli({
    send: true,
    key: modelKey,
    response: answerFor(input(), {
      answers: {
        next_step: { ...answerFor(input()).answers.next_step, choice: modelKey },
        evidence_sufficient: { type: 'noul', noul: 0.9 },
      },
    }),
  });
  assert.equal(choiceReflection.exitCode, 3);
  assert.deepEqual(resultOf(choiceReflection), { status: 'unavailable', reason: 'invalid_response' });
  assert.ok(!choiceReflection.stdout.includes(modelKey));

  const reflectedChoiceKey = 'secret_option';
  const reflectedChoice = runCli({
    send: true,
    key: reflectedChoiceKey,
    body: input({ options: { secret_option: 'Candidate containing a secret-shaped identifier.', inspect_rendering: 'Inspect rendering.' } }),
  });
  assert.equal(reflectedChoice.exitCode, 2);
  assert.deepEqual(resultOf(reflectedChoice), { status: 'invalid', reason: 'credential_in_input' });
  assert.equal(reflectedChoice.capture, null);
  assert.ok(!reflectedChoice.stdout.includes(reflectedChoiceKey));
});

test('JEV-007 stages a working preview in a core-only consumer without QA or quality', () => {
  const consumer = fs.mkdtempSync(path.join(os.tmpdir(), 'jev-core-consumer-'));
  try {
    const plan = buildPlan({ sourceRoot: root, targetRoot: consumer, selectedModules: ['core'] });
    assert.deepEqual(plan.manifest.layers, ['core']);
    assert.ok(plan.staged['.agents/skills/wtk/scripts/advise.mjs']);
    assert.ok(plan.staged['.agents/skills/wtk/references/jev-adviser.md']);
    assert.equal(Object.keys(plan.manifest.files).some((file) => file.startsWith('.agents/skills/wtk-qa')), false);
    assert.equal(Object.keys(plan.manifest.files).some((file) => file.startsWith('.agents/skills/wtk-deep-review')), false);

    for (const relative of ['.agents/skills/wtk/scripts/advise.mjs', '.agents/skills/wtk/references/jev-adviser.md']) {
      const destination = path.join(consumer, relative);
      fs.mkdirSync(path.dirname(destination), { recursive: true });
      fs.writeFileSync(destination, plan.staged[relative]);
    }
    const preview = spawnSync(process.execPath, [path.join(consumer, '.agents/skills/wtk/scripts/advise.mjs'), '--phase', 'build'], {
      cwd: consumer,
      env: { PATH: process.env.PATH || '' },
      input: JSON.stringify(input()),
      encoding: 'utf8',
      timeout: 2000,
    });
    assert.equal(preview.status, 0, preview.stderr);
    assert.equal(JSON.parse(preview.stdout).status, 'preview');
  } finally {
    fs.rmSync(consumer, { recursive: true, force: true });
  }
});
