import { createHash, randomUUID } from "node:crypto";
import { readFile, rename, unlink, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { dump, load } from "js-yaml";
import {
  buildVoiceEvaluationExport,
  validateVoiceEvaluationFormValues,
} from "../src/voice-experiment.js";

const experimentRelativePath = "catalog/metadata/voice-experiments.yaml";
const registryRelativePath =
  "research/suno-platform/experiments/voice-id-validation-registry.md";
const reportRelativePath =
  "research/suno-platform/experiments/voice-influence-test-2026-11-24.md";
const apiPath = "/api/voice-id-001";
const startMarker = "<!-- voice-id-001-writeback:start -->";
const endMarker = "<!-- voice-id-001-writeback:end -->";
const maxRequestBytes = 32 * 1024;
const loopbackHosts = new Set(["127.0.0.1", "localhost", "::1"]);

export class WritebackError extends Error {
  constructor(statusCode, message) {
    super(message);
    this.name = "WritebackError";
    this.statusCode = statusCode;
  }
}

function getExperiment(document) {
  if (!document || !Array.isArray(document.experiment_records)) {
    throw new WritebackError(500, "Voice experiment metadata is not a valid registry.");
  }
  const records = document.experiment_records.filter(
    (record) => record?.experiment_id === "Voice-ID-001",
  );
  if (records.length !== 1) {
    throw new WritebackError(500, "Expected exactly one Voice-ID-001 record.");
  }
  return records[0];
}

function getSubmissions(experiment) {
  const submissions = experiment.human_evaluation.submissions;
  if (submissions === undefined) {
    return [];
  }
  if (!Array.isArray(submissions)) {
    throw new WritebackError(500, "Voice-ID-001 submissions must be an array.");
  }
  return submissions;
}

function getListenerSuggestions(experiment) {
  const names = [
    experiment.human_evaluation.listener,
    ...getSubmissions(experiment).flatMap((submission) => [
      submission.listener_name,
      submission.user,
    ]),
  ];
  return [...new Set(names.filter((name) => typeof name === "string" && name.trim()))];
}

function getLatestSubmission(experiment) {
  return getSubmissions(experiment).at(-1) ?? null;
}

function revisionFor(contents) {
  return createHash("sha256").update(contents.join("\0")).digest("hex");
}

function codeFenceFor(content) {
  const runs = content.match(/`+/g) ?? [];
  const maxRun = runs.reduce((max, run) => Math.max(max, run.length), 0);
  return "`".repeat(Math.max(3, maxRun + 1));
}

function renderSubmissionHistory(submissions) {
  const heading = [
    "### Repository-Backed Evaluation Submissions",
    "",
    "Listener names are evaluation metadata supplied by the form; they are not authenticated identities.",
    "",
  ];

  if (submissions.length === 0) {
    heading.push("No repository-backed submissions have been recorded.");
    return heading.join("\n");
  }

  for (const [index, submission] of submissions.entries()) {
    const record = {
      submission_id: submission.submission_id,
      timestamp: submission.timestamp,
      snapshot_name: submission.snapshot_name,
      user: submission.user,
      listener_name: submission.listener_name,
      modified_fields: submission.modified_fields,
      previous_values: submission.previous_values,
      new_values: submission.new_values,
      structured_answers: submission.structured_answers,
    };
    const json = JSON.stringify(record, null, 2);
    const fence = codeFenceFor(json);
    heading.push(
      `#### Submission ${index + 1}`,
      "",
      `${fence}json`,
      json,
      fence,
      "",
    );
  }
  return heading.join("\n");
}

function updateManagedSection(markdown, anchor, section) {
  const startIndex = markdown.indexOf(startMarker);
  const endIndex = markdown.indexOf(endMarker);
  const hasStart = startIndex !== -1;
  const hasEnd = endIndex !== -1;
  const block = `${startMarker}\n${section}\n${endMarker}`;

  if (hasStart !== hasEnd) {
    throw new WritebackError(500, "A Markdown writeback marker is incomplete.");
  }
  if (hasStart) {
    if (markdown.indexOf(startMarker, startIndex + startMarker.length) !== -1 ||
        markdown.indexOf(endMarker, endIndex + endMarker.length) !== -1 ||
        endIndex < startIndex) {
      throw new WritebackError(500, "Markdown writeback markers are ambiguous.");
    }
    return `${markdown.slice(0, startIndex)}${block}${markdown.slice(endIndex + endMarker.length)}`;
  }

  const anchorIndex = markdown.indexOf(anchor);
  if (anchorIndex === -1) {
    return `${markdown.trimEnd()}\n\n${block}\n`;
  }
  return `${markdown.slice(0, anchorIndex)}${block}\n\n${markdown.slice(anchorIndex)}`;
}

async function atomicWrite(filePath, content) {
  const temporaryPath = `${filePath}.${randomUUID()}.tmp`;
  try {
    await writeFile(temporaryPath, content, { encoding: "utf8", flag: "wx" });
    await rename(temporaryPath, filePath);
  } catch (error) {
    try {
      await unlink(temporaryPath);
    } catch (cleanupError) {
      if (cleanupError.code !== "ENOENT") {
        throw new AggregateError([error, cleanupError], "Could not clean up a staged write.");
      }
    }
    throw error;
  }
}

function responseState(document, rawYaml, registry, report) {
  const experiment = getExperiment(document);
  const history = getSubmissions(experiment);
  return {
    experiment_id: "Voice-ID-001",
    revision: revisionFor([rawYaml, registry, report]),
    listener_suggestions: getListenerSuggestions(experiment),
    submissions: history,
    latest_submission: history.at(-1) ?? null,
  };
}

export function createVoiceId001WritebackService({
  repositoryRoot,
  clock = () => new Date(),
}) {
  const paths = [
    resolve(repositoryRoot, experimentRelativePath),
    resolve(repositoryRoot, registryRelativePath),
    resolve(repositoryRoot, reportRelativePath),
  ];
  let queue = Promise.resolve();

  function serialize(operation) {
    const result = queue.then(operation);
    queue = result.then(
      () => undefined,
      () => undefined,
    );
    return result;
  }

  async function readFiles() {
    return Promise.all(paths.map((path) => readFile(path, "utf8")));
  }

  async function readState() {
    const [rawYaml, registry, report] = await readFiles();
    const document = load(rawYaml);
    return responseState(document, rawYaml, registry, report);
  }

  async function submitSubmission(payload) {
    if (
      !payload ||
      typeof payload !== "object" ||
      Array.isArray(payload) ||
      payload.experiment_id !== "Voice-ID-001" ||
      typeof payload.revision !== "string"
    ) {
      throw new WritebackError(400, "A Voice-ID-001 submission and revision are required.");
    }
    const unexpectedKey = Object.keys(payload).find(
      (key) => !["experiment_id", "revision", "form_values"].includes(key),
    );
    if (unexpectedKey) {
      throw new WritebackError(400, `Unexpected request field: ${unexpectedKey}.`);
    }

    let validated;
    try {
      validated = validateVoiceEvaluationFormValues(payload.form_values);
    } catch (error) {
      throw new WritebackError(400, error.message);
    }

    const [rawYaml, registry, report] = await readFiles();
    const document = load(rawYaml);
    const experiment = getExperiment(document);
    const currentState = responseState(document, rawYaml, registry, report);
    if (payload.revision !== currentState.revision) {
      throw new WritebackError(
        409,
        "Repository data changed since this form loaded. Reload before submitting again.",
      );
    }

    const evaluation = experiment.human_evaluation;
    const history = getSubmissions(experiment);
    const previousSubmission = history.at(-1);
    const previousListener =
      previousSubmission?.listener_name ??
      previousSubmission?.user ??
      evaluation.listener;
    const previousAnswers =
      previousSubmission?.structured_answers ?? evaluation.answers;
    if (!previousAnswers || typeof previousAnswers !== "object") {
      throw new WritebackError(500, "Voice-ID-001 answer metadata is not valid.");
    }

    const currentValues = {
      listener_name: previousListener,
      ...Object.fromEntries(
        Object.entries(previousAnswers).map(([field, value]) => [`answers.${field}`, value]),
      ),
    };
    const newValues = {
      listener_name: validated.listener_name,
      ...Object.fromEntries(
        Object.entries(validated.answers).map(([field, value]) => [`answers.${field}`, value]),
      ),
    };
    const previousValues = {};
    const recordedNewValues = {};
    for (const [field, value] of Object.entries(newValues)) {
      if (currentValues[field] !== value) {
        previousValues[field] = currentValues[field] ?? null;
        recordedNewValues[field] = value;
      }
    }
    const timestamp = clock().toISOString();
    const submissionId = randomUUID();
    const timestampSlug = timestamp.replaceAll(":", "-").replaceAll(".", "-");
    const snapshotName =
      `voice-id-001-evaluation-writeback-${timestampSlug}-${submissionId.slice(0, 8)}.json`;
    const snapshotPath = resolve(
      repositoryRoot,
      "research/suno-platform/experiments",
      snapshotName,
    );
    const submission = {
      submission_id: submissionId,
      timestamp,
      snapshot_name: snapshotName,
      user: validated.listener_name,
      listener_name: validated.listener_name,
      modified_fields: Object.keys(recordedNewValues),
      previous_values: previousValues,
      new_values: recordedNewValues,
      structured_answers: validated.answers,
    };
    history.push(submission);
    evaluation.submissions = history;

    const updatedYaml = dump(document, { lineWidth: -1, noRefs: true });
    const renderedHistory = renderSubmissionHistory(history);
    const updatedRegistry = updateManagedSection(
      registry,
      "## Related References",
      renderedHistory,
    );
    const updatedReport = updateManagedSection(
      report,
      "## Repository and Catalog References",
      renderedHistory,
    );

    const updatedContents = [updatedYaml, updatedRegistry, updatedReport];
    if (revisionFor(await readFiles()) !== payload.revision) {
      throw new WritebackError(409, "Repository revision changed during submission.");
    }

    const writtenPaths = [];
    let snapshotWritten = false;

    try {
      for (let index = 0; index < paths.length; index += 1) {
        await atomicWrite(paths[index], updatedContents[index]);
        writtenPaths.push(paths[index]);
      }

      const snapshot = buildVoiceEvaluationExport(
        experiment,
        { listener_name: validated.listener_name, ...validated.answers },
        timestamp,
        {
          submission_id: submission.submission_id,
          timestamp,
          snapshot_name: snapshotName,
          user: validated.listener_name,
          modified_fields: submission.modified_fields,
          previous_values: submission.previous_values,
          new_values: submission.new_values,
        },
      );
      await writeFile(snapshotPath, `${JSON.stringify(snapshot, null, 2)}\n`, {
        encoding: "utf8",
        flag: "wx",
      });
      snapshotWritten = true;
      const newState = await readState();
      return {
        ...newState,
        snapshot_name: snapshotName,
      };
    } catch (error) {
      const rollbackErrors = [];
      if (snapshotWritten) {
        try {
          await unlink(snapshotPath);
        } catch (rollbackError) {
          rollbackErrors.push(rollbackError);
        }
      } else if (error.code !== "EEXIST") {
        try {
          await unlink(snapshotPath);
        } catch (rollbackError) {
          if (rollbackError.code !== "ENOENT") {
            rollbackErrors.push(rollbackError);
          }
        }
      }
      for (const path of writtenPaths.reverse()) {
        const index = paths.indexOf(path);
        try {
          await atomicWrite(path, [rawYaml, registry, report][index]);
        } catch (rollbackError) {
          rollbackErrors.push(rollbackError);
        }
      }
      if (rollbackErrors.length) {
        throw new AggregateError(
          [error, ...rollbackErrors],
          "Writeback failed and repository rollback was incomplete; inspect the Voice-ID-001 files.",
        );
      }
      throw error;
    }
  }

  return {
    getState: () => serialize(readState),
    submit: (payload) => serialize(() => submitSubmission(payload)),
  };
}

function sendJson(response, statusCode, body) {
  response.statusCode = statusCode;
  response.setHeader("Content-Type", "application/json; charset=utf-8");
  response.setHeader("Cache-Control", "no-store");
  response.end(JSON.stringify(body));
}

function isLoopbackAddress(address = "") {
  return (
    address === "127.0.0.1" ||
    address === "::1" ||
    address === "::ffff:127.0.0.1"
  );
}

async function readJsonBody(request) {
  let size = 0;
  const chunks = [];
  for await (const chunk of request) {
    size += chunk.length;
    if (size > maxRequestBytes) {
      throw new WritebackError(413, "Submission exceeds the request size limit.");
    }
    chunks.push(chunk);
  }
  try {
    return JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } catch {
    throw new WritebackError(400, "Submission must contain valid JSON.");
  }
}

export function createVoiceId001WritebackPlugin({ repositoryRoot }) {
  const service = createVoiceId001WritebackService({ repositoryRoot });

  return {
    name: "voice-id-001-local-writeback",
    apply: "serve",
    handleHotUpdate({ file }) {
      if (resolve(file) === resolve(repositoryRoot, experimentRelativePath)) {
        return [];
      }
    },
    configureServer(server) {
      server.middlewares.use((request, response, next) => {
        const requestUrl = new URL(request.url ?? "/", "http://127.0.0.1");
        if (
          requestUrl.pathname !== `${apiPath}/state` &&
          requestUrl.pathname !== apiPath
        ) {
          next();
          return;
        }

        void (async () => {
          if (!isLoopbackAddress(request.socket.remoteAddress)) {
            throw new WritebackError(403, "Repository writeback is available only on loopback.");
          }
          let host;
          try {
            host = new URL(`http://${request.headers.host ?? ""}`).hostname;
          } catch {
            throw new WritebackError(403, "Repository writeback host is not allowed.");
          }
          if (!loopbackHosts.has(host)) {
            throw new WritebackError(403, "Repository writeback host is not allowed.");
          }

          if (requestUrl.pathname === `${apiPath}/state` && request.method === "GET") {
            sendJson(response, 200, await service.getState());
            return;
          }
          if (requestUrl.pathname !== apiPath || request.method !== "POST") {
            throw new WritebackError(404, "Voice-ID-001 writeback route not found.");
          }

          const originHeader = request.headers.origin;
          let origin;
          try {
            origin = originHeader ? new URL(originHeader) : null;
          } catch {
            throw new WritebackError(403, "Voice-ID-001 writeback requires a same-origin request.");
          }
          if (
            !origin ||
            origin.protocol !== "http:" ||
            origin.host !== request.headers.host
          ) {
            throw new WritebackError(403, "Voice-ID-001 writeback requires a same-origin request.");
          }
          if (
            request.headers["sec-fetch-site"] &&
            request.headers["sec-fetch-site"] !== "same-origin"
          ) {
            throw new WritebackError(403, "Cross-origin writeback requests are not allowed.");
          }
          if (
            request.headers["content-type"]?.split(";")[0].trim().toLowerCase() !==
            "application/json"
          ) {
            throw new WritebackError(415, "Content-Type must be application/json.");
          }

          sendJson(response, 201, await service.submit(await readJsonBody(request)));
        })().catch((error) => {
          if (response.headersSent) {
            response.destroy(error);
            return;
          }
          const statusCode = error instanceof WritebackError ? error.statusCode : 500;
          sendJson(response, statusCode, { error: error.message });
        });
      });
    },
  };
}
