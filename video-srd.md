SRD: Maestro Video Sampling & Latent Modeling
Project: Maestro / Nemo Integration
Component: Sampler Agent (Video Vectorization & Ranking)

Status: Design Phase (Complete)
1. Core Methodology: The T Delta + 1m Ceiling
    The Spine: Every asset must pass a "Pass 0" audit for signal quality (F(t)).
    The Ceiling: Assets failing the internal metric for bitrate stability or sensor noise are discarded (The 1m ceiling).
    The Sampler: Determines "Heavy" vs. "Lean" segments, replacing flat census metrics with contextual utility.

2. The Video Vector (Vclip​)
Video is expressed as a 3D coordinate within a spatio-temporal hypervolume:
V(t)=[S(t),K(t),F(t)]
    S(t) (Spatial Density): Scene entropy/complexity.
    K(t) (Kinetic Energy): Magnitude of Optical Flow vectors.
    F(t) (Signal Fidelity): Signal-to-noise ratio and compression integrity.

3. Rules of Attraction & Repulsion
The Attraction Vector (Av​) determines the mathematical resonance between Maestro’s audio and the video asset.
Rule	Formula / Parameter	Description
Temporal Gravity	ΔT→0	Alignment of video "hits" to audio 81-frame placeholders.
Kinetic Sympathy	K≈Paudio​	Motion magnitude mirroring audio pressure (RMS).
Chromatic Resonance	ΔL≈Freqaudio​	Luminance shifts matching audio frequency spectrum.

4. Emotional Archetypes (3D Latent Coordinates)
The system interrogates for thematic gravity by mapping archetypes to the latent space:
    Seduction: [Klow​,Slow​,Lhigh​] (Lean, high-tension focus, slow bloom).
    Revenge: [Khigh​,Shigh​,Lstaccato​] (Heavy, chaotic entropy, violent spikes).
    Love/Hate: Polarity weights (we​) that filter for "Abrasive" vs. "Warm" textures.

5. The YAML Utility Belt (Interrogation Passes)
The Sampler Agent executes successive passes based on .yml instruction sets:
    spine.yml: Physical validation (Pass 0).
    attract.yml: Physics-based beat matching.
    archetype.yml: Emotional/Thematic alignment.
    post_fix.yml: Generates Resolve instructions (e.g., "Retime to 115%," "Black Lift +5").

V-CULL GATOR CHEATSHEET

    UID: First 8 chars of pHash (Start Frame).

    P-Tag: "Prime" asset (The best of its UID).

    v-Tag: "Variant" asset (Culled to /cull).

    Iteration: [frames / 81] suffix.

    Fidelity Shield: Hi-Res always beats Low-Res, regardless of loop count.

    Divergence Gate: Divergence at 1s mark creates a new unique asset.