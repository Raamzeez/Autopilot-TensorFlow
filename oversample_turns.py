import os
import random

# === Config (tweak if you like) ===
MOD_TURN_DEG = 15.0     # degrees: moderate turn threshold
SHARP_TURN_DEG = 35.0  # degrees: sharp turn threshold
MOD_DUP = 2            # total copies for moderate turns (original + 1 extra)
SHARP_DUP = 4          # total copies for sharp turns (original + 3 extras)
SHUFFLE_OUTPUT = True  # shuffle oversampled lines to spread duplicates

def parse_angle_deg(field):
    """
    field looks like: '12.345678,2025-09-30 14:30:25:789' or just '12.345678'
    Return float degrees or None if parse fails.
    """
    try:
        return float(field.split(",")[0])
    except Exception:
        return None

def main():
    dataset_dir = input("Enter dataset directory (e.g., driving_dataset_joined): ").strip()
    data_og_file = os.path.join(dataset_dir, "data_og.txt")
    data_file = os.path.join(dataset_dir, "data.txt")

    # If data_og.txt doesn't exist but data.txt does, rename it first
    if not os.path.exists(data_og_file) and os.path.exists(data_file):
        os.rename(data_file, data_og_file)
        print(f"Renamed original data.txt to data_og.txt")

    if not os.path.exists(data_og_file):
        print(f"[ERROR] Could not find {data_og_file}")
        return

    # --- Read original lines ---
    lines = []
    with open(data_og_file, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                # skip malformed lines quietly
                continue
            angle_deg = parse_angle_deg(parts[1])
            if angle_deg is None:
                # skip lines where angle can't be parsed
                continue
            lines.append((line, angle_deg))

    if not lines:
        print("[ERROR] No valid lines found in data.txt")
        return

    # --- Stats before oversampling ---
    orig_total = len(lines)
    orig_straight = sum(1 for _, a in lines if abs(a) <= MOD_TURN_DEG)
    orig_moderate = sum(1 for _, a in lines if MOD_TURN_DEG < abs(a) <= SHARP_TURN_DEG)
    orig_sharp = sum(1 for _, a in lines if abs(a) > SHARP_TURN_DEG)

    # --- Oversample ---
    oversampled = []
    for line, angle in lines:
        # always include original once
        oversampled.append(line)

        abs_deg = abs(angle)
        if abs_deg > SHARP_TURN_DEG:
            extras = SHARP_DUP - 1
        elif abs_deg > MOD_TURN_DEG:
            extras = MOD_DUP - 1
        else:
            extras = 0

        if extras > 0:
            oversampled.extend([line] * extras)

    if SHUFFLE_OUTPUT:
        random.shuffle(oversampled)

    # --- Write output to data.txt ---
    with open(data_file, "w") as f:
        for line in oversampled:
            f.write(line + "\n")

    # --- Stats after oversampling ---
    new_total = len(oversampled)
    # recompute distribution after duplication
    after_straight = 0
    after_moderate = 0
    after_sharp = 0
    for line in oversampled:
        parts = line.split()
        angle = parse_angle_deg(parts[1])
        if angle is None:
            continue
        if abs(angle) <= MOD_TURN_DEG:
            after_straight += 1
        elif abs(angle) <= SHARP_TURN_DEG:
            after_moderate += 1
        else:
            after_sharp += 1

    print("=== Oversampling Summary ===")
    print(f"Original samples:   {orig_total}")
    print(f"  straight (≤{MOD_TURN_DEG:.0f}°): {orig_straight}  ({orig_straight/max(orig_total,1)*100:.1f}%)")
    print(f"  moderate ({MOD_TURN_DEG:.0f}–{SHARP_TURN_DEG:.0f}°): {orig_moderate}  ({orig_moderate/max(orig_total,1)*100:.1f}%)")
    print(f"  sharp (>{SHARP_TURN_DEG:.0f}°): {orig_sharp}  ({orig_sharp/max(orig_total,1)*100:.1f}%)")
    print()
    print(f"Oversampled samples: {new_total}")
    print(f"  straight (≤{MOD_TURN_DEG:.0f}°): {after_straight}  ({after_straight/max(new_total,1)*100:.1f}%)")
    print(f"  moderate ({MOD_TURN_DEG:.0f}–{SHARP_TURN_DEG:.0f}°): {after_moderate}  ({after_moderate/max(new_total,1)*100:.1f}%)")
    print(f"  sharp (>{SHARP_TURN_DEG:.0f}°): {after_sharp}  ({after_sharp/max(new_total,1)*100:.1f}%)")
    print()
    print(f"[OK] Original data preserved as: {data_og_file}")
    print(f"[OK] Wrote oversampled file as: {data_file}")

if __name__ == "__main__":
    main()