# Cricket Matchup Analysis

A tool that analyzes a batter's ball-by-ball record and generates a bowling
plan against them — strike rate, dismissal rate, and phase-wise output split
by bowler type, with bootstrapped confidence intervals instead of raw
point estimates.

Case study: Vaibhav Sooryavanshi, IPL 2025-2026.

## Why this exists

Public cricket commentary throws around "weakness against spin" or
"struggles in the middle overs" without checking whether the sample size
supports the claim. This project quantifies that — for any batter, not
just one player — using free ball-by-ball data from Cricsheet.

## What it does

- Pulls and cleans ball-by-ball delivery data
- Splits performance by bowler type (pace/spin, left-arm/right-arm) and
  match phase (powerplay/middle/death)
- Estimates dismissal probability and strike rate per matchup type with
  bootstrap confidence intervals
- Flags which "weaknesses" are backed by enough data to trust

## Status

Early build. ETL and matchup engine in progress.

## Setup

(fill in once requirements.txt exists)

## Data source

[Cricsheet](https://cricsheet.org) — free ball-by-ball data, YAML/JSON format.
