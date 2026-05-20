# -*- coding: utf-8 -*-

def process_table(table_str):
    lines = [line.strip() for line in table_str.strip().split('\n') if line.strip()]
    output = [lines[0], lines[1]]
    
    for line in lines[2:]:
        cols = [c.strip() for c in line.split('|')[1:-1]]
        if len(cols) < 8: continue
        
        try:
            vin = float(cols[1].replace(',', '.'))
            vout = float(cols[2].replace(',', '.'))
        except ValueError:
            continue

        binary = cols[3].strip()
        
        # 1. Рахуємо D_p
        if binary:
            cols[4] = str(int(binary, 2))
        
        # 2. Рахуємо D_розр
        d_calc = round(((255) * vin) / 5.0, 2)
        cols[5] = str(d_calc)
        
        # 3. Рахуємо Delta V (В)
        delta_v = round(vin - vout, 3)
        cols[6] = str(delta_v)
        
        # 4. Рахуємо Delta V (%)
        delta_v_percent = round(((vout - vin) / vin) * 100, 2)
        cols[7] = str(delta_v_percent)
        
        output.append("| " + " | ".join(cols) + " |")
        
    print("\n\n"+"\n".join(output))


def process_dynamic_table(table_str):
    lines = [line.strip() for line in table_str.strip().split('\n') if line.strip()]
    output = [lines[0], lines[1]]
    
    for line in lines[2:]:
        cols = [c.strip() for c in line.split('|')[1:-1]]
        if len(cols) < 5: continue
        
        try:
            sinad = float(cols[3].replace(',', '.'))
        except ValueError:
            continue
            
        # Рахуємо ENOB за формулою (5.5) згідно PDF 
        enob = (sinad - 1.76) / 6.02
        cols[4] = f"{enob:.3f}"
        
        output.append("| " + " | ".join(cols) + " |")
        
    print("\n\n"+"\n".join(output))


process_table(r"""
| N | $V_{in}$, В | $V_{out}$, В | Binary ($D_7 ... D_0$) | $D_{p.}$ | $D_{po3p.}$ | $\Delta V$, В | $\Delta V$, % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 0.500 | 0.473 | 00011001 |  |  |  |  |
| 2 | 0.998 | 0.898 | 00110011 |  |  |  |  |
| 3 | 1.497 | 1.419 | 01001100 |  |  |  |  |
| 4 | 1.994 | 1.896 | 01100110 |  |  |  |  |
| 5 | 2.494 | 2.416 | 01111111 |  |  |  |  |
| 6 | 2.992 | 2.877 | 10011001 |  |  |  |  |
| 7 | 3.492 | 1.952 | 10110010 |  |  |  |  |
| 8 | 3.994 | 3.975 | 11001100 |  |  |  |  |
| 9 | 4.496 | 4.434 | 11100110 |  |  |  |  |
| 10 | 5.000 | 5.000 | 11111111 |  |  |  |  |
""")

process_dynamic_table( r"""
| № | Частота сигналу, Гц | Частота дискретизації, Гц | SINAD, dB | ENOB, bit |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 10   | 10K   | 6.979 | |
| 2 | 50   | 10K   | 6.894 | |
| 3 | 100  | 10K   | 9.718 | |
| 4 | 250  | 10K   | 8.136 | |
| 5 | 500  | 10K   | 4.463 | |
| 6 | 1000 | 10K   | 2.951 | |
""")