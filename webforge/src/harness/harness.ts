/**
 * harness.ts — drives one Figma frame into your local Next.js site.
 *
 *   npm run harness -- --project ../../my-site \
 *                      --figma-url <url> --component-name <Name>
 *
 * Stages: INIT → FETCH_FIGMA → GENERATE_CODE → TYPE_CHECK → BUILD_PROJECT → LOCAL_PREVIEW
 *
 * LOCAL ONLY. Nothing is deployed, nothing is pushed, nothing leaves this machine.
 * There is no git command and no network upload anywhere in this file. It writes one
 * component into your project, type-checks it, builds it, serves it on localhost, and
 * runs this repo's QA judges against that local URL.
 *
 * Options:
 *   --project <path>         required — your local Next.js site
 *   --figma-url <url>        required
 *   --component-name <Name>  required, PascalCase
 *   --run-id <id>            defaults to a timestamp
 *   --port <n>               local preview port (default 3000)
 *   --skip-qa                build and serve, skip the QA gate
 *   --no-serve               stop after BUILD_PROJECT
 *   --dry-run                print what would run, execute nothing
 */
import { execFileSync, spawn, spawnSync } from "child_process";
import * as fs from "fs";
import * as path from "path";
import { PipelineStateMachine, type Stage } from "./state-machine";

const WEBFORGE = path.resolve(__dirname, "..", "..");
const REPO = path.resolve(WEBFORGE, "..");
const CONTEXT = path.join(WEBFORGE, "CONTEXT.md");
const MEMORY = path.join(WEBFORGE, "MEMORY.md");
const PROGRESS = path.join(WEBFORGE, "PROGRESS.md");

interface Args {
  project: string;
  figmaUrl: string;
  componentName: string;
  runId: string;
  port: number;
  skipQa: boolean;
  noServe: boolean;
  dryRun: boolean;
}

interface RunResult {
  ok: boolean;
  stdout: string;
  stderr: string;
}

function parseArgs(argv: string[]): Args {
  const get = (flag: string): string | undefined => {
    const i = argv.indexOf(flag);
    return i !== -1 && argv[i + 1] && !argv[i + 1].startsWith("--")
      ? argv[i + 1]
      : undefined;
  };
  const project = get("--project");
  const figmaUrl = get("--figma-url");
  const componentName = get("--component-name");

  const missing = [
    !project && "--project",
    !figmaUrl && "--figma-url",
    !componentName && "--component-name",
  ].filter(Boolean);
  if (missing.length) {
    console.error(
      `\nMissing required argument(s): ${missing.join(", ")}\n\n` +
        `  npm run harness -- --project <path-to-your-site> \\\n` +
        `                     --figma-url <url> --component-name <Name>\n`,
    );
    process.exit(2);
  }

  return {
    project: path.resolve(process.cwd(), project as string),
    figmaUrl: figmaUrl as string,
    componentName: componentName as string,
    runId:
      get("--run-id") ?? new Date().toISOString().replace(/[:.]/g, "-").slice(0, 16),
    port: Number(get("--port") ?? 3000),
    skipQa: argv.includes("--skip-qa"),
    noServe: argv.includes("--no-serve"),
    dryRun: argv.includes("--dry-run"),
  };
}

/** `?node-id=235-958` is the URL form; the API wants `235:958`. */
function parseFigmaUrl(url: string): { fileKey: string; nodeId: string } {
  const fileKey = /\/(?:file|design)\/([A-Za-z0-9]+)/.exec(url)?.[1] ?? "";
  const raw = /[?&]node-id=([^&]+)/.exec(url)?.[1] ?? "";
  return { fileKey, nodeId: decodeURIComponent(raw).replace("-", ":") };
}

function run(
  cmd: string,
  args: string[],
  opts: { cwd?: string; dryRun?: boolean; quiet?: boolean } = {},
): RunResult {
  const label = `${cmd} ${args.join(" ")}`;
  if (opts.dryRun) {
    console.log(`  [dry-run] ${label}`);
    return { ok: true, stdout: "", stderr: "" };
  }
  console.log(`  $ ${label}`);
  const r = spawnSync(cmd, args, {
    cwd: opts.cwd ?? WEBFORGE,
    encoding: "utf8",
    maxBuffer: 32 * 1024 * 1024,
  });
  const stdout = r.stdout ?? "";
  const stderr = r.stderr ?? "";
  if (!opts.quiet && stdout.trim()) console.log(indent(stdout));
  if (!opts.quiet && stderr.trim()) console.error(indent(stderr));
  return { ok: r.status === 0, stdout, stderr };
}

function have(cmd: string): boolean {
  try {
    execFileSync("command", ["-v", cmd], { shell: "/bin/sh", stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

function indent(s: string): string {
  return s.trimEnd().split("\n").slice(0, 60).map((l) => `    ${l}`).join("\n");
}

/** Poll until the local server answers, or give up. */
function waitForServer(port: number, timeoutMs = 90_000): boolean {
  const url = `http://localhost:${port}`;
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const r = spawnSync("curl", ["-s", "-o", "/dev/null", "-w", "%{http_code}", url], {
      encoding: "utf8",
    });
    if (r.stdout && /^[23]/.test(r.stdout.trim())) return true;
    spawnSync("sleep", ["1"]);
  }
  return false;
}

function hydrateContext(args: Args, figma: { fileKey: string; nodeId: string }): void {
  const started = new Date().toISOString().replace("T", " ").slice(0, 19) + "Z";
  fs.writeFileSync(
    CONTEXT,
    `# CONTEXT — active run

Overwritten by \`src/harness/harness.ts\` at the start of every run. Treat it as the
scratchpad for the run in flight, not as history — history lives in \`MEMORY.md\`.

## Run

| | |
|---|---|
| Run ID | \`${args.runId}\` |
| Started | \`${started}\` |
| Figma URL | ${args.figmaUrl} |
| File key | \`${figma.fileKey || "—"}\` |
| Node ID | \`${figma.nodeId || "—"}\` |
| Component | \`${args.componentName}\` |
| Project | \`${args.project}\` |
| Target path | \`components/figma/${args.componentName}.tsx\` |

## Phase

| | |
|---|---|
| Current | \`INIT\` |
| Status | \`running\` |
| Local URL | \`—\` |

## Design spec

\`\`\`
runs/${args.runId}/design.json
\`\`\`

## Errors

Every failed command lands here with its full output — the harness appends, it does not
overwrite, so a run that failed three times shows all three. This is what gets read
before the next attempt.

## Notes

\`\`\`
—
\`\`\`
`,
  );
}

function setContextField(field: string, value: string): void {
  if (!fs.existsSync(CONTEXT)) return;
  const body = fs.readFileSync(CONTEXT, "utf8");
  const re = new RegExp(`(\\| ${field} \\| )\`?[^|]*?\`?( \\|)`);
  fs.writeFileSync(CONTEXT, body.replace(re, `$1${value}$2`));
}

function recordInMemory(args: Args): void {
  if (!fs.existsSync(MEMORY)) return;
  const when = new Date().toISOString().slice(0, 10);
  const line =
    `- ${when} — **${args.componentName}** — \`${args.project}\`` +
    ` · run \`${args.runId}\` · built and checked locally, not deployed`;
  const body = fs.readFileSync(MEMORY, "utf8");
  fs.writeFileSync(MEMORY, body.replace("<!-- runs -->", `<!-- runs -->\n${line}`));
}

function generationPrompt(args: Args, figma: { fileKey: string; nodeId: string }): string {
  return [
    `Build the Figma frame \`${figma.nodeId}\` as a React component named`,
    `\`${args.componentName}\` at \`components/figma/${args.componentName}.tsx\``,
    `inside the project at \`${args.project}\`.`,
    ``,
    `Source: ${args.figmaUrl}`,
    ``,
    `Read the design through figwright only (\`mcp__figwright__*\`) — the Figma MCP`,
    `connector and the Figma REST API are retired in this repo. Ping figwright first; if`,
    `it is not connected, stop and say so rather than guessing at the design.`,
    ``,
    `Save the frame dump to \`${path.join(WEBFORGE, "runs", args.runId, "design.json")}\``,
    `so the fidelity check can run against it.`,
    ``,
    `Read these FIRST, in this order. The project's own instructions outrank ours —`,
    `we only own how a Figma frame becomes markup:`,
    `  1. ${path.join(args.project, "CLAUDE.md")} — THE authority on this codebase`,
    `  2. ${path.join(args.project, "AGENTS.md")} — imported by the above`,
    `  3. ${path.join(REPO, ".claude/rules/component-architecture.md")} — where files go,`,
    `     what to reuse, the v2/v3 split`,
    `  4. ${path.join(REPO, ".claude/rules/design-tokens.md")} — colours and type here`,
    `  5. ${path.join(REPO, ".claude/rules/figma-to-tailwind.md")} — auto-layout mapping`,
    `  6. ${path.join(WEBFORGE, "RULES.md")} — the Figma-conversion constraints`,
    ``,
    `This is Next 16 + React 19 + Tailwind v4. It is NOT the Next.js you remember —`,
    `AGENTS.md says to read the relevant guide in node_modules/next/dist/docs/ before`,
    `writing Next code. Do that.`,
    ``,
    `There is no shadcn/ui, no tailwind.config.ts, and no src/ directory. Colour follows`,
    `a decision ladder, NOT a blanket no-hex rule — the codebase has ~1,536 arbitrary hex`,
    `utilities against ~439 token uses, so banning hex would make your component look`,
    `nothing like the 245 files around it. Use an hlth-* token when one covers the`,
    `colour; use the lowercase arbitrary utility when it is one of the fourteen de facto`,
    `colours listed in design-tokens.md; STOP and flag anything genuinely new.`,
    ``,
    `Reuse before writing: every price goes through <Money>, every internal link through`,
    `<LocalizedLink> — the store is multi-locale and hardcoding either breaks a market`,
    `silently. Search components/ for prior art; there are 322 files there.`,
    ``,
    `Non-negotiable: no hardcoded hex colours, \`npx tsc --noEmit\` clean, and`,
    `\`npm run lint\` clean — those two are the only gates this repo has, there is no`,
    `test runner. Measure every value off the node; never round to a nearer Tailwind`,
    `step. Copy is verbatim.`,
    ``,
    `Do not run any git command and do not deploy anything. This is a local-only build.`,
  ].join("\n");
}

function main(): void {
  const args = parseArgs(process.argv.slice(2));
  const figma = parseFigmaUrl(args.figmaUrl);
  const sm = new PipelineStateMachine({
    progressPath: PROGRESS,
    contextPath: CONTEXT,
    runId: args.runId,
  });

  const fail = (stage: Stage, message: string): never => {
    sm.fail(stage, message);
    setContextField("Status", "`failed`");
    console.error(`\n✗ ${stage} failed. See CONTEXT.md and PROGRESS.md.\n`);
    process.exit(1);
  };

  console.log(`\nwebforge · run ${args.runId} · ${args.componentName} · local only\n`);

  // ---------------------------------------------------------------- INIT
  sm.start("INIT");
  if (!figma.fileKey || !figma.nodeId) {
    fail("INIT", `Could not parse a file key and node id out of: ${args.figmaUrl}`);
  }
  if (!/^[A-Z][A-Za-z0-9]*$/.test(args.componentName)) {
    fail("INIT", `--component-name must be PascalCase, got "${args.componentName}"`);
  }
  if (!fs.existsSync(path.join(args.project, "package.json"))) {
    fail(
      "INIT",
      `No package.json at ${args.project}\n` +
        `--project must point at your local Next.js site.`,
    );
  }

  hydrateContext(args, figma);
  fs.mkdirSync(path.join(WEBFORGE, "runs", args.runId), { recursive: true });

  if (!have("claude") && !args.dryRun) {
    console.warn("  ! `claude` is not on PATH — GENERATE_CODE will fail");
  }
  sm.succeed("INIT", `${figma.fileKey}#${figma.nodeId} → ${path.basename(args.project)}`);

  // -------------------------------------------------- FETCH_FIGMA + GENERATE_CODE
  // One Claude Code invocation reads the frame through figwright and writes the
  // component. Splitting them would serialise the whole design through a file for
  // no benefit.
  sm.start("FETCH_FIGMA", "via figwright, inside the generation step");
  sm.succeed("FETCH_FIGMA", `dump → runs/${args.runId}/design.json`);

  sm.start("GENERATE_CODE", args.componentName);
  if (!have("claude") && !args.dryRun) {
    fail(
      "GENERATE_CODE",
      "The `claude` CLI is not on PATH, so the harness cannot drive generation.\n" +
        "Install Claude Code, or write the component interactively and re-run to\n" +
        "resume from TYPE_CHECK.",
    );
  }
  const gen = run("claude", ["-p", generationPrompt(args, figma)], {
    cwd: args.project,
    dryRun: args.dryRun,
  });
  if (!gen.ok) fail("GENERATE_CODE", gen.stderr || gen.stdout || "claude -p failed");
  sm.succeed("GENERATE_CODE", `components/figma/${args.componentName}.tsx`);

  // ---------------------------------------------------------------- TYPE_CHECK
  sm.start("TYPE_CHECK");
  const tsc = run("npx", ["tsc", "--noEmit"], {
    cwd: args.project,
    dryRun: args.dryRun,
  });
  if (!tsc.ok) fail("TYPE_CHECK", tsc.stdout || tsc.stderr || "tsc failed");
  // This repo has no test runner: tsc and eslint are the only gates it has.
  const lint = run("npm", ["run", "lint"], { cwd: args.project, dryRun: args.dryRun });
  if (!lint.ok) fail("TYPE_CHECK", lint.stdout || lint.stderr || "lint failed");
  sm.succeed("TYPE_CHECK", "tsc + lint clean");

  // -------------------------------------------------------------- BUILD_PROJECT
  sm.start("BUILD_PROJECT");
  const build = run("npm", ["run", "build"], {
    cwd: args.project,
    dryRun: args.dryRun,
  });
  if (!build.ok) fail("BUILD_PROJECT", build.stdout || build.stderr || "build failed");
  sm.succeed("BUILD_PROJECT");

  if (args.noServe || args.dryRun) {
    if (args.noServe) console.log("\n--no-serve: stopping after build.\n");
    setContextField("Status", "`built, not served`");
    if (!args.dryRun) recordInMemory(args);
    return;
  }

  // -------------------------------------------------------------- LOCAL_PREVIEW
  sm.start("LOCAL_PREVIEW", `localhost:${args.port}`);
  const localUrl = `http://localhost:${args.port}`;
  console.log(`  $ npm run start -- --port ${args.port}`);
  const server = spawn("npm", ["run", "start", "--", "--port", String(args.port)], {
    cwd: args.project,
    detached: true,
    stdio: "ignore",
  });

  const stopServer = (): void => {
    try {
      if (server.pid) process.kill(-server.pid, "SIGTERM");
    } catch {
      /* already gone */
    }
  };
  process.on("exit", stopServer);
  process.on("SIGINT", () => {
    stopServer();
    process.exit(130);
  });

  if (!waitForServer(args.port)) {
    stopServer();
    fail("LOCAL_PREVIEW", `Server did not answer on ${localUrl} within 90s.`);
  }
  setContextField("Local URL", localUrl);
  console.log(`\n  serving: ${localUrl}\n`);

  if (!args.skipQa) {
    // PageSpeed Insights fetches from Google's servers and cannot reach localhost, so
    // the local gate is structural only: links, meta, four viewports, console errors,
    // accessibility, and the design-fidelity diff. Speed is a deploy-time check.
    const qa = run(
      "python3",
      [
        path.join(REPO, "pagescore", "qa_runner.py"),
        localUrl,
        "--run-id",
        `webforge-${args.runId}`,
        "--skip-psi",
      ],
      { cwd: REPO },
    );
    const design = path.join(WEBFORGE, "runs", args.runId, "design.json");
    if (fs.existsSync(design)) {
      run(
        "python3",
        [
          path.join(REPO, "pagescore", "design_diff.py"),
          design,
          localUrl,
          "--out",
          path.join(REPO, "pagescore", "runs", `webforge-${args.runId}`),
        ],
        { cwd: REPO },
      );
    }
    if (!qa.ok) {
      stopServer();
      fail(
        "LOCAL_PREVIEW",
        `QA failed against ${localUrl}.\n` +
          `Findings: pagescore/runs/webforge-${args.runId}/findings.json`,
      );
    }
  }

  stopServer();
  setContextField("Status", "`complete`");
  sm.succeed("LOCAL_PREVIEW", `reviewed at ${localUrl}`);
  recordInMemory(args);

  console.log(
    `\n✓ ${args.componentName} built and checked locally.\n` +
      `  file:    ${path.join(args.project, "components/figma", args.componentName)}.tsx\n` +
      `  serve:   cd ${args.project} && npm run dev\n` +
      `  nothing was deployed, nothing was pushed.\n`,
  );
}

main();
