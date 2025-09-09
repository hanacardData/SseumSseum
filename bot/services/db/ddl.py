import sqlite3

from bot.services.db.variables import DB_PATH


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        # 외래 키 제약 조건 활성화
        conn.execute("PRAGMA foreign_keys = ON;")
        cur = conn.cursor()

        # session 테이블 생성
        cur.execute("""
        CREATE TABLE IF NOT EXISTS session (
            user_id TEXT PRIMARY KEY,
            step TEXT,
            context TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # log 테이블 생성 (user_id 외래 키 설정)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            channel TEXT,
            purpose TEXT,
            target TEXT,
            description TEXT,
            tone TEXT,
            strategy TEXT,
            title TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES session(user_id)
        );
        """)

        # user_id 인덱스 추가 (조회 성능 개선)
        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_log_user_id ON log(user_id);
        """)

        conn.commit()


if __name__ == "__main__":
    init_db()
