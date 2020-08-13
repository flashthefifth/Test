## Counting Email in a Database

#### To get credit for this assignment, perform the instructions below and upload your SQLite3 database.

### Counting Organizations

This application will read the mailbox data (mbox.txt) and count the number of email messages per organization (i.e. domain name of the email address) using a database with the following schema to maintain the counts.

```sql
CREATE TABLE Counts (org TEXT, count INTEGER)
```

When you have run the program on **mbox.txt**, upload the resulting database file for grading.

If you run the program multiple times in testing or with dfferent files, make sure to empty out the data before each run.

You can use this code as a starting point for your application: http://www.py4e.com/code3/emaildb.py.

The data file for this application is the same as in previous assignments: http://www.py4e.com/code3/mbox.txt.

Because the sample code is using an **UPDATE** statement and committing the results to the database as each record is read in the loop, it might take as long as a few minutes to process all the data. The commit insists on completely writing all the data to disk every time it is called.

The program can be speeded up greatly by moving the commit operation outside of the loop. In any database program, there is a balance between the number of operations you execute between commits and the importance of not losing the results of operations that have not yet been committed. 

## 

### Turning in Assignment 

SQLite3 database: *[emaildb.sqlite](/emaildb.sqlite)* (The top organizational count is 536.)

Python Code:

```python
import sqlite3
import re

# Create sqlite3 connection and cursor object
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()
# Start fresh
cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

fname = input() or 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    # Extract the org domains using regex
    result = re.findall(r'@(\S+)', line)
    if len(result) > 0 : org = result[0]
    # Check the current status of the above org
    cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
    row = cur.fetchone()
    # Update the org, or add it if doesn't exist
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
        # Keeping commits after every new org is added
        conn.commit()
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
conn.commit()

# # Check the top 10 domains used
# sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
# for row in cur.execute(sqlstr):
#     print(str(row[0]), row[1])
cur.close()
```