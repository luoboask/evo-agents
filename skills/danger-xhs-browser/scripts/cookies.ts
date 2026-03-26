import fs from "node:fs";
import path from "node:path";
import { mkdir, readFile, writeFile } from "node:fs/promises";

import {
  CdpConnection,
  findChromeExecutable as findChromeExecutableBase,
  findExistingChromeDebugPort,
  getFreePort,
  killChrome,
  launchChrome as launchChromeBase,
  openPageSession,
  sleep,
  waitForChromeDebugPort,
  type PlatformCandidates,
} from "baoyu-chrome-cdp";

import {
  XHS_BASE_URL,
  XHS_LOGIN_URL,
  XHS_COOKIE_NAMES,
  XHS_REQUIRED_COOKIES,
  resolveXhsCookiePath,
  resolveXhsChromeProfileDir,
} from "./constants.js";

export type CookieMap = Record<string, string>;

type CookieLike = {
  name?: string;
  value?: string;
  domain?: string;
  path?: string;
  url?: string;
};

type CookieFileData = {
  version: number;
  updatedAt: string;
  cookieMap: CookieMap;
  source?: string;
};

const CHROME_CANDIDATES: PlatformCandidates = {
  darwin: [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
  ],
  win32: [
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  ],
  default: [
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ],
};

function findChromeExecutable(): string | null {
  return (
    findChromeExecutableBase({
      candidates: CHROME_CANDIDATES,
      envNames: ["XHS_CHROME_PATH"],
    }) ?? null
  );
}

async function launchChrome(profileDir: string, port: number) {
  const chromePath = findChromeExecutable();
  if (!chromePath) throw new Error("Chrome executable not found.");
  return await launchChromeBase({
    chromePath,
    profileDir,
    port,
    url: XHS_LOGIN_URL,
    extraArgs: ["--disable-popup-blocking"],
  });
}

function buildCookieMap(cookies: CookieLike[]): CookieMap {
  const map: CookieMap = {};
  for (const name of XHS_COOKIE_NAMES) {
    const match = cookies.find(
      (c) =>
        c.name === name &&
        typeof c.value === "string" &&
        c.value.length > 0
    );
    if (match?.value) map[name] = match.value;
  }
  // Also grab any other cookies that might be useful
  for (const c of cookies) {
    if (c.name && c.value && !map[c.name]) {
      map[c.name] = c.value;
    }
  }
  return map;
}

export function hasRequiredCookies(cookieMap: CookieMap): boolean {
  return XHS_REQUIRED_COOKIES.every((name) => Boolean(cookieMap[name]));
}

async function readCookieFile(p: string): Promise<CookieMap | null> {
  try {
    if (!fs.existsSync(p) || !fs.statSync(p).isFile()) return null;
    const raw = await readFile(p, "utf8");
    const data = JSON.parse(raw) as any;

    if (data?.cookieMap && typeof data.cookieMap === "object") {
      const out: CookieMap = {};
      for (const [k, v] of Object.entries(data.cookieMap as Record<string, unknown>)) {
        if (typeof v === "string") out[k] = v;
      }
      return Object.keys(out).length > 0 ? out : null;
    }

    if (data?.cookies && typeof data.cookies === "object") {
      const out: CookieMap = {};
      for (const [k, v] of Object.entries(data.cookies as Record<string, unknown>)) {
        if (typeof v === "string") out[k] = v;
      }
      return Object.keys(out).length > 0 ? out : null;
    }

    return null;
  } catch {
    return null;
  }
}

async function writeCookieFile(cookies: CookieMap, p: string, source?: string): Promise<void> {
  const dir = path.dirname(p);
  await mkdir(dir, { recursive: true });

  const payload: CookieFileData = {
    version: 1,
    updatedAt: new Date().toISOString(),
    cookieMap: cookies,
    source,
  };
  await writeFile(p, JSON.stringify(payload, null, 2), "utf8");
}

async function fetchCookiesViaCdp(
  profileDir: string,
  timeoutMs: number,
  verbose: boolean,
  log?: (msg: string) => void
): Promise<CookieMap> {
  const existingPort = await findExistingChromeDebugPort({ profileDir });
  const reusing = existingPort !== null;
  const port = existingPort ?? (await getFreePort("XHS_DEBUG_PORT"));
  const chrome = reusing ? null : await launchChrome(profileDir, port);

  let cdp: CdpConnection | null = null;
  let targetId: string | null = null;
  try {
    const wsUrl = await waitForChromeDebugPort(port, 30_000, { includeLastError: true });
    cdp = await CdpConnection.connect(wsUrl, 15_000);

    const page = await openPageSession({
      cdp,
      reusing,
      url: XHS_LOGIN_URL,
      matchTarget: (target) =>
        target.type === "page" && target.url.includes("xiaohongshu.com"),
      enableNetwork: true,
    });
    const { sessionId } = page;
    targetId = page.targetId;

    if (verbose) {
      log?.(
        reusing
          ? `[xhs-cookies] Reusing Chrome on port ${port}. Waiting for cookies...`
          : "[xhs-cookies] Chrome opened. If needed, log in to Xiaohongshu. Waiting for cookies..."
      );
    }

    const start = Date.now();
    let last: CookieMap = {};

    while (Date.now() - start < timeoutMs) {
      const { cookies } = await cdp.send<{ cookies: CookieLike[] }>(
        "Network.getCookies",
        { urls: [`${XHS_BASE_URL}/`] },
        { sessionId, timeoutMs: 10_000 }
      );

      const m = buildCookieMap((cookies ?? []).filter(Boolean));
      last = m;
      if (hasRequiredCookies(m)) {
        return m;
      }

      await sleep(1000);
    }

    throw new Error(
      `Timed out waiting for XHS cookies. Last keys: ${Object.keys(last).join(", ")}`
    );
  } finally {
    if (cdp) {
      if (reusing && targetId) {
        try {
          await cdp.send("Target.closeTarget", { targetId }, { timeoutMs: 5_000 });
        } catch {}
      } else {
        try {
          await cdp.send("Browser.close", {}, { timeoutMs: 5_000 });
        } catch {}
      }
      cdp.close();
    }
    if (chrome) killChrome(chrome);
  }
}

async function loadCookiesFromFile(
  log?: (msg: string) => void
): Promise<CookieMap> {
  const cookiePath = resolveXhsCookiePath();
  const fileMap = (await readCookieFile(cookiePath)) ?? {};
  if (Object.keys(fileMap).length > 0) {
    log?.(`[xhs-cookies] Loaded cookies from file: ${cookiePath}`);
  }
  return fileMap;
}

async function loadCookiesFromCdp(
  log?: (msg: string) => void
): Promise<CookieMap> {
  try {
    const profileDir = resolveXhsChromeProfileDir();
    const cookieMap = await fetchCookiesViaCdp(profileDir, 5 * 60 * 1000, true, log);
    if (!hasRequiredCookies(cookieMap)) return cookieMap;

    const cookiePath = resolveXhsCookiePath();
    try {
      await writeCookieFile(cookieMap, cookiePath, "cdp");
      log?.(`[xhs-cookies] Cookies saved to ${cookiePath}`);
    } catch (error) {
      log?.(
        `[xhs-cookies] Failed to write cookie file: ${error instanceof Error ? error.message : String(error)}`
      );
    }
    return cookieMap;
  } catch (error) {
    log?.(
      `[xhs-cookies] Failed to load cookies via CDP: ${error instanceof Error ? error.message : String(error)}`
    );
    return {};
  }
}

export async function loadXhsCookies(
  log?: (msg: string) => void
): Promise<CookieMap> {
  const fileMap = await loadCookiesFromFile(log);
  if (hasRequiredCookies(fileMap)) return fileMap;

  const cdpMap = await loadCookiesFromCdp(log);
  return { ...fileMap, ...cdpMap };
}

export async function refreshXhsCookies(
  log?: (msg: string) => void
): Promise<CookieMap> {
  return loadCookiesFromCdp(log);
}

export function buildCookieHeader(cookieMap: CookieMap): string | undefined {
  const entries = Object.entries(cookieMap).filter(([, v]) => v);
  if (entries.length === 0) return undefined;
  return entries.map(([k, v]) => `${k}=${v}`).join("; ");
}

/**
 * Get a CDP connection + page session for browsing XHS.
 * Returns the connection, sessionId, and cleanup function.
 */
export async function getXhsBrowserSession(
  log?: (msg: string) => void
): Promise<{
  cdp: CdpConnection;
  sessionId: string;
  targetId: string;
  navigateTo: (url: string) => Promise<void>;
  evaluate: <T = unknown>(expression: string) => Promise<T>;
  cleanup: () => Promise<void>;
}> {
  const profileDir = resolveXhsChromeProfileDir();
  const existingPort = await findExistingChromeDebugPort({ profileDir });
  const reusing = existingPort !== null;
  const port = existingPort ?? (await getFreePort("XHS_DEBUG_PORT"));
  const chrome = reusing ? null : await launchChrome(profileDir, port);

  const wsUrl = await waitForChromeDebugPort(port, 30_000, { includeLastError: true });
  const cdp = await CdpConnection.connect(wsUrl, 15_000);

  const page = await openPageSession({
    cdp,
    reusing,
    url: XHS_LOGIN_URL,
    matchTarget: (target) =>
      target.type === "page" && target.url.includes("xiaohongshu.com"),
    enableNetwork: true,
    enableRuntime: true,
    enablePage: true,
  });

  const { sessionId, targetId } = page;

  const navigateTo = async (url: string) => {
    await cdp.send("Page.navigate", { url }, { sessionId, timeoutMs: 30_000 });
    // Wait for load
    await sleep(3000);
    // Additional wait for dynamic content
    await cdp.send(
      "Runtime.evaluate",
      {
        expression: `new Promise(r => {
          if (document.readyState === 'complete') r();
          else window.addEventListener('load', r);
        })`,
        awaitPromise: true,
      },
      { sessionId, timeoutMs: 30_000 }
    );
    await sleep(1000);
  };

  const evaluate = async <T = unknown>(expression: string): Promise<T> => {
    const result = await cdp.send<{
      result: { value?: T; type?: string; description?: string };
      exceptionDetails?: { text?: string; exception?: { description?: string } };
    }>(
      "Runtime.evaluate",
      {
        expression,
        returnByValue: true,
        awaitPromise: true,
      },
      { sessionId, timeoutMs: 30_000 }
    );

    if (result.exceptionDetails) {
      const errMsg =
        result.exceptionDetails.exception?.description ||
        result.exceptionDetails.text ||
        "Unknown evaluation error";
      throw new Error(`DOM evaluation error: ${errMsg}`);
    }

    return result.result.value as T;
  };

  const cleanup = async () => {
    try {
      if (reusing) {
        await cdp.send("Target.closeTarget", { targetId }, { timeoutMs: 5_000 });
      } else {
        await cdp.send("Browser.close", {}, { timeoutMs: 5_000 });
      }
    } catch {}
    cdp.close();
    if (chrome) killChrome(chrome);
  };

  return { cdp, sessionId, targetId, navigateTo, evaluate, cleanup };
}
