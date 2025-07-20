import json
from datetime import datetime


def extract_conversation_metadata(filename):
    metadata_list = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue

            try:
                # Parse the complete JSON object
                record = json.loads(line)

                # Extract the fields that are most useful for analysis
                metadata = {
                    'line_number': line_number,
                    'bot_name': record.get('bot_name', 'Unknown'),
                    'bot_id': record.get('bot_id', 'Unknown'),
                    'timestamp': record.get('submission_timestamp'),
                    'conversation_length': len(record.get('conversation', [])),
                    'has_greeting': bool(record.get('bot_greeting')),
                    'has_definitions': bool(record.get('bot_definitions'))
                }

                # Convert timestamp to readable format if present
                if metadata['timestamp']:
                    metadata['readable_timestamp'] = datetime.fromtimestamp(
                        metadata['timestamp'] / 1000  # Convert from milliseconds
                    ).strftime('%Y-%m-%d %H:%M:%S')

                metadata_list.append(metadata)

                # Optional: Print progress for large files
                if line_number % 1000 == 0:
                    print(f"Processed {line_number} conversation records...")

            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_number}: {e}")
                continue

    return metadata_list


# Example usage for analysis
def analyze_conversation_metadata(metadata_list):
    total_conversations = len(metadata_list)
    total_messages = sum(meta['conversation_length'] for meta in metadata_list)
    unique_bots = len(set(meta['bot_name'] for meta in metadata_list))

    print(f"Dataset Summary:")
    print(f"Total conversations: {total_conversations}")
    print(f"Total messages across all conversations: {total_messages}")
    print(f"Unique bot characters: {unique_bots}")
    print(f"Average messages per conversation: {total_messages / total_conversations:.1f}")

    # Find the most active bots
    bot_counts = {}
    for meta in metadata_list:
        bot_name = meta['bot_name']
        bot_counts[bot_name] = bot_counts.get(bot_name, 0) + 1

    top_bots = sorted(bot_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    print(f"\nTop 10 Most Active Bots:")
    for bot_name, count in top_bots:
        print(f"  {bot_name}: {count} conversations")

analyze_conversation_metadata(extract_conversation_metadata('../Original PIPPA/pippa.jsonl'))