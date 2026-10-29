# Sailing passage summaries

## Purpose and summary

This repository creates concise, single-page sailing passage summaries that are easy for crew to view and zoom on a phone. The current passages are **St Kilda → Deal Island** and **Deal Island → Port Welshpool** aboard Flight in October–November 2026. Each sheet combines a supplied map and passage line, distance and estimated timing, relevant tide information, and communications details.

The summaries are designed to be **iterated with an AI agent**: ask for a change, review the new images, and refine them over several rounds. Each iteration should go into a new timestamped folder so the prior version remains available for comparison.

**These are planning aids, not navigational charts.** Verify the passage, tides and currents, depths, weather and warnings against current sources and local advice before sailing. High or low water is not necessarily current slack. The version README records source and time-zone caveats.

## Ask for another version

Open this repository in your AI coding agent and describe what to change. You do not need to know how the generator works or repeat the versioning instructions. For example:

> On Part 2, enlarge the Rabbit Island tide box and move it away from the passage line.

The repository's [agent guidance](AGENTS.md) tells agents to use the newest version as the baseline, create a new timestamped folder, preserve existing files and map proportions, generate and inspect both phone PNGs and PDFs, and document the result. You can explicitly request a different baseline or an in-place change if that is what you intend.

For new journeys or changed dates, include as much as you know: the route and map files, planned departures, distances and speeds, tide stations and date range, desired contacts or hazards, and any authoritative tide sources or supplied values. Ask the agent to **verify sources and time zones, mark gaps rather than invent predictions, and record assumptions**. Review the result on a phone and give follow-up instructions such as “move this box”, “make the dates larger” or “show another design”.

If a requested change would overwrite a source file or earlier version, clarify that choice first. Keep any original map and passage-plan inputs unchanged unless an explicit update is requested.

## Find and use the latest version

Version folders are named `summaries_YYYYMMDD_HHMMSS`. Sort those folder names in descending order to find the most recently created version. Its PNGs are suited to phone viewing; save them offline and zoom in as needed. Its PDFs are single-page equivalents suited to printing. Read that folder's `README.md` for its specific dates, data sources, assumptions and unresolved issues. Older folders may contain incomplete predictions or alternative layouts.

### Page size and printing

The current output is **custom-sized, not A3**: each PDF has the width of A3 landscape (420 mm), but its height depends on the supplied map's aspect ratio and any additional layout margins. In the current version, Part 1 is approximately **420 × 353.2 mm** and Part 2 **420 × 408.4 mm**. Part 1 includes a margin below the map for the Rip table. The maps are neither stretched nor cropped. To print on A3, choose landscape and **fit to page**; the artwork will be reduced, particularly for Part 2. Check legibility on the chosen printer and paper. A future map or generator change can alter these dimensions.

## Privacy and permitted use

This is intended to be a private repository shared with friends. The passage plan still contains crew names, itinerary and vessel details; review it and other files before sharing more widely. The owner has confirmed that permission for the map and tide data has been granted for this use.

## Technical guidance

Technical information for iterating on and generating summaries, including inputs, dependencies and validation, is in [AGENTS.md](AGENTS.md).
