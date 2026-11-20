# Demo Version Lineage

## Conceptual Chain

```text
demo
    ->
development project
    ->
working version
    ->
candidate version
    ->
approved work
    ->
recording
    ->
master
    ->
release
```

Each arrow represents a governed relationship or promotion, not an automatic conversion. The original demo remains immutable after any promotion.

## Future Version Evidence

Each derived version should eventually preserve:

- Parent ID
- Generator and model
- Suno operation
- Prompt and lyrics
- Intended change
- Observed result
- Voice-drift assessment
- Reviewer decision
- Audio checksum

Use stable IDs and `UNKNOWN` for missing values. Store audio in an approved asset location; metadata references its location and checksum.

## Registry Boundary

The `demos.yaml` and `development-projects.yaml` files in this phase are schema examples only. Do not alter the current song registry to represent a demo. Design a future work/composition registry before assigning promoted works into `songs.yaml`.
