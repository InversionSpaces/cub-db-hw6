import random
import shutil
import string
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

from dbms.executor import Executor
from dbms.storage import FileStorage
from dbms.visitor import parse


def generate_random_text(min_length: int, max_length: int) -> str:
    length = random.randint(min_length, max_length)
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@dataclass
class Stats:
    queries: int = 0
    rows_inserted: int = 0
    rows_updated: int = 0
    rows_deleted: int = 0
    rows_selected: int = 0
    elapsed: float = 0.0
    _by_type: dict[str, list[float]] = field(default_factory=dict)

    def record(self, query_type: str, duration: float, row_count: int = 0) -> None:
        self.queries += 1
        self._by_type.setdefault(query_type, []).append(duration)
        if query_type == "INSERT":
            self.rows_inserted += row_count
        elif query_type == "UPDATE":
            self.rows_updated += row_count
        elif query_type == "DELETE":
            self.rows_deleted += row_count
        elif query_type == "SELECT":
            self.rows_selected += row_count

    @property
    def total_rows_affected(self) -> int:
        return self.rows_inserted + self.rows_updated + self.rows_deleted

    def qps(self) -> float:
        return self.queries / self.elapsed if self.elapsed > 0 else 0.0

    def format_summary(self, label: str) -> str:
        lines = [
            f"  {label}",
            f"    Elapsed:   {self.elapsed:.1f}s",
            f"    Queries:   {self.queries:,} ({self.qps():,.1f} qps)",
        ]
        if self.rows_inserted:
            lines.append(f"    Inserted:  {self.rows_inserted:,} rows")
        if self.rows_updated:
            lines.append(f"    Updated:   {self.rows_updated:,} rows")
        if self.rows_deleted:
            lines.append(f"    Deleted:   {self.rows_deleted:,} rows")
        if self.rows_selected:
            lines.append(f"    Selected:  {self.rows_selected:,} rows")
        for qt, durations in sorted(self._by_type.items()):
            avg = sum(durations) / len(durations) * 1000
            p50 = sorted(durations)[len(durations) // 2] * 1000
            p99_idx = min(int(len(durations) * 0.99), len(durations) - 1)
            p99 = sorted(durations)[p99_idx] * 1000
            lines.append(f"    {qt:8s}   avg={avg:7.1f}ms  p50={p50:7.1f}ms  p99={p99:7.1f}ms  n={len(durations)}")
        return "\n".join(lines)


def log(msg: str) -> None:
    print(msg, flush=True)


def timed_execute(executor: Executor, sql: str, stats: Stats, query_type: str) -> int:
    t0 = time.time()
    stmt = parse(sql)
    result = executor.execute(stmt)
    duration = time.time() - t0
    row_count = result if isinstance(result, int) else (len(result.rows) if result else 0)
    stats.record(query_type, duration, row_count)
    return row_count


def run_load_test(
    target_mb: int = 10,
    duration_minutes: int = 5,
    batch_size: int = 2000,
    cycle_batch: int = 100,
    report_interval: int = 10,
) -> None:
    temp_dir = Path(tempfile.mkdtemp())
    storage = FileStorage(temp_dir / "test.db")
    executor = Executor(storage)

    executor.execute(parse("CREATE TABLE test (id INT, name TEXT, value INT, data TEXT)"))

    avg_row_size = 8 + 55 + 8 + 1250
    target_bytes = target_mb * 1024 * 1024
    target_rows = target_bytes // avg_row_size
    end_time = time.time() + duration_minutes * 60

    log(f"Load Test: target ~{target_mb} MB ({target_rows:,} rows), {duration_minutes}m timeout")
    log("=" * 60)

    log("Phase 1: Bulk insert")
    phase1 = Stats()
    phase1_start = time.time()
    inserted = 0

    while inserted < target_rows and time.time() < end_time:
        batch_to_insert = min(batch_size, target_rows - inserted)

        values_clauses = []
        for i in range(batch_to_insert):
            row_id = inserted + i
            name = generate_random_text(10, 100)
            value = random.randint(0, 1000000)
            data = generate_random_text(500, 2000)
            values_clauses.append(f"({row_id}, '{name}', {value}, '{data}')")

        values_str = ", ".join(values_clauses)
        count = timed_execute(
            executor,
            f"INSERT INTO test (id, name, value, data) VALUES {values_str}",
            phase1,
            "INSERT",
        )
        inserted += count
        phase1.elapsed = time.time() - phase1_start
        rows_per_sec = inserted / phase1.elapsed if phase1.elapsed > 0 else 0
        log(f"  {inserted:>8,} / {target_rows:,} rows  ({rows_per_sec:,.0f} rows/sec)")

    phase1.elapsed = time.time() - phase1_start
    log(phase1.format_summary("Phase 1 results"))
    log("")

    log("Phase 2: Mixed workload (SELECT + UPDATE + DELETE + INSERT per cycle)")
    phase2 = Stats()
    phase2_start = time.time()
    max_id = inserted
    cycles = 0

    while time.time() < end_time:
        ids = random.sample(range(max_id), min(cycle_batch, max_id))
        or_conditions = " OR ".join(f"id = {row_id}" for row_id in ids)

        timed_execute(executor, f"SELECT * FROM test WHERE {or_conditions}", phase2, "SELECT")

        new_value = random.randint(0, 1000000)
        timed_execute(executor, f"UPDATE test SET value = {new_value} WHERE {or_conditions}", phase2, "UPDATE")

        timed_execute(executor, f"DELETE FROM test WHERE {or_conditions}", phase2, "DELETE")

        values_clauses = []
        for row_id in ids:
            name = generate_random_text(10, 100)
            value = random.randint(0, 1000000)
            data = generate_random_text(500, 2000)
            values_clauses.append(f"({row_id}, '{name}', {value}, '{data}')")
        values_str = ", ".join(values_clauses)
        timed_execute(
            executor,
            f"INSERT INTO test (id, name, value, data) VALUES {values_str}",
            phase2,
            "INSERT",
        )

        cycles += 1
        phase2.elapsed = time.time() - phase2_start

        if cycles % report_interval == 0:
            log(
                f"  cycle {cycles:>5}  "
                f"queries={phase2.queries:,}  "
                f"qps={phase2.qps():,.1f}  "
                f"rows_affected={phase2.total_rows_affected:,}"
            )

    phase2.elapsed = time.time() - phase2_start
    log(phase2.format_summary("Phase 2 results"))
    log("")

    total_elapsed = time.time() - phase1_start
    total_queries = phase1.queries + phase2.queries
    db_size = sum(f.stat().st_size for f in temp_dir.rglob("*") if f.is_file())

    log("=" * 60)
    log("Summary")
    log(f"  Total time:      {total_elapsed:.1f}s")
    log(f"  Total queries:   {total_queries:,} ({total_queries / total_elapsed:,.1f} qps)")
    log(f"  Phase 1 rows:    {phase1.rows_inserted:,}")
    log(f"  Phase 2 cycles:  {cycles}")
    log(f"  Phase 2 queries: {phase2.queries:,}")
    log(f"  DB size:         {db_size / (1024 ** 2):.2f} MB")

    storage.close()
    shutil.rmtree(temp_dir)
    log("Cleaned up.")


if __name__ == "__main__":
    run_load_test()
