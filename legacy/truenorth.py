def true_north_diagnostic(suitability_scores, legend, threshold=0.85):
    top_score = np.max(suitability_scores)
    
    if top_score < threshold:
        print(f"[!] LOW CONFIDENCE MATCH: {top_score:.4f}")
        print(f"[?] The library may lack assets matching this fingerprint.")
    
    # Check if the top results are all from the same directory (Neighborhood lock)
    top_indices = np.argsort(suitability_scores)[::-1][:5]
    paths = [legend[i]['path'] for i in top_indices]
    
    if all("Risers" in p for p in paths):
        print("[!] DIMENSIONAL DRIFT: Search is trapped in the 'Riser' neighborhood.")
        print("[*] Recommendation: Re-calibrate HIT anchors using a known percussion file.")