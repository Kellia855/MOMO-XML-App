import json
import os
import time

# Paths
PROCESSED_FILE = os.path.join("data", "processed", "sms_records.json")

# Load SMS records from JSON
def load_sms():
    with open(PROCESSED_FILE, "r") as f:
        sms_list = json.load(f)
    return sms_list

# Build dictionary for O(1) lookup
def build_dict(sms_list):
    return {sms["transaction_id"]: sms for sms in sms_list if sms["transaction_id"]}

# Linear Search
def linear_search(sms_list, transaction_id):
    for sms in sms_list:
        if sms["transaction_id"] == transaction_id:
            return sms
    return None

# Dictionary Lookup
def dict_lookup(sms_dict, transaction_id):
    return sms_dict.get(transaction_id, None)

def main():
    sms_list = load_sms()
    sms_dict = build_dict(sms_list)

    # Use first 20 records for testing
    test_ids = [sms["transaction_id"] for sms in sms_list[:20] if sms["transaction_id"]]

    linear_times = []
    dict_times = []

    for tid in test_ids:
        # Linear search timing
        start = time.time()
        linear_search(sms_list, tid)
        linear_times.append(time.time() - start)

        # Dictionary lookup timing
        start = time.time()
        dict_lookup(sms_dict, tid)
        dict_times.append(time.time() - start)

    avg_linear = sum(linear_times) / len(linear_times)
    avg_dict = sum(dict_times) / len(dict_times)

    print("=== DSA Comparison: Linear Search vs Dictionary Lookup ===")
    print(f"Average Linear Search Time (20 records): {avg_linear:.8f} seconds")
    print(f"Average Dictionary Lookup Time (20 records): {avg_dict:.8f} seconds")
    print(f"Dictionary lookup is approximately {avg_linear/avg_dict:.1f} times faster than linear search.\n")


if __name__ == "__main__":
    main()

