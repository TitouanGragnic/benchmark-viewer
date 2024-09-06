import plotly.graph_objects as go

""" 
    \brief create a trace 
    
    \param data Database
    \param data_name Name of the column
    \param name Name of the trace
    
    \return the trace created
"""


def create_trace(data, data_name, name):
    return go.Scatter(
        x=[e for e in range(len(data))],
        y=data[data_name],
        mode="lines",
        name=name,
    )


""" 
    \brief create a div trace for CPU data
    
    \param data Database
    \param name Name of the trace
    
    \return the trace created
"""


def create_div_trace(data, name):
    return go.Scatter(
        x=[e for e in range(len(data))],
        y=(
            (data["GPU memory total"] - data["GPU memory free"])
            / data["GPU memory total"]
        )
        * 100,
        mode="lines",
        name=name,
    )


""" 
    \brief create a layout 
    
    \param title Title of the trace
    
    \return the layout created
"""


def create_layout(title):
    return go.Layout(
        title=title,
        xaxis=dict(title="x"),
        yaxis=dict(title="Value"),
        hovermode="closest",
    )


""" 
    \brief create 2 trace one input one output 
    
    \param data Database
    \param name Name of the column
    \param is_2 True if it's needed to add a 2 for the name trace
    
    \return tupple of 2 trace
"""


def create_input_output_trace(data, name, is_2):
    return (
        create_trace(data, "Input " + name, "Input " + name + (" 2" if is_2 else "")),
        create_trace(data, "Output " + name, "Output " + name + (" 2" if is_2 else "")),
    )


""" 
    \brief create 3 GPU trace 
    
    \param data Database
    \param is_2 True if it's needed to add a 2 for the name trace
    
    \return tupple of 3 trace
"""


def create_GPU_trace(data, is_2):
    return (
        create_trace(data, "GPU load", "GPU load" + (" 2" if is_2 else "")),
        create_trace(
            data, "GPU memory load", "GPU memory load" + (" 2" if is_2 else "")
        ),
        create_div_trace(data, "GPU Memory division" + (" 2" if is_2 else "")),
    )


""" 
    \brief create a figure of the first database from df
    
    \param df Liste of 2 database 
    \param name Name of the figure wanted
    
    \return the figure created
"""


def create_fig(df, name):
    return go.Figure(
        data=list(create_input_output_trace(df[0], name, False)),
        layout=create_layout("Input/Output " + name),
    )


""" 
    \brief create a figure who compare 2 database
    
    \param df Liste of 2 database
    \param name Name of the figure wanted
    
    \return the figure created
"""


def create_fig_compare(df, name):
    return go.Figure(
        data=list(create_input_output_trace(df[0], name, False))
        + list(create_input_output_trace(df[1], name, True)),
        layout=create_layout("Comparison of Input/Output name"),
    )


""" 
    \brief create a figure for Input/Output FPS
    
    \param df Liste of 2 database
    
    \return the figure created
"""


def fig_fps(df):
    return create_fig(df, "FPS")


""" 
    \brief create a figure who compare Input/Output FPS from 2 database
    
    \param df Liste of 2 database
    
    \return the figure created
"""


def fig_fps_compare(df):
    return create_fig_compare(df, "FPS")


""" 
    \brief create a figure for Input/Output Throughput
    
    \param df Liste of 2 database
    
    \return the figure created
"""


def fig_throughput(df):
    return create_fig(df, "Throughput")


""" 
    \brief create a figure who compare Input/Output Throughput from 2 database
    
    \param df Liste of 2 database
    
    \return the figure created
"""


def fig_throughput_compare(df):
    return create_fig_compare(df, "Throughput")


""" 
    \brief create a figure for GPU Data
    
    \param df Liste of 2 database
    
    \return the figure created
"""


def fig_GPU(df):
    trace_load, trace_mem, trace_div = create_GPU_trace(df[0], False)

    return go.Figure(
        data=[trace_load, trace_mem, trace_div],
        layout=create_layout("GPU Data"),
    )


""" 
    \brief create a figure who compare GPU Data from 2 database
    
    \param df Liste of 2 database
    
    \return the figure created
"""


def fig_GPU_compare(df):
    trace1_load, trace1_mem, trace1_div = create_GPU_trace(df[0], False)
    trace2_load, trace2_mem, trace2_div = create_GPU_trace(df[1], True)

    return go.Figure(
        data=[trace1_load, trace2_load, trace1_mem, trace2_mem, trace1_div, trace2_div],
        layout=create_layout("Comparison of GPU Data"),
    )
