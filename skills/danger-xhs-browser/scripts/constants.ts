import os from "node:os";
import path from "node:path";
import process from "node:process";

const APP_DATA_DIR = "baoyu-skills";
const XHS_DATA_DIR = "xhs-browser";
const COOKIE_FILE_NAME = "cookies.json";
const PROFILE_DIR_NAME = "xhs-chrome-profile";
const CONSENT_FILE_NAME = "consent.json";

export const XHS_BASE_URL = "https://www.xiaohongshu.com";
export const XHS_LOGIN_URL = "https://www.xiaohongshu.com";
export const XHS_SEARCH_URL = (keyword: string) =>
  `${XHS_BASE_URL}/search_result?keyword=${encodeURIComponent(keyword)}&source=web_search_result_notes`;
export const XHS_NOTE_URL = (noteId: string) => `${XHS_BASE_URL}/explore/${noteId}`;

export const DEFAULT_USER_AGENT =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36";

export const XHS_COOKIE_NAMES = [
  "web_session",
  "a1",
  "webId",
  "gid",
  "customerClientId",
  "x-user-id-creator.xiaohongshu.com",
] as const;

// Minimum cookies needed to detect logged-in state
export const XHS_REQUIRED_COOKIES = ["web_session"] as const;

function resolveUserDataRoot(): string {
  if (process.platform === "win32") {
    return process.env.APPDATA ?? path.join(os.homedir(), "AppData", "Roaming");
  }
  if (process.platform === "darwin") {
    return path.join(os.homedir(), "Library", "Application Support");
  }
  return process.env.XDG_DATA_HOME ?? path.join(os.homedir(), ".local", "share");
}

export function resolveXhsDataDir(): string {
  return path.join(resolveUserDataRoot(), APP_DATA_DIR, XHS_DATA_DIR);
}

export function resolveXhsCookiePath(): string {
  return path.join(resolveXhsDataDir(), COOKIE_FILE_NAME);
}

export function resolveXhsChromeProfileDir(): string {
  const override = process.env.XHS_CHROME_PROFILE_DIR?.trim();
  if (override) return path.resolve(override);
  return path.join(resolveUserDataRoot(), APP_DATA_DIR, PROFILE_DIR_NAME);
}

export function resolveXhsConsentPath(): string {
  return path.join(resolveXhsDataDir(), CONSENT_FILE_NAME);
}

/**
 * Parse a note ID from a URL or raw ID string.
 * Supports:
 *   - https://www.xiaohongshu.com/explore/{noteId}
 *   - https://www.xiaohongshu.com/discovery/item/{noteId}
 *   - https://xhslink.com/xxx (short links — just returns null, caller should handle)
 *   - Raw hex IDs like "6123456789abcdef01234567"
 */
export function parseNoteId(input: string): string | null {
  const trimmed = input.trim();
  if (!trimmed) return null;

  // Raw hex ID (24 chars)
  if (/^[0-9a-f]{24}$/i.test(trimmed)) return trimmed;

  try {
    const url = new URL(trimmed);
    // /explore/{noteId}
    const exploreMatch = url.pathname.match(/\/explore\/([0-9a-f]{24})/i);
    if (exploreMatch?.[1]) return exploreMatch[1];

    // /discovery/item/{noteId}
    const discoveryMatch = url.pathname.match(/\/discovery\/item\/([0-9a-f]{24})/i);
    if (discoveryMatch?.[1]) return discoveryMatch[1];

    // Sometimes note IDs are shorter or alphanumeric
    const genericMatch = url.pathname.match(/\/(?:explore|discovery\/item)\/([a-zA-Z0-9]+)/);
    if (genericMatch?.[1]) return genericMatch[1];
  } catch {
    // Not a URL, check if it looks like a note ID
    if (/^[a-zA-Z0-9]{10,}$/.test(trimmed)) return trimmed;
  }

  return null;
}
