import asyncio
import json
import sqlite3
from pathlib import Path

from bot.services.db.variables import DB_PATH
from bot.services.works.payloads.payload import set_text_payload
from bot.services.works.post_content import post_to_works

LOG_FILE = Path("user_log.json")


def get_dau_mau() -> dict | None:
    """오늘 DAU, 이번 달 MAU + timestamp 조회"""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        # 오늘 DAU
        cur.execute(
            """
            SELECT
                DATE('now', 'localtime') AS ts,
                COUNT(DISTINCT user_id) AS dau
            FROM session
            WHERE DATE(updated_at) >= DATE('now', '-1 day', 'localtime');
            """
        )
        dau_row = cur.fetchone()

        # 이번 달 MAU
        cur.execute(
            """
            SELECT
                COUNT(DISTINCT user_id) AS mau
            FROM session
            WHERE DATE(updated_at) >= DATE('now', '-30 day', 'localtime');
            """
        )
        mau_row = cur.fetchone()

        cur.execute(
            """
            SELECT COUNT(*) FROM log;
            """
        )
        num_logs_row = cur.fetchone()
        if dau_row and mau_row:
            return {
                "timestamp": dau_row[0],
                "dau": dau_row[1],
                "mau": mau_row[0],
                "nlogs": num_logs_row[0],
            }
        return None


def save_log(entry: dict):
    """DAU/MAU 결과를 JSON 파일에 append"""
    logs = []
    if LOG_FILE.exists():
        with LOG_FILE.open("r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(entry)
    with LOG_FILE.open("w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    entry = get_dau_mau()
    if entry:
        save_log(entry)
        print("Saved:", entry)
        asyncio.run(
            post_to_works(
                payload=set_text_payload(str(entry)),
                id="d7577f96-1fb8-48ef-16cc-038c8d93f08a",
            )
        )
