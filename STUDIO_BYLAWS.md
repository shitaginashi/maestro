STUDIO_BYLAWS.md
Project: MAESTRO / Ouroboros architecture
Agent Role: 72B Headless Auditor (Shifu)

Standard: 128d/3d Spatio-Temporal Evaluation
1. Objective

To perform a high-fidelity audit of visual assets, physically segregate technical failures, and provide a mathematically rationalized ranking of "Processed Clips" (pclips) for automated assembly in the Blender VSE.
2. Phase 1: Segregated Culling Protocol

The Auditor shall scan all .mp4 files in the specified directory. Culling is a two-stage process.
2.1 Studio Baseline (Technical)

The following are considered "Useless" and moved to /res immediately:
    Corruption: File read errors or 0kb renders.
    Static Voids: Clips with zero motion vectors across >90% of the 81-frame window.
    Complete Occlusion: Clips that are pure black or pure white (unintentional).

2.2 Director Intervention (Aesthetic Override)

CRITICAL: Before a clip is rejected for "Low Coherency" or "Signal Noise," the Director Persona (director.yml) must evaluate the Intentionality Vector.
    Disturbing vs. Useless: If the Director identifies "Lynchian" textures (e.g., strobing, unsettling blur, high-grain industrial aesthetic), the clip receives a Hard Pass even if it violates standard fidelity metrics.
    Injection: The Director injects a weight multiplier (Wdir​) into the asset metadata before Stage 4.2.

3. Phase 1.5: Feature Extraction

Surviving clips (pclips) are analyzed for:
    Temporal Fingerprint: Identifying the "Riser > Hit > Suckback" curve.
    128d/3d Embedding: Generating the spatial energy map to be saved as project.npy.

4. Phase 2: Temporal Asset Ranking (The Maestro Formula)

The Utility Score (U) for placement suitability is calculated as follows:
U=∑(ΔT+1m(Wstudio​+Wdir​)​)

    ΔT: Temporal distance to the nearest predicted audio beat (a, b, or c).
    1m: The rational ceiling (1ms/1-frame) to prevent asymptotic inflation.
    Wdir​: The aesthetic weight injected by the Director.

5. Director Notes & Migration (director_notes.md)

The 72B must output a comprehensive markdown file containing:
5.1 Individual Clip Critiques
    Identify the "Hero Frame" for each high-ranking pclip.
    Note specific reasons for the Director Override (e.g., "Clip_04 avoided /res because the shutter-drag aligns with Lynchian dream-logic.").

5.2 Holistic Video Philosophy
    Core Values: The overarching "vibe" of the edit.
    Bookending: Specific suggestions for the Title/Opening and the Closing "Suckback."
    Void Mapping: Suggestions for re-renders or specific asset types needed for empty timeline sections.

5.3 Sidecar Migration Segment
    A block of structured data intended for the 8B Sidecar Agent.
    Includes "Sassy/Flex" toggle suggestions for the VSE N-tab (e.g., "Allow extreme temporal stretching on Clip_12").

Architectural Alignment
    Future-Proofing (Chat): The Bylaws are written as "Directives." This allows a future chat interface to ask, "Why did you keep Clip_09?" and the 72B can cross-reference Section 2.2 of the Bylaws to explain its Lynchian reasoning.

    Logic Harvest:
        From SPEC.md: Preserved the 81-frame placeholder logic.
        From video-srd.md: Integrated the Attraction/Repulsion logic into the Wdir​ injection.
        From MAESTRO_MANIFEST: Maintained the A, B, C audio-sync priority.

    The Spine: By dropping project.npy and legend.yml alongside these notes, the 8B agent has a complete map of the Director's intent without needing to re-run the "Lynchian" vision processing.