import xml.etree.ElementTree as ET
import json
import os

RAW_FILE = "data/raw/modified_sms_v2.xml"
PROCESSED_FILE = "data/processed/sms_records.json"

def parse_sms_xml():
    tree = ET.parse(RAW_FILE)
    root = tree.getroot()

    sms_list = []

    for i, sms in enumerate(root.findall(".//sms"), start=1):
        record = {
            "id":i,
            "address": sms.get("address"),
            "date": sms.get("date"),
            "type": sms.get("type"),
            "body": sms.get("body"),
            "readable_date": sms.get("readable_date"),
            "contact_name": sms.get("contact_name"),
            "service_center": sms.get("service_center"),
            "transaction_id": None
        }

        # Extract Financial Transaction Id from body if present
        body_text = record["body"] or ""
        if "Financial Transaction Id:" in body_text:
            record["transaction_id"] = body_text.split("Financial Transaction Id:")[-1].strip().split()[0]

        sms_list.append(record)

    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)

    with open(PROCESSED_FILE, "w") as f:
        json.dump(sms_list, f, indent=4)

    return sms_list

if __name__ == "__main__":
    data = parse_sms_xml()
    print(f"Parsed {len(data)} SMS records. Saved to {PROCESSED_FILE}")

