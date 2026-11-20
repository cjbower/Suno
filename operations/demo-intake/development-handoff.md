# Development Handoff

## Formal Boundary

An Approved Development Brief is the formal boundary between A&R intake and Internal Studio Development. A favorable comment, grade, audience response, or provisional candidate does not authorize production.

The proposed schema example is in [`catalog/metadata/development-projects.yaml`](../../catalog/metadata/development-projects.yaml). It is not a project record.

## Brief Contents

An approved brief identifies:

- `development_id` and source `demo_id`
- `approved_disposition`
- `assigned_entity_type` and `assigned_entity_id`, or explicit `UNKNOWN` / unassigned status
- `source_material_id` and `emotional_objective`
- `elements_to_preserve`, `elements_to_change`, and `prohibited_changes`
- `voice_strategy` and `production_strategy`
- `rights_conditions`
- `success_evidence`
- `approved_by`, `approved_at`, `status`, `current_version`, and `candidate_version`
- `notes` and known limitations

## Handoff Controls

- Preserve the original demo and its checksum.
- Do not create an artist or band merely to make the brief appear complete.
- Keep the work unassigned when no entity fit has been approved.
- Resolve blocking rights conditions before the affected development activity.
- Internal Studio Development owns execution and version creation after approval.
- A frozen candidate version is required before audience research.
- A&R and human editorial review decide whether to revise, hold, assign, promote, hand off, or archive after evidence is returned.

## Promotion

`promoted_to_work` means a separate work/composition record exists. It does not mean a recording, master, or release exists. The demo remains preserved and linked to the work. Do not overload `songs.yaml` before a future work/composition registry is designed.
