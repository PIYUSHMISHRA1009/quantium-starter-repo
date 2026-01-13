import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load processed data
df = pd.read_csv("processed_pink_morsel_sales.csv")

# Convert columns to correct types
df["date"] = pd.to_datetime(df["date"])
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Aggregate sales per region per day to guard against duplicates
df = (
    df.groupby(["date", "region"], as_index=False)["sales"].sum()
    .sort_values("date")
)

# Create line chart by region
fig = px.line(
    df,
    x="date",
    y="sales",
    color="region",
    labels={
        "date": "Date",
        "sales": "Sales ($)",
        "region": "Region"
    },
    title="Pink Morsel Sales Over Time"
)

# Currency tick formatting
fig.update_yaxes(tickprefix="$", showgrid=True)

# Add price increase marker
fig.add_shape(
    type="line",
    x0="2021-01-15",
    x1="2021-01-15",
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(color="red", dash="dash")
)

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
