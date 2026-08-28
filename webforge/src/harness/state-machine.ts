/**
 * PipelineStateMachine — the pipeline's live status, written to PROGRESS.md.
 *
 * Every transition rewrites the file immediately rather than buffering to the end, so a
 * run that hangs or is killed still leaves an accurate record of how far it got and what
 * it was doing. That is the whole point: a status file that is only correct on success
 * is useless exactly when you need it.
 */
import * as fs from "fs";
import * as path from "path";

export const STAGES = [
  "INIT",
  "FETCH_FIGMA",
  "GENERATE_CODE",
  "TYPE_CHECK",
  "BUILD_PROJECT",
  "LOCAL_PREVIEW",
] as const;

export type Stage = (typeof STAGES)[number];
export type StageStatus = "pending" | "running" | "done" | "failed";

const MARK: Record<StageStatus, string> = {
  pending: "[ ]",
  running: "[~]",
  done: "[x]",
  failed: "[!]",
};

const DESCRIPTION: Record<Stage, string> = {
  INIT: "validate args, hydrate `CONTEXT.md`, check the toolchain",
  FETCH_FIGMA: "read the frame through figwright, save the dump",
  GENERATE_CODE: "drive Claude Code to write the component",
  TYPE_CHECK: "`npx tsc --noEmit`",
  BUILD_PROJECT: "`npm run build`",
  LOCAL_PREVIEW: "serve locally, QA against localhost — nothing leaves this machine",
};

interface StageState {
  status: StageStatus;
  startedAt?: string;
  finishedAt?: string;
  note?: string;
  error?: string;
}

export interface StateMachineOptions {
  /** Absolute path to PROGRESS.md. */
  progressPath: string;
  /** Absolute path to CONTEXT.md — error traces are appended here too. */
  contextPath?: string;
  runId: string;
}

function stamp(): string {
  return new Date().toISOString().replace("T", " ").slice(0, 19) + "Z";
}

export class PipelineStateMachine {
  private readonly progressPath: string;
  private readonly contextPath?: string;
  private readonly runId: string;
  private readonly startedAt: string;
  private readonly stages: Record<Stage, StageState>;
  private readonly log: string[] = [];

  constructor(options: StateMachineOptions) {
    this.progressPath = options.progressPath;
    this.contextPath = options.contextPath;
    this.runId = options.runId;
    this.startedAt = stamp();
    this.stages = STAGES.reduce((acc, s) => {
      acc[s] = { status: "pending" };
      return acc;
    }, {} as Record<Stage, StageState>);
    this.render();
  }

  /** Mark a stage as running. */
  start(stage: Stage, note?: string): void {
    this.stages[stage] = { status: "running", startedAt: stamp(), note };
    this.append(`${stamp()}  ${stage}  started${note ? ` — ${note}` : ""}`);
    this.render();
  }

  /** Mark a stage as complete. `note` shows next to it in PROGRESS.md. */
  succeed(stage: Stage, note?: string): void {
    const prev = this.stages[stage];
    this.stages[stage] = {
      ...prev,
      status: "done",
      finishedAt: stamp(),
      note: note ?? prev.note,
    };
    this.append(`${stamp()}  ${stage}  done${note ? ` — ${note}` : ""}`);
    this.render();
  }

  /**
   * Mark a stage as failed and record the full error. The trace goes to PROGRESS.md's
   * log and, when a context file is configured, is appended to CONTEXT.md — which is
   * what gets read before the next attempt.
   */
  fail(stage: Stage, error: unknown): void {
    const message = error instanceof Error ? error.message : String(error);
    const prev = this.stages[stage];
    this.stages[stage] = {
      ...prev,
      status: "failed",
      finishedAt: stamp(),
      error: message,
    };
    this.append(`${stamp()}  ${stage}  FAILED`);
    this.append(indent(message));
    this.render();
    this.appendToContext(stage, message);
  }

  status(stage: Stage): StageStatus {
    return this.stages[stage].status;
  }

  get failed(): boolean {
    return STAGES.some((s) => this.stages[s].status === "failed");
  }

  get complete(): boolean {
    return STAGES.every((s) => this.stages[s].status === "done");
  }

  /** The stage currently running, or the last one that finished. */
  get current(): Stage {
    return (
      STAGES.find((s) => this.stages[s].status === "running") ??
      [...STAGES].reverse().find((s) => this.stages[s].status !== "pending") ??
      "INIT"
    );
  }

  private append(line: string): void {
    this.log.push(line);
  }

  private appendToContext(stage: Stage, message: string): void {
    if (!this.contextPath || !fs.existsSync(this.contextPath)) return;
    const block = `\n### ${stamp()} — ${stage} failed\n\n\`\`\`\n${message.trim()}\n\`\`\`\n`;
    const body = fs.readFileSync(this.contextPath, "utf8");
    // Land it under the Errors heading, replacing the empty placeholder the first time.
    const marker = "## Errors";
    const idx = body.indexOf(marker);
    if (idx === -1) {
      fs.appendFileSync(this.contextPath, block);
      return;
    }
    const head = body.slice(0, idx + marker.length);
    const tail = body.slice(idx + marker.length).replace(/^\s*```\s*—\s*```\s*/m, "\n");
    fs.writeFileSync(this.contextPath, `${head}${tail.trimEnd()}\n${block}`);
  }

  private render(): void {
    const overall = this.failed
      ? "failed"
      : this.complete
        ? "complete"
        : "running";

    const lines: string[] = [
      "# PROGRESS",
      "",
      "Written by `src/harness/state-machine.ts` as each stage transitions. Do not edit by",
      "hand while a run is in flight — it is overwritten on every transition.",
      "",
      "Legend: `[ ]` pending · `[~]` running · `[x]` done · `[!]` failed",
      "",
      "## Pipeline",
      "",
    ];

    for (const stage of STAGES) {
      const s = this.stages[stage];
      const bits: string[] = [];
      if (s.note) bits.push(s.note);
      if (s.startedAt && s.finishedAt) bits.push(elapsed(s.startedAt, s.finishedAt));
      else if (s.startedAt) bits.push(`since ${s.startedAt}`);
      const suffix = bits.length ? ` — ${bits.join(" · ")}` : "";
      lines.push(
        `- ${MARK[s.status]} **${stage}** — ${DESCRIPTION[stage]}${suffix}`,
      );
      if (s.error) lines.push(`  - \`${firstLine(s.error)}\``);
    }

    lines.push(
      "",
      "## Run",
      "",
      "| | |",
      "|---|---|",
      `| Run ID | \`${this.runId}\` |`,
      `| Started | \`${this.startedAt}\` |`,
      `| Updated | \`${stamp()}\` |`,
      `| Status | \`${overall}\` |`,
      "",
      "## Log",
      "",
      "<!-- log -->",
      "",
      "```",
      ...(this.log.length ? this.log : ["—"]),
      "```",
      "",
    );

    fs.mkdirSync(path.dirname(this.progressPath), { recursive: true });
    fs.writeFileSync(this.progressPath, lines.join("\n"));
  }
}

function firstLine(s: string): string {
  return s.trim().split("\n")[0]?.slice(0, 160) ?? "";
}

function indent(s: string): string {
  return s
    .trim()
    .split("\n")
    .slice(0, 40)
    .map((l) => `    ${l}`)
    .join("\n");
}

function elapsed(from: string, to: string): string {
  const ms = Date.parse(to.replace(" ", "T")) - Date.parse(from.replace(" ", "T"));
  if (!Number.isFinite(ms) || ms < 0) return "";
  const secs = Math.round(ms / 1000);
  return secs < 60 ? `${secs}s` : `${Math.floor(secs / 60)}m ${secs % 60}s`;
}
