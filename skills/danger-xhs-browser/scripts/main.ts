import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import process from "node:process";
import { mkdir, readFile, writeFile } from "node:fs/promises";

import { sleep } from "baoyu-chrome-cdp";

import {
  XHS_SEARCH_URL,
  XHS_NOTE_URL,
  parseNoteId,
  resolveXhsConsentPath,
} from "./constants.js";

import {
  loadXhsCookies,
  refreshXhsCookies,
  hasRequiredCookies,
  getXhsBrowserSession,
} from "./cookies.js";

import {
  extractSearchResults,
  extractSearchResultsFallback,
  extractNoteContent,
  extractComments,
  checkPageState,
} from "./extract.js";

import {
  formatSearchResultsMarkdown,
  formatNoteMarkdown,
  formatCommentsMarkdown,
} from "./markdown.js";

// ─── Types ───────────────────────────────────────────────────────────────────

type CliArgs = {
  command: "search" | "note" | "comments" | null;
  target: string | null; // keyword for search, url/id for note/comments
  limit: number;
  login: boolean;
  help: boolean;
};

type ConsentRecord = {
  version: number;
  accepted: boolean;
  acceptedAt: string;
  disclaimerVersion: string;
};

const DISCLAIMER_VERSION = "1.0";

// ─── CLI Parsing ─────────────────────────────────────────────────────────────

function printUsage(exitCode: number): never {
  const script = "bun scripts/main.ts";
  console.log(`Xiaohongshu (小红书) Browser

Usage:
  ${script} search <keyword> [--limit N]
  ${script} note <url-or-id>
  ${script} comments <url-or-id> [--limit N]
  ${script} --login
  ${script} --help

Commands:
  search <keyword>        Search for notes by keyword
  note <url-or-id>        Extract note content (title, text, images, stats)
  comments <url-or-id>    Extract comments from a note

Options:
  --limit <n>    Max results for search/comments (default: 20)
  --login        Open Chrome to refresh XHS login cookies
  --help, -h     Show this help message

Examples:
  ${script} search "二十八星宿" --limit 20
  ${script} note https://www.xiaohongshu.com/explore/6123456789abcdef01234567
  ${script} note 6123456789abcdef01234567
  ${script} comments 6123456789abcdef01234567 --limit 50
  ${script} --login
`);
  process.exit(exitCode);
}

function parseArgs(argv: string[]): CliArgs {
  const out: CliArgs = {
    command: null,
    target: null,
    limit: 20,
    login: false,
    help: false,
  };

  const positional: string[] = [];

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;

    if (a === "--help" || a === "-h") {
      out.help = true;
      continue;
    }

    if (a === "--login") {
      out.login = true;
      continue;
    }

    if (a === "--limit") {
      const v = argv[++i];
      if (!v) throw new Error("Missing value for --limit");
      out.limit = parseInt(v, 10);
      if (isNaN(out.limit) || out.limit < 1) throw new Error("--limit must be a positive integer");
      continue;
    }

    if (a.startsWith("-")) {
      throw new Error(`Unknown option: ${a}`);
    }

    positional.push(a);
  }

  if (positional.length > 0) {
    const cmd = positional[0]!.toLowerCase();
    if (cmd === "search" || cmd === "note" || cmd === "comments") {
      out.command = cmd as "search" | "note" | "comments";
      out.target = positional.slice(1).join(" ") || null;
    } else {
      // Maybe it's a URL/ID directly — treat as "note"
      out.command = "note";
      out.target = positional.join(" ");
    }
  }

  return out;
}

// ─── Consent ─────────────────────────────────────────────────────────────────

function isValidConsent(value: unknown): value is ConsentRecord {
  if (!value || typeof value !== "object") return false;
  const r = value as Partial<ConsentRecord>;
  return (
    r.accepted === true &&
    r.disclaimerVersion === DISCLAIMER_VERSION &&
    typeof r.acceptedAt === "string" &&
    r.acceptedAt.length > 0
  );
}

async function promptYesNo(question: string): Promise<boolean> {
  if (!process.stdin.isTTY) return false;
  const rl = readline.createInterface({ input: process.stdin, output: process.stderr });
  try {
    const answer = await new Promise<string>((resolve) => rl.question(question, resolve));
    return ["y", "yes"].includes(answer.trim().toLowerCase());
  } finally {
    rl.close();
  }
}

async function ensureConsent(log: (msg: string) => void): Promise<void> {
  const consentPath = resolveXhsConsentPath();

  try {
    if (fs.existsSync(consentPath) && fs.statSync(consentPath).isFile()) {
      const raw = await readFile(consentPath, "utf8");
      const parsed = JSON.parse(raw);
      if (isValidConsent(parsed)) {
        log(`⚠️  Warning: Using Chrome automation on Xiaohongshu. Accepted on: ${parsed.acceptedAt}`);
        return;
      }
    }
  } catch {}

  log(`⚠️  DISCLAIMER

This tool uses Chrome browser automation to browse Xiaohongshu (小红书).

Risks:
- May break without notice if XHS changes page structure
- No official support or guarantees
- Possible account restrictions if automation detected
- Use at your own risk
`);

  if (!process.stdin.isTTY) {
    throw new Error(
      `Consent required. Run in a TTY or create ${consentPath} with accepted: true and disclaimerVersion: "${DISCLAIMER_VERSION}"`
    );
  }

  const accepted = await promptYesNo("Do you accept these terms and wish to continue? (y/N): ");
  if (!accepted) {
    throw new Error("User declined the disclaimer. Exiting.");
  }

  await mkdir(path.dirname(consentPath), { recursive: true });
  const payload: ConsentRecord = {
    version: 1,
    accepted: true,
    acceptedAt: new Date().toISOString(),
    disclaimerVersion: DISCLAIMER_VERSION,
  };
  await writeFile(consentPath, JSON.stringify(payload, null, 2), "utf8");
  log(`[xhs-browser] Consent saved to: ${consentPath}`);
}

// ─── Output helpers ──────────────────────────────────────────────────────────

function resolveOutputDir(): string {
  return path.resolve(process.cwd(), "xhs-browser");
}

async function saveFile(filePath: string, content: string, log: (msg: string) => void): Promise<void> {
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, content, "utf8");
  log(`[xhs-browser] Saved: ${filePath}`);
  console.log(filePath);
}

// ─── Commands ────────────────────────────────────────────────────────────────

async function handleSearch(keyword: string, limit: number, log: (msg: string) => void): Promise<void> {
  log(`[xhs-browser] Searching for: "${keyword}" (limit: ${limit})`);

  const session = await getXhsBrowserSession(log);

  try {
    const searchUrl = XHS_SEARCH_URL(keyword);
    log(`[xhs-browser] Navigating to: ${searchUrl}`);
    await session.navigateTo(searchUrl);

    // Check page state
    const state = await checkPageState(session.evaluate);
    if (state === "login_required") {
      throw new Error("Login required. Run with --login first.");
    }
    if (state === "verification") {
      throw new Error("Anti-bot verification detected. Please complete it manually in Chrome.");
    }

    log("[xhs-browser] Extracting search results...");
    let results = await extractSearchResults(session.evaluate, limit);

    // If primary extraction found nothing, try fallback
    if (results.length === 0) {
      log("[xhs-browser] Primary extraction found 0 results, trying fallback...");
      results = await extractSearchResultsFallback(session.evaluate, limit);
    }

    log(`[xhs-browser] Found ${results.length} results`);

    const markdown = formatSearchResultsMarkdown(keyword, results);
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
    const sanitizedKeyword = keyword.replace(/[^a-zA-Z0-9\u4e00-\u9fff-]/g, "_").slice(0, 50);
    const outputPath = path.join(resolveOutputDir(), `search-${sanitizedKeyword}-${timestamp}.md`);

    await saveFile(outputPath, markdown, log);
  } finally {
    await session.cleanup();
  }
}

async function handleNote(target: string, log: (msg: string) => void): Promise<void> {
  const noteId = parseNoteId(target);
  if (!noteId) {
    throw new Error(`Cannot parse note ID from: ${target}`);
  }

  const noteUrl = XHS_NOTE_URL(noteId);
  log(`[xhs-browser] Extracting note: ${noteUrl}`);

  const session = await getXhsBrowserSession(log);

  try {
    await session.navigateTo(noteUrl);

    const state = await checkPageState(session.evaluate);
    if (state === "login_required") {
      throw new Error("Login required. Run with --login first.");
    }
    if (state === "verification") {
      throw new Error("Anti-bot verification detected. Please complete it manually in Chrome.");
    }
    if (state === "not_found") {
      throw new Error(`Note not found: ${noteId}`);
    }

    log("[xhs-browser] Extracting note content...");
    const content = await extractNoteContent(session.evaluate, noteUrl);

    const markdown = formatNoteMarkdown(content);
    const outputPath = path.join(resolveOutputDir(), "notes", `${noteId}.md`);

    await saveFile(outputPath, markdown, log);
  } finally {
    await session.cleanup();
  }
}

async function handleComments(target: string, limit: number, log: (msg: string) => void): Promise<void> {
  const noteId = parseNoteId(target);
  if (!noteId) {
    throw new Error(`Cannot parse note ID from: ${target}`);
  }

  const noteUrl = XHS_NOTE_URL(noteId);
  log(`[xhs-browser] Extracting comments from: ${noteUrl} (limit: ${limit})`);

  const session = await getXhsBrowserSession(log);

  try {
    await session.navigateTo(noteUrl);

    const state = await checkPageState(session.evaluate);
    if (state === "login_required") {
      throw new Error("Login required. Run with --login first.");
    }
    if (state === "verification") {
      throw new Error("Anti-bot verification detected. Please complete it manually in Chrome.");
    }
    if (state === "not_found") {
      throw new Error(`Note not found: ${noteId}`);
    }

    log("[xhs-browser] Extracting comments...");
    const comments = await extractComments(session.evaluate, limit);
    log(`[xhs-browser] Found ${comments.length} comments`);

    const markdown = formatCommentsMarkdown(noteId, noteUrl, comments);
    const outputPath = path.join(resolveOutputDir(), "notes", `${noteId}-comments.md`);

    await saveFile(outputPath, markdown, log);
  } finally {
    await session.cleanup();
  }
}

async function handleLogin(log: (msg: string) => void): Promise<void> {
  log("[xhs-browser] Refreshing cookies via browser login...");
  const cookieMap = await refreshXhsCookies(log);
  if (!hasRequiredCookies(cookieMap)) {
    throw new Error("Missing required cookies after login. Please ensure you are logged in to Xiaohongshu.");
  }
  log("[xhs-browser] Cookies refreshed successfully.");
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) printUsage(0);
  if (!args.login && !args.command) printUsage(1);

  const log = (msg: string) => console.error(msg);
  await ensureConsent(log);

  if (args.login) {
    await handleLogin(log);
    return;
  }

  switch (args.command) {
    case "search":
      if (!args.target) throw new Error("Missing search keyword. Usage: search <keyword>");
      await handleSearch(args.target, args.limit, log);
      break;

    case "note":
      if (!args.target) throw new Error("Missing note URL or ID. Usage: note <url-or-id>");
      await handleNote(args.target, log);
      break;

    case "comments":
      if (!args.target) throw new Error("Missing note URL or ID. Usage: comments <url-or-id>");
      await handleComments(args.target, args.limit, log);
      break;

    default:
      printUsage(1);
  }
}

await main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error ?? ""));
  process.exit(1);
});
