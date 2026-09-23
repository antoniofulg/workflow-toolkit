import fs from 'node:fs';

let calls = 0;
let timeoutMs;
const originalTimeout = AbortSignal.timeout.bind(AbortSignal);
AbortSignal.timeout = (milliseconds) => {
  timeoutMs = milliseconds;
  return originalTimeout(process.env.JEV_MOCK_CASE === 'timeout-body' ? 10 : milliseconds);
};

globalThis.fetch = async (url, options) => {
  calls += 1;
  const key = process.env.TYPESAFE_API_KEY || '';
  const request = JSON.parse(options.body);
  const headers = new Headers(options.headers);
  const capture = {
    calls,
    url: String(url),
    method: options.method,
    redirect: options.redirect,
    timeout_ms: timeoutMs,
    authorization_matches: headers.get('authorization') === `Bearer ${key}`,
    header_names: [...headers.keys()].sort(),
    request,
  };
  fs.writeFileSync(process.env.JEV_MOCK_CAPTURE, JSON.stringify(capture));

  switch (process.env.JEV_MOCK_CASE) {
    case 'http-error': return new Response(`provider error ${key}`, { status: 503 });
    case 'redirect': return new Response(null, { status: 302, headers: { location: 'https://example.invalid/redirect' } });
    case 'network-error': throw new Error(`provider error ${key}`);
    case 'malformed': return new Response('{not-json');
    case 'oversize': return new Response(Buffer.alloc(64 * 1024 + 1, 0x78));
    case 'timeout-body': {
      const body = new ReadableStream({
        start(controller) {
          const keepAlive = setTimeout(() => {}, 100);
          options.signal.addEventListener('abort', () => {
            clearTimeout(keepAlive);
            controller.error(options.signal.reason);
          }, { once: true });
        },
      });
      return new Response(body, { status: 200 });
    }
    default: return new Response(process.env.JEV_MOCK_RESPONSE, { status: 200 });
  }
};

