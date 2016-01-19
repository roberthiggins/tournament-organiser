CREATE TABLE table_allocation(
    entry_id    INTEGER NOT NULL REFERENCES entry(id),
    table_no    INTEGER NOT NULL,
    round_no    INTEGER NOT NULL,
    PRIMARY KEY (entry_id, round_no)
);
COMMENT ON COLUMN table_allocation.table_no IS 'We assume that there are the exact number of tables you need for the players. When this is no longer true we should make this a reference to a table of tables';
