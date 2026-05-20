import pandas as pd
import glob
import re
import io
import numpy as np


results = {}
files = glob.glob("lr1_2 220 x *.scp*")


common_vin = np.linspace(5.0, 25.0, 20)

for file in files:
    match = re.search(r'x\s+(\d+)', file)
    num_res = match.group(1) if match else "unknown"
    
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    data_start_idx = next(i for i, line in enumerate(lines) if "---" in line) + 1
    df = pd.read_csv(io.StringIO("".join(lines[data_start_idx:])), sep=r"\s+", names=["Time", "Vin", "Vout"])
    

    df_sorted = df.sort_values('Vin')
    vout_interp = np.interp(common_vin, df_sorted['Vin'], df_sorted['Vout'])
    
    results[num_res] = vout_interp


final_df = pd.DataFrame({'Vin': common_vin})
for num in sorted(results.keys(), key=int):
    final_df[f'Vout_{num}R'] = results[num]


final_df = final_df.round(3)

print(r'''
<div align="right">
Таблиця 2: Результати вимірювань вихідної напруги при різних вихідних навантаженнях
</div>
<div align="center" >

''')
print(final_df.to_markdown(index=False))
print(r'''
</div>''')

# Створюємо список для зберігання результатів аналізу
analysis_data = []
VO_NOM = 5.0  # Номінальна вихідна напруга для порівняння
# Розрахунок Line Regulation та збір даних в список
for num in sorted(results.keys(), key=int):
    col_name = f'Vout_{num}R'
    delta_vo = np.max(np.abs(final_df[col_name] - VO_NOM))
    line_reg = 100.0 * (delta_vo / VO_NOM)
    
    analysis_data.append({
        "Кількість резисторів": num,
        "ΔVo (max), B": round(delta_vo, 4),
        "Line Regulation, %": round(line_reg, 2)
    })

# Створення таблиці аналізу
analysis_df = pd.DataFrame(analysis_data)


print(r'''
<div align="right">
Таблиця 3: LINE REGULATION
</div>
<div align="center" >

''')
print(analysis_df.to_markdown(index=False))
print(r'''
</div>''')