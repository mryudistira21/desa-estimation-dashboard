import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Dashboard Estimasi Desa")

# Upload data atau pakai file dari repo
df = pd.read_csv("hasil_estimasi.csv")

# Sidebar pilihan model
model_choice = st.sidebar.selectbox("Pilih model", ["Direct", "Bayesian", "Fay-Herriot"])

# Pilih kolom RSE
rse_col = {"Direct":"rse_direct", "Bayesian":"rse_bayes", "Fay-Herriot":"rse_fh"}[model_choice]

st.write(f"Menampilkan peta dengan model: {model_choice}")

# Load peta desa
import json
import geopandas as gpd
gdf = gpd.read_file("desa.geojson")
gdf = gdf.merge(df, left_on="iddesa", right_on="iddesa")  # sesuaikan key

# Buat peta
m = folium.Map(location=[-0.5, 117], zoom_start=5)
folium.Choropleth(
    geo_data=gdf,
    data=gdf,
    columns=["desa_id", rse_col],
    key_on="feature.properties.desa_id",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f"RSE {model_choice} (%)"
).add_to(m)

st_folium(m, width=700, height=500)

# Tabel RSE
st.write("Tabel RSE:")
st.dataframe(gdf[["desa_id", rse_col]])