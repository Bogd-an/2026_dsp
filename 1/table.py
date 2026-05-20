import pandas as pd

data = [
    {"Vin": 4.0, "Iout": 18, "Vout": 3.843},
    {"Vin": 4.5, "Iout": 20, "Vout": 4.341},
    {"Vin": 6.0, "Iout": 23, "Vout": 4.993},
    {"Vin": 6.5, "Iout": 23, "Vout": 4.995},
    {"Vin": 20.0, "Iout": 23, "Vout": 4.996},
    {"Vin": 24.0, "Iout": 23, "Vout": 4.996},
    {"Vin": 25.0, "Iout": 23, "Vout": 4.996},
]

df = pd.DataFrame(data)
V_NOM = 5.0

df['Delta_Vo'] = df.apply(lambda row: round(abs(row['Vout'] - V_NOM), 3) if row['Vin'] >= 6.0 else '-', axis=1)

md_table = "| № | $V_{in}$, В | $I_{out}$, мА | $V_{out}$, В | $\\Delta V_o$, В |\n"
md_table += "| :--- | :--- | :--- | :--- | :--- |\n"

for i, row in df.iterrows():
    md_table += rf"| {i+1} | {row['Vin']:.1f} | {row['Iout']} | {row['Vout']:.3f} | {row['Delta_Vo']} |" + "\n"

print(md_table)

valid_delta = df[df['Vin'] >= 6.0]['Delta_Vo'].max()
line_reg = (valid_delta / V_NOM) * 100
print(f"\nLine Regulation: {line_reg:.2f}%")