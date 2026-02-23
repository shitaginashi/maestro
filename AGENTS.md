SPEC.md: Maestro (errata)
1. Core Architecture
    Engine: MaestroEngineV3 (3.2-STABLE)
    Asset Whitelist: /mega/, /fx/ (Exclude /11/ - redundant/raw).
    Logic: TΔ+1m (1 minute/400 frame ceiling for ranking density).

2. The Tri-Hex System (XXYYZZ)
    XX (Momentum): Spectral Centroid Growth + RMS Delta.
    YY (Impact): Transient/Crest Factor.
    ZZ (Gravity): Mean Spectral Centroid (Pitch/Weight).

3. The "Mirror" Solve (Inversion)
    Method: Inverting Lane C (Suckbacks) into Lane A (Risers).
    Prefilter: initial_spike < (avg_abs * 4). This prevents "Thump-End" artifacts when reversed.
    VSE Hook: strip.use_reverse = True.

4. ERRATA & AGENT STRATEGY (Agent-Specific)
A. The "Ghost Riser" Strategy
Problem: Even with 2,656 Potential Risers, the Sampler may find a high-integrity beat with no matching Riser in the appropriate "Gravity" (ZZ).
Agent Method: The agent should check for "Flippable" assets with a ZZ delta within ±10%. If found, it should force a re-rank of that asset to prioritize it over a native Riser that has a poor ZZ match.

B. Statistical Rarity Dampener (SRD) - Attraction/Repulsion
The SRD uses Rank=Integrity×Total/Count​.
    Repulsion Logic: If Lane B (Hits) becomes >40% of the Spine, the Agent should suggest an "Integrity Tax" of −0.2 on all Lane B assets to force Lane A/C variety.
    Attraction Logic: In high-intensity scenes (TΔ<100 frames), the Agent can bypass the 400-frame culling if the two assets have a ZZ (Gravity) difference >0.5 (e.g., a "Deep Sub" followed by a "High Tinkle").
Refined SRD Logic: Dynamic Culling (The "Rubber Band" Window)

Instead of a hard 400-frame block, the agent should calculate the Culling Radius (Rc​) based on the local density of the Spine.
1. The Formula
Rc​=Integrity×Rarity_Weight400​
    Repulsion: If an asset has high Integrity and high Rarity, it "claims" more territory (up to 400 frames), pushing other assets away to ensure it has the spotlight.
    Attraction (The Override): If the Agent detects a ZZ (Gravity) Delta >0.6 (High frequency vs. Sub-bass), it can apply a 0.5× multiplier to Rc​, allowing a "High-Low" stack even within the safety window.

2. Entropy Compensation
If the Spine density drops below 1 hit per 5 seconds, the Agent should trigger "Ghost Filling":
    Identify the largest gap in the timeline.
    Search legend.yml for the asset with the highest XX (Momentum) that hasn't been used yet.
    Inject into Lane C with inverted: true

C. The Foley "Pitch-In" Rule
While Foley isn't fully supported until M8, it is currently available in the legend.yml.
    Method: If Lane B (Hits) is empty for a specific ZZ range, search class: foley for the same fingerprint.
    Constraint: Only use Foley for "Dull" textures (YY<0.3). Do not use Foley for high-impact cinematic "Hits."

D. FFmpeg Ingestion Errata
    Normalization: Always ingest with -ar 48000 to match Blender's VSE master clock.
    Headroom: If the soundtrack.wav is peaking >−0.1dB, the Materializer may cause clipping in the VSE preview. The Agent should check rms levels and suggest a -6dB pad during FFmpeg conversion if necessary.

5. RECOVERY & TRIAGE
    ModuleNotFoundError: Ensure /mnt/forge/forge/maestro is in sys.path.
    Hanging Indentation: All materialization logic must be contained within the execute or run method scopes.
    Empty Spine: If spine.yml is empty, the agent should fallback to a "Metronome" generation (1 beat every 48 frames) to verify VSE health.