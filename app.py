#!/bin/env python

from fig import (
    fig_fps,
    fig_fps_compare,
    fig_GPU,
    fig_GPU_compare,
    fig_throughput,
    fig_throughput_compare,
)
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

df = [None, None]
metadata_dict = [{}, {}]


""" 
    \brief read the meta data from a csv file
    
    \param file_path Path of the file
    
    \return a dict with all meta data
"""


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
            metadata_dict[0] = read_meta(file_path)
            df[0] = pd.read_csv(file_path, header=1)
        if file2:
            file_path = os.path.join(os.getenv("APPDATA"), file2.filename)
            file2.save(file_path)
            metadata_dict[1] = read_meta(file_path)
            df[1] = pd.read_csv(file_path, header=1)
        if file1 or file2:
            return redirect(url_for("index"))

    return render_template(
        "index.html",
        data_loaded=df[0] is not None,
        all_data_loaded=df[0] is not None and df[1] is not None,
    )


@app.route("/plot/<plot_type>")
def plot(plot_type):
    global df
    if df[0] is not None:
        if plot_type == "fps":
            fig = fig_fps(df)
        elif plot_type == "throughput":
            fig = fig_throughput(df)
        elif plot_type == "gpu":
            fig = fig_GPU(df)
        elif plot_type == "throughput_compare" and df[1] is not None:
            fig = fig_throughput_compare(df)
        elif plot_type == "fps_compare" and df[1] is not None:
            fig = fig_fps_compare(df)
        elif plot_type == "gpu_compare" and df[1] is not None:
            fig = fig_GPU_compare(df)
        else:
            return "Invalid plot type", 400
        graph_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
        return render_template("plot.html", graph_html=graph_html)
    else:
        return "No data loaded", 400


if __name__ == "__main__":
    app.run(debug=True)
