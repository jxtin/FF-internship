from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots


app = Flask(__name__)


def std_dev(df, col, n):
    return df[col].head(n).std()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        n = request.form.get("N")
        n = int(n)
    else:
        n = 5  # default value

    df = pd.read_csv("ds_new.csv")
    df["std_dev_close"] = df["Close"].rolling(window=n).std()
    df["std_dev_ATR"] = df["ATR"].rolling(window=n).std()
    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        specs=[
            [{"type": "candlestick"}],
            [{"type": "scatter"}],
            [{"type": "scatter"}],
            [{"type": "scatter"}],
        ],
    )

    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["ATR"],
            name="ATR",
            line=dict(color="red", width=2),
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["std_dev_ATR"],
            name="std_dev_ATR",
            line=dict(color="blue", width=2),
        ),
        row=3,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["std_dev_close"],
            name="std_dev_close",
            line=dict(color="green", width=2),
        ),
        row=4,
        col=1,
    )
    fig.update_layout(
        legend_orientation="h",
        xaxis_rangeslider_visible=True,
        # reduce height of range slider
        xaxis_rangeslider=dict(thickness=0.01),
        height=1600,
        width=800,
    )
    fig.update_xaxes(rangeslider={"visible": False}, row=2, col=1)
    fig.update_xaxes(rangeslider={"visible": False}, row=3, col=1)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # dump graphJSON to json file
    with open("graphJSON.json", "w") as f:
        f.write(graphJSON)
    return render_template("index.html", graphJSON=graphJSON)


if __name__ == "__main__":
    app.run(debug=True)
