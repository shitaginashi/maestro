# 📂 MAESTRO ARCHITECTURAL MANIFEST [RC0]
**Status:** Stable / Flattened
**Context:** Nemo / The Forge
**Logic:** T-Delta + 1m Ceiling Sampler

---

## 🏗️ DIRECTORY AUTHORITY
All paths are relative to the project root (CWD).
- **Project Root:** `/mnt/forge/forge/maestro`
- **Asset Source:** `/mnt/forge/audio/mega`
- **Blender Link:** `/home/shiro/.config/blender/4.2/scripts/addons/maestro`

## 🧩 COMPONENT MAP
| File | Responsibility |
| :--- | :--- |
| `__init__.py` | Blender Entry Point & Class Registration |
| `maestro_core.py` | Path Resolver & YAML IO |
| `materialize_agent.py` | VSE Strip Creation (Blender 4.2 API Fix) |
| `ranking_agent.py` | Sampler Logic (Heavy vs. Lean) |
| `operators.py` | UI/UX Buttons & N-Tab Definition |
| `conductor.py` | Spine Generator & Metadata Scanner |

## 🎞️ VSE CHANNEL ALLOCATION
- **Channels 1-7:** Video Assets / Generative Strips
- **Channel 8:** **MASTER SOUNDTRACK** (Anchor)
- **Channels 11-13:** Audio Layers (SFX / Latent Braid)

## ⚖️ RANKING METHODOLOGY
- **Sampler Basis:** The census is discarded; ranking is determined by the sampler.
- **The Ceiling:** $T_{\delta} + 1m$ provides the rational ranking ceiling for asset context.
- **Heavy vs. Lean:** Determined by the gap between asset duration and the T-delta.

---

## 🛠️ RECOVERY COMMANDS
**1. Relink Addon:**
`ln -s /mnt/forge/forge/maestro /home/shiro/.config/blender/4.2/scripts/addons/maestro`

**2. Clean Cache:**
`find . -name "__pycache__" -exec rm -rf {} +`

**3. Hard Reset to GitHub:**
`git fetch origin && git reset --hard origin/main`

HLD: Phase-Centric Acoustic Fingerprinting
1. The Complex Vector (A+Bi)
We define the fingerprint not as a scalar (volume), but as a coordinate in a complex spectral plane.
    The Real Component (A): Represents Spectral Magnitude (The "What"). It is the fundamental frequency or the dominant energy bin (4B0).
    The Imaginary Component (i): Represents Phase Stability (The "How").
        +0i (Zero Phase Rotation): Indicates a phase-locked event. This is a "Dry Hit" or a "Transient" where energy is aligned perfectly.
        ±f (Phase Variance/Jitter): Indicates a decorrelated event. This is the signature of a "Wet Suckback" or "Granular Texture" where energy is smeared across frequency and time.

2. Temporal Integrity (The Index)
This digit determines the Linearity of the asset, allowing the Sampler to distinguish between stationary loops and evolving tails.
    Index 0 (Periodic/Stationary): The net phase displacement over the asset's duration is zero.
        Identification: Perfect loops, sustained drones, sine-stable textures.

    Index +1 (Dispersive/Evolving): The phase "wraps" or rotates. The high frequencies lag or lead the fundamental.
        Identification: Chimes, bells, explosive decays, or "Suckbacks" that have a distinct temporal direction.

3. The "Staircase" Constraints

The Spine must adhere to the 81-frame Base + 1m Ceiling.
    81-frame Anchor: Every fingerprint placement on the timeline must be separated by ≥81 frames.
    The 1m (1-meter) Buffer: A "safety margin" that prevents temporal crowding, ensuring the A, B, and C lanes remain discrete and scannable in the VSE.

Summary of Descriptive Categories
Fingerprint Shorthand	Type	Acoustic Behavior	Asset Category
4B0+0i→[0]	Static/Dry	Phase-locked, percussive, loopable.	Kick, Snare, Woodblock.
680±f→[+1]	Dynamic/Wet	Phase-dispersive, evolving, directional.	Chime, Suckback, Cymbal Crash.
Center±f→[0]	Atmospheric	High jitter but stationary/loopable.	Granular Pad, Radio Static.

The 3-Axis Fingerprint Encoding

We encode assets using a normalized float array [X,Y,Z], where each axis represents a specific sonic characteristic.
Axis 1: Momentum (The "Riser" Profile)
    Value Range: 0.0 to 1.0
    Encoding: Measures the amplitude delta over time (the "slope").

    What it means: * 0.0: Flat or instantaneous (a dry snare "hit").
        1.0: Maximum exponential growth (a 4-bar tension riser).
        Usage: Used to filter assets for the "Riser" phase of the audio complement.

Axis 2: Impact Integrity (The "Hit" Profile)
    Value Range: 0.0 to 1.0
    Encoding: Calculated via peak-to-average power ratio (PAPR) at the start of the sample.

    What it means:
        0.0: Soft, atmospheric pad with no clear start.
        1.0: High-transient, "glass-shattering" impact.
        Usage: This directly matches the integrity metric in your spine.yml. High-integrity beats in the Spine demand assets with an Impact value ≈1.0.

Axis 3: Spectral Gravity (The "Suckback" Profile)
    Value Range: 0.0 to 1.0
    Encoding: Based on the Centroid Frequency (the "brightness" or "darkness" of the sound).

    What it means:
        0.0: Sub-heavy, low-frequency rumble (The "Spanish Bass" Lane C).
        1.0: High-frequency, piercing "whisp" or white noise.
        Usage: Defines the "flavor" of the suckback. A value of 0.2 would be a deep, vacuum-like suckback, whereas 0.8 would be a sharp, metallic reverse-cymbal.

The Matching Logic: Attraction vs. Repulsion
In your SRD (Statistical Rarity Design), the engine doesn't just look for a "perfect" match. It calculates the Euclidean Distance between the Spine's requirement and the asset's fingerprint.
Distance=(Xspine​−Xasset​)2+(Yspine​−Yasset​)2+(Zspine​−Zasset​)2​
    Attraction: Assets with a distance <0.15 are "locked" for the Lane.
    Repulsion: If an asset is too similar to one already placed in the 400-frame window, the engine "repels" it to prevent sonic repetitive fatigue, even if the rank is high.

The Fingerprint Mapping by Lane
Lane	Target Axis Focus	Audio Role	Ideal Fingerprint (Approx)
A	Momentum (X)	Risers	[0.9,0.4,0.7]
B	Impact (Y)	Main Hits	[0.2,0.9,0.5]
C	Gravity (Z)	Suckbacks	[0.5,0.3,0.1]
