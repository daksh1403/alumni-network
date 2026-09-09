-- ====================================================================
-- ALUMNI NETWORK AND ENGAGEMENT PLATFORM
-- Master runner: executes all parts in order on a FRESH schema.
-- Usage:  SQL> @run_all.sql
-- ====================================================================
PROMPT >>> Part 0: dropping old objects
@@00_drop_all.sql

PROMPT >>> Part 1: creating schema (14 relations)
@@01_schema.sql

PROMPT >>> Part 2: PL/SQL components
@@02_plsql.sql

PROMPT >>> Part 3: seed data
@@03_seed_data.sql
