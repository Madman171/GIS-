"""Quote Lux3D work around the Python 3.7 fractional-second parser gap."""

from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path


RUNTIME = Path(r"C:\Users\LENOVO\.codex\plugins\cache\openai-curated-remote\aholo-lux3d\0.1.1\skills\lux3d\core\runtime")
ITEMS = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(RUNTIME))
import commerce_client  # noqa: E402


def parse_datetime(value, field_name):
    text = value.strip().replace("Z", "+00:00")
    text = re.sub(r"(\.\d{6})\d+", r"\1", text)
    parsed = datetime.datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError(f"{field_name} must include a timezone")
    return parsed.astimezone(datetime.timezone.utc)


commerce_client.parse_datetime = parse_datetime
client = commerce_client.CommerceClient(source=1)
try:
    account = client.get_account(region="cn")
    items = commerce_client.normalize_items(json.loads(ITEMS.read_text(encoding="utf-8")))
    quote = client.create_quote(region="cn", unique_id=account["uniqueId"], items=items)
    print(json.dumps({"account": account, "quote": quote}, ensure_ascii=False, indent=2))
finally:
    client.close()
