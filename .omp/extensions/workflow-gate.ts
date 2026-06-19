import { existsSync } from "node:fs";
import { normalize } from "node:path";

type ExecResult = {
  stdout?: string;
  code?: number;
};

type ToolCallEvent = {
  toolName?: string;
  input?: {
    path?: string;
  };
};

type ActiveBeadResult = { id: string } | { error: true } | { error: false };

function normalizeRepoPath(path: string): string | null {
  const normalized = normalize(path).replace(/\\/g, "/").replace(/^\.\//, "");
  if (
    normalized === ".." ||
    normalized.startsWith("../") ||
    normalized.includes("/../")
  ) {
    return null;
  }
  return normalized;
}

async function getActiveBead(
  pi: { exec: (cmd: string, args: string[]) => Promise<ExecResult> },
): Promise<ActiveBeadResult> {
  try {
    const result = await pi.exec("br", [
      "list",
      "--status",
      "open",
      "--status",
      "in_progress",
      "--json",
    ]);

    if ((result.code ?? 1) !== 0 || !result.stdout) {
      return { error: true };
    }

    const parsed = JSON.parse(result.stdout);
    const issues = Array.isArray(parsed) ? parsed : parsed?.issues;
    if (!Array.isArray(issues) || issues.length === 0) {
      return { error: false };
    }

    issues.sort((a: { updated_at?: string }, b: { updated_at?: string }) => {
      const aTime = typeof a?.updated_at === "string" ? a.updated_at : "";
      const bTime = typeof b?.updated_at === "string" ? b.updated_at : "";
      return bTime.localeCompare(aTime);
    });

    return typeof issues[0]?.id === "string" ? { id: issues[0].id } : { error: false };
  } catch {
    return { error: true };
  }
}

export default function workflowGate(pi: {
  on: (
    event: string,
    handler: (
      event: ToolCallEvent,
    ) =>
      | Promise<{ block: boolean; reason: string } | void>
      | { block: boolean; reason: string }
      | void,
  ) => void;
  exec: (cmd: string, args: string[]) => Promise<ExecResult>;
}) {
  let cachedBead: { id: string } | null = null;
  let cachedAt = 0;
  const cacheTtlMs = 30_000;

  async function resolveActiveBead() {
    const now = Date.now();
    if (cachedBead && now - cachedAt < cacheTtlMs) {
      return cachedBead;
    }
    const bead = await getActiveBead(pi);
    if ("id" in bead) {
      cachedBead = bead;
      cachedAt = now;
    } else {
      cachedBead = null;
      cachedAt = 0;
    }
    return bead;
  }

  pi.on("tool_call", async (event) => {
    if (process.env.OMP_SKIP_BEADS_WORKFLOW === "1") {
      return;
    }

    if (event.toolName !== "edit" && event.toolName !== "write") {
      return;
    }

    const rawPath = typeof event.input?.path === "string" ? event.input.path : null;
    if (!rawPath) {
      return;
    }

    const path = normalizeRepoPath(rawPath);
    if (!path) {
      return {
        block: true,
        reason: `Workflow gate: ${rawPath} escapes the repository root. Use a normalized in-repo path.`,
      };
    }

    if (rawPath.replace(/\\/g, "/").startsWith(".beads/artifacts/") && !path.startsWith(".beads/artifacts/")) {
      return {
        block: true,
        reason: `Workflow gate: ${rawPath} escapes bead artifacts after normalization. Use a direct artifact path.`,
      };
    }

    // Always allow .omp/ files (workflow infrastructure)
    if (path.startsWith(".omp/")) {
      return;
    }

    // Allow .beads/ files that are NOT bead artifacts
    // (db, journal, locks, history — workflow state files)
    if (
      path.startsWith(".beads/") &&
      !path.startsWith(".beads/artifacts/")
    ) {
      return;
    }

    const bead = await resolveActiveBead();

    // br failed — warn but don't block (no false positives)
    if ("error" in bead && bead.error) {
      console.warn(
        "[workflow-gate] Could not determine active bead (br failed). Allowing edit.",
      );
      return;
    }

    // No active bead — allow
    if ("error" in bead) {
      return;
    }

    const activeBead = bead.id;

    // Writing to any bead's artifacts — allow
    if (path.startsWith(".beads/artifacts/")) {
      const activeArtifactPrefix = `.beads/artifacts/${activeBead}/`;
      if (!path.startsWith(activeArtifactPrefix)) {
        return {
          block: true,
          reason: `Workflow gate: ${path} is outside the active bead ${activeBead}. Scope artifact writes to the active bead.`,
        };
      }

      // But block review-report.md if no completion evidence exists
      if (
        path.endsWith("/review-report.md") &&
        path.includes(`/artifacts/${activeBead}/`) &&
        !existsSync(`.beads/artifacts/${activeBead}/completion-evidence.json`)
      ) {
        return {
          block: true,
          reason: `Workflow gate: no completion evidence for ${activeBead}. Run /verify first.`,
        };
      }
      return;
    }

    // Source file edit — require PRD
    if (!existsSync(`.beads/artifacts/${activeBead}/prd.md`)) {
      return {
        block: true,
        reason: `Workflow gate: active bead ${activeBead} has no PRD. Run /create first.`,
      };
    }

    // Source file edit — require plan
    if (!existsSync(`.beads/artifacts/${activeBead}/plan.md`)) {
      return {
        block: true,
        reason: `Workflow gate: active bead ${activeBead} has no plan. Run /plan first.`,
      };
    }
  });
}
