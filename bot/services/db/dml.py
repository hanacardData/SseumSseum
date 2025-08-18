import json
import sqlite3

from bot.services.db.variables import DB_PATH


def upsert_session(user_id: str, step: str, context: dict):
    ctx_str = json.dumps(context, ensure_ascii=False)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
        INSERT INTO session (user_id, step, context, created_at, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id) DO UPDATE SET
            step = excluded.step,
            context = excluded.context,
            updated_at = CURRENT_TIMESTAMP;
        """,
            (user_id, step, ctx_str),
        )
        conn.commit()


def insert_log(user_id: str, context: dict, copy: str):
    ctx_str = json.dumps(context, ensure_ascii=False)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """
        INSERT INTO log (user_id, context, copy)
        VALUES (?, ?, ?)
        """,
            (user_id, ctx_str, copy),
        )
        conn.commit()


def get_session(user_id: str) -> dict[str, str] | None:
    """특정 user_id 의 세션 정보 조회"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  # 결과를 dict 처럼 사용 가능
        cur = conn.cursor()
        cur.execute(
            """
        SELECT
            step,
            context,
            updated_at
        FROM session
        WHERE user_id = ?
        """,
            (user_id,),
        )
        row = cur.fetchone()

        if row is None:
            return None

        # context 는 JSON string 이므로 dict 로 변환
        context = json.loads(row["context"]) if row["context"] else {}

        return {
            "step": row["step"],
            "context": context,
            "updated_at": row["updated_at"],
        }


def get_logs(user_id: str, limit: int = 10) -> list[dict[str, str]]:
    """특정 user_id 의 로그 최신순 조회"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM log
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
        rows = cur.fetchall()

        results = []
        for row in rows:
            context = json.loads(row["context"]) if row["context"] else {}
            results.append(
                {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "context": context,
                    "copy": row["copy"],
                    "created_at": row["created_at"],
                }
            )

        return results
