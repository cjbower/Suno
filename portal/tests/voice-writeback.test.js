import test from "node:test";
import assert from "node:assert/strict";
import { copyFile, mkdir, mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { dump, load } from "js-yaml";
import {
  createVoiceId001WritebackPlugin,
  createVoiceId001WritebackService,
} from "../server/voice-id-001-writeback.js";

const sourceFiles = [
  [
    new URL("../../catalog/metadata/voice-experiments.yaml", import.meta.url),
    "catalog/metadata/voice-experiments.yaml",
  ],
  [
    new URL("../../research/suno-platform/experiments/voice-id-validation-registry.md", import.meta.url),
    "research/suno-platform/experiments/voice-id-validation-registry.md",
  ],
  [
    new URL("../../research/suno-platform/experiments/voice-influence-test-2026-11-24.md", import.meta.url),
    "research/suno-platform/experiments/voice-influence-test-2026-11-24.md",
  ],
];

async function createTemporaryRepository() {
  const root = await mkdtemp(join(tmpdir(), "suno-voice-writeback-"));
  for (const [sourceUrl, relativePath] of sourceFiles) {
    const target = join(root, relativePath);
    await mkdir(join(target, ".."), { recursive: true });
    await copyFile(sourceUrl, target);
  }
  const yamlPath = join(root, "catalog/metadata/voice-experiments.yaml");
  const document = load(await readFile(yamlPath, "utf8"));
  const experiment = document.experiment_records.find(
    (record) => record.experiment_id === "Voice-ID-001",
  );
  experiment.human_evaluation.submissions = [];
  await writeFile(yamlPath, dump(document, { lineWidth: -1, noRefs: true }));
  return root;
}

test("Voice-ID-001 writeback appends exact listener metadata, audit values, and a new snapshot", async () => {
  const root = await createTemporaryRepository();
  const preservedExportPath = join(
    root,
    "research/suno-platform/experiments/voice-id-001-evaluation-2026-11-24.json",
  );
  await writeFile(preservedExportPath, "preserve this historical export\n");
  const service = createVoiceId001WritebackService({
    repositoryRoot: root,
    clock: () => new Date("2026-11-25T01:02:03.456Z"),
  });

  try {
    const initialState = await service.getState();
    const result = await service.submit({
      experiment_id: "Voice-ID-001",
      revision: initialState.revision,
      form_values: {
        listener_name: "  Kai O'Neil  ",
        pronunciation_change: "Yes",
        one_sentence_conclusion: "The output is obvious.",
      },
    });

    assert.equal(result.experiment_id, "Voice-ID-001");
    assert.ok(result.listener_suggestions.includes("Christopher Bower"));
    assert.ok(result.listener_suggestions.includes("  Kai O'Neil  "));
    assert.equal(result.latest_submission.listener_name, "  Kai O'Neil  ");
    assert.equal(result.latest_submission.user, "  Kai O'Neil  ");
    assert.deepEqual(result.latest_submission.modified_fields, [
      "listener_name",
      "answers.pronunciation_change",
    ]);
    assert.equal(result.latest_submission.previous_values.listener_name, "Christopher Bower");
    assert.equal(result.latest_submission.new_values.listener_name, "  Kai O'Neil  ");
    assert.equal(result.latest_submission.previous_values["answers.pronunciation_change"], null);
    assert.equal(result.latest_submission.new_values["answers.pronunciation_change"], "Yes");

    const yamlText = await readFile(
      join(root, "catalog/metadata/voice-experiments.yaml"),
      "utf8",
    );
    const experiment = load(yamlText).experiment_records.find(
      (record) => record.experiment_id === "Voice-ID-001",
    );
    assert.equal(experiment.human_evaluation.submissions.length, 1);
    assert.equal(experiment.human_evaluation.submissions[0].listener_name, "  Kai O'Neil  ");

    const registry = await readFile(
      join(root, "research/suno-platform/experiments/voice-id-validation-registry.md"),
      "utf8",
    );
    const report = await readFile(
      join(root, "research/suno-platform/experiments/voice-influence-test-2026-11-24.md"),
      "utf8",
    );
    assert.match(registry, /Repository-Backed Evaluation Submissions/);
    assert.match(registry, /Kai O'Neil/);
    assert.match(report, /Repository-Backed Evaluation Submissions/);
    assert.match(report, /answers\.pronunciation_change/);

    assert.equal(await readFile(preservedExportPath, "utf8"), "preserve this historical export\n");
    const files = await readdir(join(root, "research/suno-platform/experiments"));
    const snapshotName = files.find((name) => name === result.snapshot_name);
    assert.ok(snapshotName);
    const snapshot = JSON.parse(
      await readFile(join(root, "research/suno-platform/experiments", snapshotName), "utf8"),
    );
    assert.equal(snapshot.schema_version, 2);
    assert.equal(snapshot.listener, "  Kai O'Neil  ");
    assert.equal(snapshot.writeback.timestamp, "2026-11-25T01:02:03.456Z");
    assert.equal(snapshot.writeback.snapshot_name, result.snapshot_name);
    assert.deepEqual(snapshot.writeback.modified_fields, [
      "listener_name",
      "answers.pronunciation_change",
    ]);

    const nextState = await service.getState();
    assert.ok(nextState.listener_suggestions.includes("  Kai O'Neil  "));
    const secondSubmission = await service.submit({
      experiment_id: "Voice-ID-001",
      revision: nextState.revision,
      form_values: { listener_name: "Another Listener" },
    });
    assert.equal(secondSubmission.submissions.length, 2);
    assert.equal(secondSubmission.submissions[0].listener_name, "  Kai O'Neil  ");
    assert.equal(secondSubmission.submissions[1].listener_name, "Another Listener");
    assert.ok(secondSubmission.listener_suggestions.includes("Another Listener"));

    await assert.rejects(
      service.submit({
        experiment_id: "Voice-ID-001",
        revision: initialState.revision,
        form_values: { listener_name: "Another Listener" },
      }),
      { statusCode: 409 },
    );
    const finalState = await service.getState();
    assert.equal(finalState.submissions.length, 2);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("Voice-ID-001 writeback rejects invalid input without modifying repository files", async () => {
  const root = await createTemporaryRepository();
  const service = createVoiceId001WritebackService({ repositoryRoot: root });
  const before = await Promise.all(
    sourceFiles.map(([, relativePath]) => readFile(join(root, relativePath), "utf8")),
  );

  try {
    const state = await service.getState();
    await assert.rejects(
      service.submit({
        experiment_id: "Voice-ID-001",
        revision: state.revision,
        form_values: {
          listener_name: "A listener",
          treatment_strength: "Extremely Strong",
        },
      }),
      { statusCode: 400 },
    );
    await assert.rejects(
      service.submit({
        experiment_id: "Voice-ID-002",
        revision: state.revision,
        form_values: { listener_name: "Out of scope" },
      }),
      { statusCode: 400 },
    );
    const after = await Promise.all(
      sourceFiles.map(([, relativePath]) => readFile(join(root, relativePath), "utf8")),
    );
    assert.deepEqual(after, before);
    const files = await readdir(join(root, "research/suno-platform/experiments"));
    assert.equal(files.some((name) => name.includes("writeback-")), false);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("Voice-ID-001 HTTP writeback requires same-origin requests", async () => {
  const root = await createTemporaryRepository();
  const plugin = createVoiceId001WritebackPlugin({ repositoryRoot: root });
  let middleware;
  plugin.configureServer({
    middlewares: {
      use(handler) {
        middleware = handler;
      },
    },
  });
  const server = createServer((request, response) => {
    middleware(request, response, () => {
      response.statusCode = 404;
      response.end();
    });
  });

  try {
    await new Promise((resolveListen, rejectListen) => {
      server.once("error", rejectListen);
      server.listen(0, "127.0.0.1", resolveListen);
    });
    const address = server.address();
    const origin = `http://127.0.0.1:${address.port}`;
    const stateResponse = await fetch(`${origin}/api/voice-id-001/state`);
    const state = await stateResponse.json();
    assert.equal(stateResponse.status, 200);

    const payload = {
      experiment_id: "Voice-ID-001",
      revision: state.revision,
      form_values: { listener_name: "Listener from local form" },
    };
    const rejected = await fetch(`${origin}/api/voice-id-001`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Origin: "https://example.test" },
      body: JSON.stringify(payload),
    });
    assert.equal(rejected.status, 403);

    const saved = await fetch(`${origin}/api/voice-id-001`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Origin: origin },
      body: JSON.stringify(payload),
    });
    assert.equal(saved.status, 201);
    assert.equal((await saved.json()).latest_submission.listener_name, "Listener from local form");
  } finally {
    await new Promise((resolveClose, rejectClose) => {
      server.close((error) => (error ? rejectClose(error) : resolveClose()));
    });
    await rm(root, { recursive: true, force: true });
  }
});
