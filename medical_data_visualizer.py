import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1️⃣ Import Data
df = pd.read_csv("medical_examination.csv")

# 2️⃣ Tambahkan kolom "overweight"
df["BMI"] = df["weight"] / ((df["height"] / 100) ** 2)
df["overweight"] = (df["BMI"] > 25).astype(int)
df.drop(columns=["BMI"], inplace=True)  # Hapus kolom BMI setelah digunakan

# 3️⃣ Normalisasi cholesterol dan glucose
df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
df["gluc"] = (df["gluc"] > 1).astype(int)

# 4️⃣ Fungsi untuk membuat categorical plot
def draw_cat_plot():
    # Pastikan urutan kolom sesuai dengan yang diharapkan dalam tes unit
    category_order = ["active", "alco", "cholesterol", "gluc", "overweight", "smoke"]
    
    # Buat DataFrame untuk categorical plot
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=category_order)  # Urutan diperbaiki di sini
    
    # Buat categorical plot
    fig = sns.catplot(x="variable", hue="value", col="cardio", data=df_cat, kind="count", order=category_order)

    # Pastikan label sumbu X benar
    fig.set_axis_labels("variable", "total")

    # Simpan hasil
    fig.savefig("catplot.png")

    return fig.figure



# 5️⃣ Fungsi untuk membuat heatmap
def draw_heat_map():
    df_heat = df[
        (df["ap_lo"] <= df["ap_hi"]) &
        (df["height"] >= df["height"].quantile(0.025)) &
        (df["height"] <= df["height"].quantile(0.975)) &
        (df["weight"] >= df["weight"].quantile(0.025)) &
        (df["weight"] <= df["weight"].quantile(0.975))
    ]

    corr = df_heat.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", cmap="coolwarm", ax=ax)

    fig.savefig("heatmap.png")

    # Pastikan fungsi mengembalikan fig, bukan array
    return fig  # Perbaiki ini!

