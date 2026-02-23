import numpy as np

# --- MOCK SETUP (Simulating your environment) ---
CHANNELS = {
    'a': {'vid': 1, 'aud': 2},
    'b': {'vid': 3, 'aud': 4},
    'c': {'vid': 5, 'aud': 6}
}

class AssetRequest:
    def __init__(self, band, energy, iters=1):
        self.band = band
        self.energy = round(energy, 3)
        self.iters = iters
        self.grid = 81
        self.total_frames = iters * self.grid

class ConductorCore:
    def __init__(self):
        self.grid = 81
        self.timeline = []
        self.locks = {i: 0 for i in range(1, 10)} # Simplified channel range

    def request_placement(self, start_frame, request):
        bt = request.band.lower()
        v_chan, a_chan = CHANNELS[bt]['vid'], CHANNELS[bt]['aud']
        v_end = start_frame + request.total_frames

        # Video (Exclusive/Locking)
        video_status = "DROPPED"
        if self.locks[v_chan] <= start_frame:
            self.timeline.append({
                "T": "VID", "CH": v_chan, "START": start_frame, 
                "END": v_end, "NRG": request.energy, "BT": bt
            })
            self.locks[v_chan] = v_end
            video_status = "PLACED"

        # Audio (Additive/Flat)
        self.timeline.append({
            "T": "AUD", "CH": a_chan, "START": start_frame, 
            "END": start_frame + self.grid, "NRG": request.energy, "BT": bt
        })
        return video_status

# --- THE TEST RUN ---
def test_spine_logic():
    core = ConductorCore()
    limit = 0.5
    
    # Simulating 3 frames of detection
    # Frame 0: Heavy Hit (All bands)
    # Frame 81: Mid-only (B)
    # Frame 162: Collision Test (Try to place A again while locked)
    
    mock_frames = [
        {'f': 0,   'a': 0.9, 'b': 0.8, 'c': 0.9}, 
        {'f': 81,  'a': 0.1, 'b': 0.7, 'c': 0.2},
        {'f': 100, 'a': 0.9, 'b': 0.1, 'c': 0.1} # This should drop Video A
    ]

    print(f"{'FRAME':<8} | {'BAND':<5} | {'VIDEO':<10} | {'ENERGY':<8}")
    print("-" * 40)

    for data in mock_frames:
        f = data['f']
        for b in ['a', 'b', 'c']:
            val = data[b]
            if val > limit:
                req = AssetRequest(band=b, energy=val, iters=1)
                status = core.request_placement(f, req)
                print(f"{f:<8} | {b.upper():<5} | {status:<10} | {val:<8}")

    return core.timeline

timeline = test_spine_logic()