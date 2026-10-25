from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

BASE = Path(__file__).parent
BLUE, GREY, ORANGE = "#1f5fa8", "#b4b9c0", "#d9730d"
SEASONS = ["Semi", "Panas", "Gugur", "Dingin"]
WEATHER = ["Cerah", "Berkabut", "Hujan/Salju Ringan"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
SEGMENTS = ["Dini Hari (00-05)", "Pagi Sibuk (06-09)", "Siang (10-15)", "Sore Sibuk (16-19)", "Malam (20-23)"]
TEMP_BINS = ["Dingin (<10°C)", "Sejuk (10-20°C)", "Hangat (20-30°C)", "Panas (>30°C)"]
DEMAND = ["Rendah (<3.000)", "Sedang (3.000-5.500)", "Tinggi (>5.500)"]

st.set_page_config(page_title="Dashboard Bike Sharing", page_icon="🚲", layout="wide")


@st.cache_data
def load_viz():
    return joblib.load(BASE / "viz_data.joblib")


def style(fig, height=380):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    fig.update_yaxes(gridcolor="rgba(128,128,128,.2)", zeroline=False)
    fig.update_xaxes(showgrid=False)
    return fig


viz_all = load_viz()

with st.sidebar:
    st.title("🚲 Bike Sharing")
    st.caption("Capital Bikeshare, Washington D.C. (2011–2012)")
    scope = st.selectbox("Periode", list(viz_all.keys()))

v = viz_all[scope]
kpi = v["kpi"]

st.title("Dashboard Analisis Penyewaan Sepeda")
st.caption(f"Periode: {scope}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total penyewaan", f"{kpi['total']:,.0f}")
c2.metric("Rata-rata per hari", f"{kpi['rata_harian']:,.0f}")
c3.metric("Pengguna terdaftar", f"{kpi['registered']:.0%}")
c4.metric("Pengguna casual", f"{kpi['casual']:.0%}")

tab1, tab2, tab3 = st.tabs(["Pola Jam", "Cuaca & Musim", "Tren & Suhu"])


with tab1:
    st.subheader("Kapan jam puncak penyewaan di hari kerja vs non-kerja?")
    hourly = v["hourly"]
    fig = px.line(hourly, x="hr", y="cnt", color="day_type", markers=True,
                  color_discrete_map={"Hari Kerja": BLUE, "Non-Kerja": ORANGE},
                  labels={"hr": "Jam", "cnt": "Rata-rata penyewaan per jam", "day_type": ""})
    fig.update_layout(showlegend=True, legend=dict(orientation="h", y=1.08), height=400,
                      margin=dict(l=10, r=10, t=30, b=10), plot_bgcolor="rgba(0,0,0,0)",
                      yaxis=dict(gridcolor="rgba(128,128,128,.2)"))
    fig.update_xaxes(dtick=2)
    st.plotly_chart(fig, width="stretch")

    peaks = hourly.loc[hourly.groupby("day_type").cnt.idxmax()]
    st.info(" | ".join(f"**{r.day_type}**: puncak {int(r.hr):02d}:00 (±{r.cnt:,.0f} sewa/jam)"
                       for r in peaks.itertuples()))

    st.markdown("**Porsi penyewaan per segmen waktu**")
    day_type = st.radio("Tipe hari", ["Hari Kerja", "Non-Kerja"], horizontal=True)
    seg = v["segment"].query("day_type == @day_type").set_index("time_segment").reindex(SEGMENTS).reset_index()
    seg["warna"] = seg.time_segment.map(lambda s: BLUE if "Sibuk" in s else GREY)
    fig = px.bar(seg, x="persen", y="time_segment", orientation="h", text="persen",
                 color="warna", color_discrete_map="identity",
                 labels={"persen": "% total penyewaan", "time_segment": ""})
    fig.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[0, max(50, seg.persen.max() + 8)])
    st.plotly_chart(style(fig, 320), width="stretch")


with tab2:
    st.subheader("Seberapa besar cuaca dan musim memengaruhi penyewaan?")
    left, right = st.columns(2)

    w = v["weather"].set_index("weather").reindex(WEATHER).dropna().reset_index()
    base = w.loc[w.weather == "Cerah", "cnt"].iloc[0]
    w["warna"] = w.weather.map(lambda x: BLUE if x == "Cerah" else GREY)
    w["label"] = [f"{c:,.0f}" if n == "Cerah" else f"{c:,.0f} ({c / base - 1:+.0%})"
                  for n, c in zip(w.weather, w.cnt)]
    fig = px.bar(w, x="weather", y="cnt", text="label", color="warna", color_discrete_map="identity",
                 labels={"weather": "", "cnt": "Rata-rata penyewaan harian"})
    fig.update_traces(textposition="outside")
    fig.update_yaxes(range=[0, w.cnt.max() * 1.2])
    left.markdown("**Berdasarkan cuaca**")
    left.plotly_chart(style(fig), width="stretch")

    s = v["season"].set_index("season").reindex(SEASONS).reset_index()
    s["warna"] = s.season.map(lambda x: BLUE if x == s.loc[s.cnt.idxmax(), "season"]
                              else (ORANGE if x == s.loc[s.cnt.idxmin(), "season"] else GREY))
    fig = px.bar(s, x="season", y="cnt", text="cnt", color="warna", color_discrete_map="identity",
                 labels={"season": "", "cnt": "Rata-rata penyewaan harian"})
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_yaxes(range=[0, s.cnt.max() * 1.2])
    right.markdown("**Berdasarkan musim**")
    right.plotly_chart(style(fig), width="stretch")

    hi, lo = s.loc[s.cnt.idxmax()], s.loc[s.cnt.idxmin()]
    st.info(f"Musim tertinggi: **{hi.season}** (±{hi.cnt:,.0f}/hari) | terendah: **{lo.season}** (±{lo.cnt:,.0f}/hari).")

    st.markdown("**Proporsi hari menurut tingkat permintaan (% per musim)**")
    fig = px.bar(v["demand"], x="season", y="persen", color="demand_level", barmode="stack",
                 category_orders={"season": SEASONS, "demand_level": DEMAND},
                 color_discrete_sequence=[ORANGE, GREY, BLUE],
                 labels={"season": "", "persen": "% hari", "demand_level": "Tingkat permintaan"})
    st.plotly_chart(style(fig, 340).update_layout(showlegend=True, legend=dict(orientation="h", y=1.12)),
                    width="stretch")

with tab3:
    st.subheader("Tren bulanan dan pengaruh suhu")
    left, right = st.columns(2)

    m = v["monthly"].copy()
    m["year"] = m.year.astype(str)
    fig = px.line(m, x="month", y="cnt", color="year", markers=True,
                  color_discrete_map={"2011": GREY, "2012": BLUE},
                  category_orders={"month": MONTHS},
                  labels={"month": "", "cnt": "Total penyewaan", "year": "Tahun"})
    left.markdown("**Total penyewaan per bulan**")
    left.plotly_chart(style(fig).update_layout(showlegend=True, legend=dict(orientation="h", y=1.1)),
                      width="stretch")

    t = v["temp"].set_index("temp_bin").reindex(TEMP_BINS).dropna().reset_index()
    t["warna"] = t.temp_bin.map(lambda x: BLUE if x == t.loc[t.cnt.idxmax(), "temp_bin"] else GREY)
    fig = px.bar(t, x="temp_bin", y="cnt", text="cnt", color="warna", color_discrete_map="identity",
                 labels={"temp_bin": "", "cnt": "Rata-rata penyewaan harian"})
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_yaxes(range=[0, t.cnt.max() * 1.2])
    right.markdown("**Rata-rata penyewaan menurut kelompok suhu**")
    right.plotly_chart(style(fig), width="stretch")

st.divider()
st.markdown(
    "**Rekomendasi:** (1) redistribusi sepeda sebelum 07:00 dan 16:00 pada hari kerja; "
    "(2) jadwalkan perawatan pada 00:00–05:00 dan musim Semi; "
    "(3) beri promo pada musim Semi / cuaca buruk dan siapkan armada ekstra pada musim Panas–Gugur."
)
st.caption("Sumber: Capital Bikeshare (UCI Bike Sharing Dataset). Data per jam yang tidak tercatat (165 jam) tidak diimputasi.")
