from collections import defaultdict

def build_summary_email(categorized):
    summary = ""
    for level in ["Critical", "Medium", "Low"]:
        entries = categorized.get(level, [])
        if entries:
            summary += f"\n\n===== {level} Threats ({len(entries)}) =====\n\n"
            for entry in entries[-5:]:  # last 5 threats per level
                summary += entry + "\n"
    return summary or "✅ No threats detected today."


def categorize_alerts(log_path="logs/alerts.log"):
    categorized = defaultdict(list)
    if not os.path.exists(log_path):
        return categorized

    with open(log_path, "r") as f:
        lines = f.readlines()

    current_block = []
    current_severity = "Unknown"

    for line in lines:
        if "Threat Detected" in line:
            # Save previous block
            if current_block:
                categorized[current_severity].append("".join(current_block))
                current_block = []
            if "Critical" in line:
                current_severity = "Critical"
            elif "Medium" in line:
                current_severity = "Medium"
            elif "Low" in line:
                current_severity = "Low"
            else:
                current_severity = "Unknown"
        current_block.append(line)

    # Save the final block
    if current_block:
        categorized[current_severity].append("".join(current_block))

    return categorized
