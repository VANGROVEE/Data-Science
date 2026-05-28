# %% [markdown]
# # A/B Testing Dashboard VANGROVE
# ## Import Library

# %%
import numpy as np 
from scipy import stats

# %% [markdown]
# ## Menyiapkan Data Eksperimen
# 
# Pada eksperimen ini dilakukan perbandingan antara:<br>
# **Dashboard A:** Dashboard dengan filter interaktif<br>
# **Dashboard B:** Dashboard tanpa filter interaktif
# 
# Metrik evaluasi yang digunakan adalah total waktu penyelesaian task (dalam detik).

# %%
# Dashboard A (Dengan Filter)
dashboard_A = [130, 160, 138, 140, 112]

# Dashboard B (Tanpa Filter)
dashboard_B = [144, 120, 72, 93, 105]

# %% [markdown]
# ## Menghitung Statistik Dasar

# %%
mean_A = np.mean(dashboard_A)
mean_B = np.mean(dashboard_B)

std_A = np.std(dashboard_A, ddof=1)
std_B = np.std(dashboard_B, ddof=1) 

print(f"Rata-rata Dashboard A: {mean_A:.2f}") 
print(f"Rata-rata Dashboard B: {mean_B:.2f}") 

print(f"Standar Deviasi Dashboard A: {std_A:.2f}") 
print(f"Standar Deviasi Dashboard B: {std_B:.2f}")

# %% [markdown]
# ## Menentukan Hipotesis
# 
# Hipotesis yang digunakan pada eksperimen ini adalah:<br>
# **Hipotesis Nol (H0):** Tidak terdapat perbedaan signifikan terhadap efisiensi penggunaan dashboard dengan filter interaktif dan dashboard tanpa filter.<br>
# **Hipotesis Alternatif (H1):** Terdapat perbedaan signifikan terhadap efisiensi penggunaan dashboard dengan filter interaktif dan dashboard tanpa filter.

# %% [markdown]
# ## Melakukan Independent Sample t-test
# 
# Pengujian menggunakan Independent Sample t-test karena standar deviasi populasi tidak diketahui, dan jumlah sampel kurang dari 30.

# %%
t_statistic, p_value = stats.ttest_ind(
    dashboard_A, dashboard_B
) 

print(f"T-statistic: {t_statistic:.4f}") 
print(f"P-value: {p_value:.4f}")

# %% [markdown]
# ## Menentukan Keputusan Statistik

# %%
alpha = 0.05 

if p_value < alpha: 
    print("Tolak H0") 
    print("Terdapat perbedaan signifikan antara kedua dashboard") 
else: 
    print("Gagal menolak H0") 
    print("Tidak terdapat perbedaan signifikan antara kedua dashboard")

# %% [markdown]
# ## Interpretasi Hasil

# %%
if p_value < alpha:
    print(f"""
Nilai p-value sebesar {p_value:.4f} lebih kecil dari alpha ({alpha}), sehingga H0 ditolak.

Artinya, terdapat perbedaan signifikan secara statistik antara dashboard dengan filter interaktif dan dashboard tanpa filter terhadap efisiensi waktu penyelesaian analisis data.
""")

else:
    print(f"""
Nilai p-value sebesar {p_value:.4f} lebih besar dari alpha ({alpha}), sehingga gagal menolak H0.

Artinya, tidak terdapat perbedaan signifikan secara statistik antara dashboard dengan filter interaktif dan dashboard tanpa filter terhadap efisiensi waktu penyelesaian analisis data.
""")


