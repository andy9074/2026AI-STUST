# 教學重點：tkinter + matplotlib 整合 + filedialog 檔案選擇器
# 流程：點按鈕 → 跳出選檔視窗 → 選 xlsx → 把圖畫在 GUI 視窗裡

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
# FigureCanvasTkAgg 是把 matplotlib 圖塞進 tkinter 的橋樑
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

window = tk.Tk()
window.title("湖西鄉人口分析")
window.geometry("1000x600")

# 上方放按鈕、檔案路徑顯示
上方 = tk.Frame(window)
上方.pack(side="top", fill="x", pady=5)

路徑顯示 = tk.Label(上方, text="（尚未選擇檔案）", fg="gray")
路徑顯示.pack(side="left", padx=10)

# 圖表會放在這個 Frame 裡
圖表區 = tk.Frame(window)
圖表區.pack(side="top", fill="both", expand=True)

# 用一個變數紀錄目前畫布，重新畫圖前要先清掉
目前畫布 = {"obj": None}

def 畫圖(path):
    try:
        df = pd.read_excel(path, header=None, skiprows=1)
        years  = df.iloc[:, 0].astype(int).tolist()
        months = df.iloc[:, 1].astype(int).tolist()
        births = df.iloc[:, 8].astype(int).tolist()
        deaths = df.iloc[:, 9].astype(int).tolist()
    except Exception as e:
        messagebox.showerror("讀檔失敗", str(e))
        return

    labels = [f'{y}/{m:02d}' for y, m in zip(years, months)]
    diff = [b - d for b, d in zip(births, deaths)]
    colors = ['#2E86DE' if v >= 0 else '#E74C3C' for v in diff]

    # 清掉上一張圖（重新選檔時用得到）
    if 目前畫布["obj"] is not None:
        目前畫布["obj"].get_tk_widget().destroy()

    # 用 Figure 物件而不是 plt.figure()，方便嵌進 tkinter
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(len(labels)), diff, color=colors)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=75, fontsize=7)
    ax.set_xlabel('年/月')
    ax.set_ylabel('出生 - 死亡 (人)')
    ax.set_title('湖西鄉 每月自然增加人口 (出生 - 死亡)')
    fig.tight_layout()

    # 把 fig 塞進 tkinter 的 Frame
    canvas = FigureCanvasTkAgg(fig, master=圖表區)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    目前畫布["obj"] = canvas

def 選檔案():
    # 跳出檔案選擇視窗，filetypes 限制可選副檔名
    path = filedialog.askopenfilename(
        title="選擇湖西鄉人口資料",
        filetypes=[("Excel 檔", "*.xlsx *.xls"), ("所有檔案", "*.*")]
    )
    if path:   # 使用者沒按取消才繼續
        路徑顯示.config(text=path, fg="black")
        畫圖(path)

tk.Button(上方, text="選擇檔案", command=選檔案).pack(side="right", padx=10)

window.mainloop()
