import psycopg2

conn = psycopg2.connect("dbname=aa_proj")
cur = conn.cursor()

cur.execute("SELECT nomorg,assembly FROM organisme\
             WHERE assembly = 'GCA_000009985.1'")
             
res = cur.fetchall()

print(res)

print("res[0]",res[0])
print("res[0][0]",res[0][0])
print("res[0][1]",res[0][1])

conn.close()