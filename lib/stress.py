from lib.sampler import Sampler

def run_sampler_trials():
    print("--- INITIATING SAMPLER STRESS TEST ---")
    try:
        trent = Sampler("latent_inventory.yml")
    except FileNotFoundError:
        print("ERROR: latent_inventory.yml not found. Run inventory.py first.")
        return

    # Trial 1: The Standard Riser (Phrase Length)
    print("\nTRIAL 1: Seeking '+0-' (Riser/Loop/Dry) @ 5.0s")
    matches = trent.query("+0-", 5.0)
    display_results(matches)

    # Trial 2: The Impulse Hit (Short Duration)
    print("\nTRIAL 2: Seeking '00-' (Static/Loop/Dry) @ 0.5s")
    matches = trent.query("00-", 0.5)
    display_results(matches)

    # Trial 3: The Deep Archive (Long Atmosphere)
    print("\nTRIAL 3: Seeking '00+' (Static/Loop/Wet) @ 45.0s")
    matches = trent.query("00+", 45.0)
    display_results(matches)

def display_results(matches):
    if not matches:
        print("   [!] NO MATCHES FOUND FOR THIS VECTOR.")
        return
    
    print(f"   Found {len(matches)} candidates:")
    for i, m in enumerate(matches):
        prefix = "   WINNER ->" if i == 0 else "   RUNNER ->"
        print(f"{prefix} {m['id']} | {m['t_d']}s | {m['path'].split('/')[-1]}")

if __name__ == "__main__":
    run_sampler_trials()