# Stress test for Parquet queries

We have generated a number of parquet files:
```
...
-rw-r--r--    1 pminkov  staff    17M Jan  8 07:52 output7786.parquet
-rw-r--r--    1 pminkov  staff    17M Jan  8 07:52 output7816.parquet
-rw-r--r--    1 pminkov  staff    17M Jan  8 07:52 output7875.parquet
-rw-r--r--    1 pminkov  staff    17M Jan  8 07:52 output7924.parquet
-rw-r--r--    1 pminkov  staff    17M Jan  8 07:44 output7986696.parquet
-rw-r--r--    1 pminkov  staff    17M Jan  8 07:47 output8056.parquet
...
```

```
$ du -h
4.7G	.
```

The data looks like this:
```
D select * from "*.parquet" limit 5;
┌───────┬───────┐
│  c1   │  c2   │
│ int64 │ int64 │
├───────┼───────┤
│   552 │     1 │
│    80 │     3 │
│   981 │     1 │
│   824 │     9 │
│   475 │     6 │
└───────┴───────┘
```
```
D select count (*) from "*.parquet";
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│   2850000000 │
└──────────────┘
```
That's `2,850,000,000`.


Query 1:
```
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││    Query Profiling Information    ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
explain analyze select avg(c2) from "*.parquet" where c1 = 10;
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││         Total Time: 18.22s        ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
┌───────────────────────────┐
│      EXPLAIN_ANALYZE      │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             0             │
│          (0.00s)          │
└─────────────┬─────────────┘                             
┌─────────────┴─────────────┐
│    UNGROUPED_AGGREGATE    │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          avg(#0)          │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             1             │
│          (0.88s)          │
└─────────────┬─────────────┘                             
┌─────────────┴─────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             c2            │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          2853580          │
│          (0.30s)          │
└─────────────┬─────────────┘                             
┌─────────────┴─────────────┐
│       PARQUET_SCAN        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             c2            │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│  Filters: c1=10 AND c1 IS │
│          NOT NULL         │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│       EC: 570000000       │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│          2853580          │
│         (143.01s)         │
└───────────────────────────┘                        
```

The total time is 18.22s, but the filtering happens in parallel so that's why it
shows 143.01s.
