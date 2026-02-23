SPEC.md: Maestro
1. Core Architecture
Maestro is an A/V conductor that maps a 3D latent space of audio assets onto a 1D temporal spine in Blender’s VSE.
    Engine: MaestroEngineV3 (3.2-STABLE)
    Environment: Nemo (Blender 4.2 / Python 3.11)
    Whitelisted Directories: /mnt/forge/audio/mega/, /mnt/forge/audio/fx/
    Blacklisted Directories: /mnt/forge/audio/11/ (Raw sessions/Scraps)

2. The Tri-Hex Coordinate System (XXYYZZ)
Every asset is assigned a 6-digit hexadecimal fingerprint based on normalized physics-based metrics (0.0 to 1.0 mapped to 00 to FF).
Vector	Metric	Definition
XX	Momentum	Combination of volume growth (RMS) and Spectral Centroid shift over time.
YY	Impact	Transient peak vs. average RMS ratio (Crest factor).
ZZ	Gravity	Mean Spectral Centroid (Weight/Frequency).
Lane Assignment Logic
    Lane A (Risers): XX>0.5 (High Momentum)
    Lane B (Hits): YY>0.4 (High Impact)
    Lane C (Suckbacks): XX<0.2 (Reverse Momentum)

3. The "Mirror" Asset Solution
Due to population scarcity in Lane A, the system utilizes Population Redistribution.
    Criteria: If a Lane C asset (Suckback) has an initial transient spike <4× its average absolute volume, it is tagged flippable: true.
    Execution: The Sidecar injects an inverted: true flag. The VSE materializer sets strip.use_reverse = True.

4. Ranking Methodology (TΔ+1m Ceiling)
The sampler ranks beats to prevent A/V congestion.
    Square Root Dampener: Rank=Integrity×TotalBeats/LaneCount​
    Culling: 400-frame (16.6s) safety window prevents overlaps. Higher rank assets block lower rank assets within this window.

5. VSE Materialization Handoff
Assets are materialized into the Blender VSE across specific channels:
    Channel 1: Soundtrack (Master Floor)
    Channels 3-5: Discrete Audio Assets (SND_A, SND_B, SND_C)
    Channels 7-9: V31 Control Strips (Visual Markers for Video Handoff)

6. IO Protocols
    Ingestion: ffmpeg -i source.mp3 -ar 48000 -ac 2 soundtrack.wav
    Spine: spine.yml (Source of beat data, t_delta, and integrity).
    Legend: legend.yml (Source of asset paths and Tri-Hex fingerprints).
    Export: EDL format per lane (Title, Event, Type, Start Frame, End Frame).
EOF