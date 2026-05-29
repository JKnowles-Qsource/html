#!/usr/bin/env python3

import json
import pandas as pd
import plotly.express as px

# ============================================================
# LOAD GeoJSON LOCALLY
# ============================================================

with open("counties.geojson") as f:
    counties = json.load(f)

with open("us-states.geojson") as f:
    states = json.load(f)




# ============================================================
# LOAD DATA
# ============================================================

# CSV must contain:
# FIPS, LocationName, Network

df = pd.read_csv(
    "NWFIPSLocations.csv",
    dtype={"FIPS": str}
)

# Ensure FIPS codes are always 5 digits
df["FIPS"] = df["FIPS"].astype(str).str.replace(".0", "", regex=False).str.zfill(5)

# Convert Network to string so Plotly uses DISCRETE colors
df["Network"] = pd.to_numeric(df["Network"], errors="coerce")
df = df.dropna(subset=["Network"])
df["Network"] = df["Network"].astype(int).astype(str)


# ============================================================
# CREATE COUNTY MAP
# ============================================================

fig = px.choropleth(
    df,
    geojson=counties,
    locations="FIPS",
    color="Network",
    hover_name="LocationName",
    hover_data={
        "FIPS": False,
        "Network": True,
        "Contractor": True,
        "HasDialysisFacility": True
        },
    featureidkey="id",
    scope="usa",
    projection="albers usa",
)
fig.add_choropleth(
    geojson=states,
    locations=[f["properties"]["STATE"] for f in states["features"]],
    z=[1] * len(states["features"]),
    featureidkey="properties.STATE",
    colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
    showscale=False,
    marker_line_color="black",
    marker_line_width=0.9,
    hoverinfo="skip"
)

# ============================================================
# MAP STYLING
# ============================================================

fig.update_geos(
    visible=False,
    showcountries=False,
    showcoastlines=False,
    showland=False,
)

fig.update_layout(
    title="ESRD Networks - County Level",
    legend_title="Network",
    margin={"r":0, "t":50, "l":0, "b":0},
    height=850
)

# ============================================================
# EXPORT TO HTML FOR SHAREPOINT
# ============================================================

output_file = "esrd_network_county_map.html"

fig.write_html(
    output_file,
    full_html=True,
)

print(f"Map exported to: {output_file}")

# Optional local preview
fig.show()
