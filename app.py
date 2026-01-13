import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
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

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="hero",
            children=[
                html.Div(
                    className="title-block",
                    children=[
                        html.H1("Soul Foods Pink Morsel Sales Visualiser"),
                        html.P(
                            "Explore daily Pink Morsel sales and compare performance by region."
                        ),
                    ],
                ),
                html.Div(
                    className="controls",
                    children=[
                        html.Label("Select region", className="label"),
                        dcc.RadioItems(
                            id="region-filter",
                            className="radio",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="card",
            children=[
                html.Div(
                    className="card-header",
                    children=[
                        html.H2("Pink Morsel Sales Over Time"),
                        html.Span("Includes price increase marker on 2021-01-15", className="muted"),
                    ],
                ),
                dcc.Graph(id="sales-chart", config={"displayModeBar": True}),
            ],
        ),
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region: str):
    region_df = df if region == "all" else df[df["region"] == region]

    fig = px.line(
        region_df,
        x="date",
        y="sales",
        color="region",
        labels={
            "date": "Date",
            "sales": "Sales ($)",
            "region": "Region",
        },
        title=None,
    )

    # Currency tick formatting and subtle grid
    fig.update_yaxes(tickprefix="$", showgrid=True, gridcolor="#2b2f36")
    fig.update_xaxes(showgrid=False)

    # Add price increase marker
    fig.add_shape(
        type="line",
        x0="2021-01-15",
        x1="2021-01-15",
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="#ff6b6b", dash="dash"),
    )

    fig.update_layout(
        margin=dict(l=40, r=20, t=20, b=40),
        plot_bgcolor="#11151c",
        paper_bgcolor="#11151c",
        font=dict(color="#e8edf2"),
        legend_title_text="Region",
        hovermode="x unified",
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)
