#!/bin/env python

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import os
import plotly.graph_objects as go

app = Flask(__name__)

df = None  # Global variable to store the loaded data
metadata_dict = {}
df_prev = None  # Global variable to store the loaded data
metadata_dict_prev = {}


def fig_fps():
    # use plotly to create a line chart that has each "FPS" column as a line, and the x-axis is the length of the index
    fig = px.line(df, x=range(len(df)), y=["Output FPS"])
    # add à horizontal blue line at the level of the "Input FPS" first value
    fig.add_hline(
        y=df["Input FPS"][20],
        line_dash="dot",
        line_color="blue",
        annotation_text="Input FPS",
        annotation_position="bottom right",
    )

    return fig


def fig_fps_compare():
    trace1_out = go.Scatter(
        x=[e for e in range(len(df))],
        y=df["Output FPS"],
        mode="lines",
        name="Output FPS",
    )

    trace2_out = go.Scatter(
        x=[e for e in range(len(df_prev))],
        y=df_prev["Output FPS"],
        mode="lines",
        name="Output FPS 2",
    )

    trace1_in = go.Scatter(
        x=[e for e in range(len(df))],
        y=df["Input FPS"],
        mode="lines",
        name="Input FPS",
    )

    trace2_in = go.Scatter(
        x=[e for e in range(len(df_prev))],
        y=df_prev["Input FPS"],
        mode="lines",
        name="Input FPS 2",
    )

    layout = go.Layout(
        title="Comparison of Data from Two CSV Files",
        xaxis=dict(title="x"),
        yaxis=dict(title="Value"),
        hovermode="closest",
    )
    fig = go.Figure(data=[trace1_in, trace2_in, trace1_out, trace2_out], layout=layout)

    return fig


def fig_throughput():
    # use plotly to create a line chart that has each "Throughput" column as a line, and the x-axis is the length of the index
    fig = px.line(df, x=range(len(df)), y=["Input Throughput", "Output Throughput"])

    return fig


def fig_throughput_compare():
    trace1 = go.Scatter(
        x=[e for e in range(len(df))],
        y=df["Input Throughput"],
        mode="lines",
        name="Input Throughput",
    )

    trace2 = go.Scatter(
        x=[e for e in range(len(df_prev))],
        y=df_prev["Input Throughput"],
        mode="lines",
        name="Input Throughput 2",
    )

    trace1_out = go.Scatter(
        x=[e for e in range(len(df))],
        y=df["Output Throughput"],
        mode="lines",
        name="Output Throughput",
    )

    trace2_out = go.Scatter(
        x=[e for e in range(len(df_prev))],
        y=df_prev["Output Throughput"],
        mode="lines",
        name="Output Throughput 2",
    )

    layout = go.Layout(
        title="Comparison of Data from Two CSV Files",
        xaxis=dict(title="x"),
        yaxis=dict(title="Value"),
        hovermode="closest",
    )
    fig = go.Figure(data=[trace1, trace2, trace1_out, trace2_out], layout=layout)

    return fig


def fig_GPU_compare():
    trace1_load = go.Scatter(
        x=[e for e in range(len(df))],
        y=df["GPU load"],
        mode="lines",
        name="GPU load",
    )

    trace2_load = go.Scatter(
        x=[e for e in range(len(df_prev))],
        y=df_prev["GPU load"],
        mode="lines",
        name="GPU load 2",
    )

    trace1_mem = go.Scatter(
        x=[e for e in range(len(df))],
        y=df["GPU memory load"],
        mode="lines",
        name="GPU memory load",
    )

    trace2_mem = go.Scatter(
        x=[e for e in range(len(df_prev))],
        y=df_prev["GPU memory load"],
        mode="lines",
        name="GPU memory load 2",
    )

    trace1_div = go.Scatter(
        x=[e for e in range(len(df))],
        y=((df["GPU memory total"] - df["GPU memory free"]) / df["GPU memory total"])
        * 100,
        mode="lines",
        name="GPU Memory division",
    )

    trace2_div = go.Scatter(
        x=[e for e in range(len(df_prev))],
        y=(
            (df_prev["GPU memory total"] - df_prev["GPU memory free"])
            / df_prev["GPU memory total"]
        )
        * 100,
        mode="lines",
        name="GPU Memory division 2",
    )

    layout = go.Layout(
        title="Comparison of Data from Two CSV Files",
        xaxis=dict(title="x"),
        yaxis=dict(title="Value"),
        hovermode="closest",
    )
    fig = go.Figure(
        data=[trace1_load, trace2_load, trace1_mem, trace2_mem, trace1_div, trace2_div],
        layout=layout,
    )

    return fig


def fig_GPU():
    trace1_load = go.Scatter(
        x=[e for e in range(len(df))],
        y=df["GPU load"],
        mode="lines",
        name="GPU load",
    )

    trace1_mem = go.Scatter(
        x=[e for e in range(len(df))],
        y=df["GPU memory load"],
        mode="lines",
        name="GPU memory load",
    )

    trace1_div = go.Scatter(
        x=[e for e in range(len(df))],
        y=((df["GPU memory total"] - df["GPU memory free"]) / df["GPU memory total"])
        * 100,
        mode="lines",
        name="GPU Memory division",
    )

    layout = go.Layout(
        title="Comparison of Data from Two CSV Files",
        xaxis=dict(title="x"),
        yaxis=dict(title="Value"),
        hovermode="closest",
    )
    fig = go.Figure(
        data=[trace1_load, trace1_mem, trace1_div],
        layout=layout,
    )

    return fig


def read_meta(file_path):
    with open(file_path, "r") as file:
        first_line = file.readline()
        metadata = first_line.split(",")
    res = {}
    for meta in metadata:
        key, value = meta.split(": ")
        res[key] = value
    return res


@app.route("/", methods=["GET", "POST"])
def index():
    global df, metadata_dict, df_prev, metadata_dict_prev
    if request.method == "POST":
        print(request.files)
        file1 = request.files["file1"]
        file2 = request.files["file2"]
        if file1:
            file_path = os.path.join(os.getenv("APPDATA"), file1.filename)
            file1.save(file_path)
            metadata_dict = read_meta(file_path)
            df = pd.read_csv(file_path, header=1)
        if file2:
            file_path = os.path.join(os.getenv("APPDATA"), file2.filename)
            file2.save(file_path)
            metadata_dict_prev = read_meta(file_path)
            df_prev = pd.read_csv(file_path, header=1)
        if file1 or file2:
            return redirect(url_for("index"))

    # Pass df status to the template
    return render_template(
        "index.html",
        data_loaded=df is not None,
        all_data_loaded=df is not None and df_prev is not None,
    )


@app.route("/plot/<plot_type>")
def plot(plot_type):
    global df
    if df is not None:
        if plot_type == "fps":
            fig = fig_fps()
        elif plot_type == "throughput":
            fig = fig_throughput()
        elif plot_type == "gpu":
            fig = fig_GPU()
        elif plot_type == "throughput_compare":
            fig = fig_throughput_compare()
        elif plot_type == "fps_compare":
            fig = fig_fps_compare()
        elif plot_type == "gpu_compare":
            fig = fig_GPU_compare()
        else:
            return "Invalid plot type", 400
        graph_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
        return render_template("plot.html", graph_html=graph_html)
    else:
        return "No data loaded", 400


if __name__ == "__main__":
    app.run(debug=True)
