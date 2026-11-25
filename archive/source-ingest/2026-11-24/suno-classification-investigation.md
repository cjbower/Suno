# Suno Music Generation Investigation
## Lyric Classification, Genre Selection, Vocal Archetypes, Prompt Weighting, and Context Processing

**Author:** Christopher Bower  
**Date:** 2026-11-22  
**Purpose:** Capture observations, experiments, hypotheses, evidence, findings, and open questions from investigation into Suno's music-generation behavior.

---

# Executive Summary

While developing a Nebraska football anthem, repeated attempts to refine the resulting vocalist and production style revealed behavior that could not be explained solely by prompt wording.

Initial assumptions focused on:

- Country-related prompts
- Stadium-related prompts
- Football-related prompts
- Male/female vocalist settings
- Crowd-noise generation
- Production descriptors

After many controlled experiments, evidence suggests Suno may perform semantic analysis and internal classification of both lyrics and style text before generation.

The investigation indicates that:

- Lyrics likely influence classification.
- Style text likely influences classification.
- Instrumentation likely influences classification.
- Prompt placement appears to matter.
- Negative prompts appear weaker than positive prompts.
- Singer selection may be tied to internally classified genre families.
- Some vocal behaviors appear resistant to prompt changes.

A key breakthrough occurred when lyrical content was accidentally placed in the Style field rather than the Lyrics field.

That mistake exposed behavior suggesting the Style field may be interpreted as semantic content rather than purely genre instructions.

---

# Original Problem

Goal:

Create a Nebraska football anthem with:

- Nebraska football themes
- Stadium energy
- Celtic influences
- Heartland influences
- Country influences
- No crowd noise
- No audience clapping
- No gang vocals
- Authentic singer

Observed problem:

The vocalist repeatedly sounded:

- Artificial
- Over-performed
- Throat-heavy
- Forced raspy
- Attempting toughness
- Like a character rather than a real person

Description eventually used:

> "A fat hairy beer-belly truck driver who smokes, drinks, and wants to sound tough."

Even when prompts changed dramatically, this core perception persisted.

---

# Key Findings

## Finding 1

The Style field appears capable of carrying semantic meaning.

Evidence:

Coffee-shop imagery accidentally placed in Style field affected generation.

## Finding 2

Lyrics alone do not appear to fully determine output.

Evidence:

Punk-style overrides produced meaningful changes.

## Finding 3

Negative prompts appear weaker than positive prompts.

Evidence:

Large exclusion lists often failed.

## Finding 4

Prompt placement likely matters.

Evidence:

Mixed-in constraints sometimes appeared stronger than appended constraint blocks.

## Finding 5

Instrumentation may influence classification more than expected.

Evidence:

folk/country/bluegrass classification persisted despite content changes.

## Finding 6

The model appears capable of independently determining:

- Subject matter
- Genre
- Voice family

rather than simply following the prompt literally.

---

# Working Theory

```text
Lyrics
+
Style Text
+
Instrumentation

↓

Semantic Classification

↓

Genre Family

↓

Singer Family

↓

Arrangement

↓

Generation
```

Positive genre signals appear stronger than negative exclusions.

---

# High Priority Future Experiments

## Experiment A

Lyrics: Urban coffee-shop lyrics.

Style: Football anthem instructions.

Goal: Determine dominant source of classification.

## Experiment B

Lyrics: Football anthem.

Style: Alternative Rock, Power Pop, Punk.

Goal: Measure override strength.

## Experiment C

Keep lyrics fixed.

Remove:

- Banjo
- Mandolin
- Fiddle

Goal: Measure instrument influence.

## Experiment D

Use identical lyrics.

Generate:

- Country
- Punk
- Power Pop
- Alternative
- EDM

Goal: Map classification resistance.

---

# Engineering Lesson Learned

The most important discovery may not be the Nebraska song.

The most important discovery may be:

> Suno appears to construct an internal understanding of the song before generation.

If that understanding can be influenced predictably, it may become possible to produce unconventional combinations such as:

- Psalms as EDM
- Church lyrics as Post-Punk
- Patriotic content as Electronic Music
- Football songs as Alternative Rock

while understanding exactly how much effort is required to overcome the model's natural classification tendencies.
