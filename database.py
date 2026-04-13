import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect("agriculture.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS agriculture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    response TEXT
)
""")

# Insert data
data = [
    ("wheat", "Wheat is a major rabi crop grown in Punjab, Haryana, and UP."),
    ("rice", "Rice is a kharif crop. West Bengal is the largest producer."),
    ("maize", "Maize is grown in Karnataka, MP, and Bihar."),
    ("fertilizer", "Fertilizers include urea, DAP, and potash."),
    ("irrigation", "Irrigation methods include drip, sprinkler, and canals."),
    ("soil", "India has alluvial, black, red, and laterite soils."),
    ("organic farming", "Organic farming avoids chemicals."),
    ("pesticides", "Pesticides protect crops but must be used carefully."),
    ("msp", "MSP is the minimum price given to farmers by government."),
    ("kharif", "Kharif crops are sown in monsoon."),
    ("rabi", "Rabi crops are sown in winter.")
]

cursor.executemany("INSERT INTO agriculture (keyword, response) VALUES (?, ?)", data)

conn.commit()
conn.close()

print("Database created successfully!")
