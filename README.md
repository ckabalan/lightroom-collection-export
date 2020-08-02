# Lightroom Collection Export

Quick and dirty script to read a Lightroom Database (`*.lrcat`) file and make
a directory structure based on the Collection structure.

The `lrcat` file is actually a SQL Database, but for this simple application
it wasn't worth figuring out recursion in SQL statements with joins, so I
just exported every table to CSV using the "DB Browser for SQLite" tool.

# License

MIT