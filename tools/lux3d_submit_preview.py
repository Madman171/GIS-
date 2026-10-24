"""Submit the approved Lux3D preview request and download its GLB output."""

from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path


RUNTIME = Path(r"C:\Users\LENOVO\.codex\plugins\cache\openai-curated-remote\aholo-lux3d\0.1.1\skills\lux3d\core\runtime")
ITEMS = Path("preview/ai-pet-v2/lux3d-quote-items.json").resolve()
OUTPUT = Path("preview/ai-pet-v2/lux3d_spirit_pix_v2.glb").resolve()
RECORD = Path("preview/ai-pet-v2/lux3d-attempt.json").resolve()
sys.path.insert(0, str(RUNTIME))

import commerce_client  # noqa: E402
import lux3d_client  # noqa: E402


def parse_datetime(value, field_name):
    text = value.strip().replace("Z", "+00:00")
    text = re.sub(r"(\.\d{6})\d+", r"\1", text)
    parsed = datetime.datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError(f"{field_name} must include a timezone")
    return parsed.astimezone(datetime.timezone.utc)


# The service returns nanosecond timestamps while the bundled Python 3.7
# parser accepts at most six fractional digits.
commerce_client.parse_datetime = parse_datetime

items = json.loads(ITEMS.read_text(encoding="utf-8"))
body = items["1"]["parameters"]["body"]
client = commerce_client.CommerceClient(source=1)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
try:
    account = client.get_account(region="cn")
    normalized_items = commerce_client.normalize_items(items)
    quote = client.create_quote(region="cn", unique_id=account["uniqueId"], items=normalized_items)
    if quote["estimatedCreditsTotal"] != 1:
        raise RuntimeError(f"Quote changed from the approved 1 credit: {quote['estimatedCreditsTotal']}")
    record = {
        "schema": "lux3d.preview-attempt/v1",
        "itemId": "spirit-pix-v2",
        "attemptId": "spirit-pix-v2-lux3d-1",
        "region": "cn",
        "operation": "image-to-3d",
        "version": body["version"],
        "outputFormat": body["outputFormat"],
        "faceCount": body["faceCount"],
        "quoteId": quote["quoteId"],
        "estimatedCredits": quote["estimatedCreditsTotal"],
        "quoteExpiresAt": quote["expiresAt"],
        "status": "submission_started",
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
finally:
    client.close()

task_id = lux3d_client.create_image_to_3d_task(
    img=body["img"],
    version=body["version"],
    faceCount=body["faceCount"],
    outputFormat=body["outputFormat"],
    enablePbr=body["enablePbr"],
    aiPredictSize=body["aiPredictSize"],
    region="cn",
)
record["taskId"] = task_id
record["status"] = "submitted"
RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"taskId": task_id, "quoteId": record["quoteId"]}, ensure_ascii=False))

try:
    formats = lux3d_client.generation_result_formats(body["version"], body["outputFormat"])
    downloads = lux3d_client.complete_task(
        task_id,
        output_path=str(OUTPUT),
        expected_formats=formats,
        region="cn",
        max_attempts=60,
        interval=15,
    )
    record["status"] = "succeeded"
    record["downloadedArtifacts"] = [{"path": str(path), "bytes": size, "format": fmt} for (fmt, (path, size)) in zip(formats, downloads)]
    record["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "succeeded", "downloads": downloads}, ensure_ascii=False))
except Exception as exc:
    record["status"] = "failed"
    record["errorType"] = type(exc).__name__
    record["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    raise
