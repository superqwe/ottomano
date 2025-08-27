import re

def format_log_line(line):
    # Regex per trovare timestamp e livello di log
    match = re.match(r"(\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}\]) (DEBUG|INFO|WARNING|ERROR)", line)
    if match:
        timestamp = match.group(1)
        level = match.group(2).lower()
        # Sostituisci con gli span HTML
        line = line.replace(timestamp, f'<span class="time">{timestamp}</span>')
        line = line.replace(level.upper(), f"<span class='{level}'>{level.upper()}</span>")
    return line

# Esempio di utilizzo
# log_lines = [
#     '[2025-08-22 11:39:30,251] INFO django.server - "GET /personale/estrai_dati HTTP/1.1" 200 32414',
#     '[2025-08-22 11:39:44,272] ERROR django.request - Internal Server Error: /personale/dati_estratti',
#     'Traceback (most recent call last):',
#     '  File "C:\\Users\\L. MASI\\Documents\\Pr',
#     '[2025-08-22 11:39:44,278] ERROR django.server - "POST /personale/dati_estratti HTTP/1.1" 500 98976',
#     '[2025-08-22 11:40:28,471] INFO django.utils.autoreload - C:\\Users\\L. MASI\\Documents\\Programmi\\ottomano\\ottomano\\personale\\estrai_dati_util.py changed, reloading.'
# ]
#
# formatted_lines = [format_log_line(line) for line in log_lines]
#
# for line in formatted_lines:
#     print(line)
