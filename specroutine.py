# Base: Spectrolyzer let you copy the data in the clipboard 
# Step 1: retrieve data from clipboard to pandas dataframe (via GUI or cammnd prompt)
# Step 2: append clipboard content to another dataframe, check wether clipboard content is the same #important not to measure the same sample twice --> could be that same values and therefore not appended to dataframe
# Step 3: interesting Graphics with plotly(+ seaborn, matplotlib, ...?)

# coded with assist of ChatGPT for getting along with errors and some of the code logic needed (instead of looking in the docs)

import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
#import tkinter as tk
from datetime import datetime
from os import listdir, path

def style(df_draw,titlename):
    
    boundary_lines = [(280.0, "UV-C"),(315.0, "UV-B"),(390.0, "UV-A"),(770.0, "VIS (violet -> red)")] # list of tuples with value and name of boundary
    min_y_value = df_draw["absorption"].min()
    max_y_value = df_draw["absorption"].max()
    
    df_draw["wavelength [nm]"] = pd.to_numeric(df_draw["wavelength [nm]"]) # set x-axis to numeric
    
    fig = px.line(df_draw, x="wavelength [nm]", y="absorption", color="sample",title=titlename)
    #fig.add_annotation(text="100 - 280 nm: UV-C | 280 - 315 nm: UV-B | 315 - 400 nm: UV-A | 400 - 800 nm: VIS (violet to blue)", xref="paper", yref="paper", x=0.5, y=-0.35, showarrow=False)
    #fig.update_layout(margin=dict(b=200))
    for x_val, label in boundary_lines:
        fig.add_vline(x=x_val, line_width=2, line_dash="dash", line_color="gray")
        fig.add_annotation(
            x=x_val, y=1, xref="x", yref="paper",
            text=label, showarrow=False, yanchor="bottom",xanchor="right", textangle=0,
            font=dict(size=12, color="gray")
        )
    fig.add_annotation(
        x=-0.06,           # just to the left of the y-axis
        y=max_y_value,     # arrow head at the top
        xref="paper",
        yref="y",
        ax=-0.05,          # same x, since it's vertical
        ay=min_y_value,    # arrow tail at the bottom
        ayref="y",
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="black",
        text="",           # no label, just arrow
    )
    fig.add_annotation(
        x=-0.07,
        xref="paper",
        y=max_y_value,
        yref="y",
        showarrow=False,
        text="less light<br>comes through",
        font=dict(size=12),
        xanchor="right"
    )
    fig.add_annotation(
        x=-0.07,
        xref="paper",
        y= min_y_value,
        yref="y",
        showarrow=False,
        text="much light<br>comes through",
        font=dict(size=12),
        xanchor="right"
    )
    fig.update_layout(margin=dict(l=200))
    fig.show()
# root = tk.Tk()
# root.withdraw()  # Hide main window

# clipboard = pd.DataFrame(root.clipboard_get())

def getClipboard():
    cb = pd.read_clipboard().set_index("Timestamp")
    group = str(input("type 'g' when measurement is related to 'Brillenmessung' and type 'w' if related to water samples: "))
    descr = str(input("provide description for the measurement: "))
    if group == "g":
        cb.insert(0, "group", "glasses")
    elif group == "w":
        cb.insert(0, "group", "water")
    cb.insert(0, "description", descr)
    return cb

def data_append(data, clipboardContent):

    data0 = pd.concat([data,clipboardContent])
    cc = clipboardContent
    stat = 1
    return data0, stat, cc

def plot_all_seperate(data2draw):
    all_rows = []
    x_axis = data2draw.columns[3:]
    for i in data2draw.index:
        y_axis = data2draw.loc[i][3:]
        df_temp = pd.DataFrame({"wavelength [nm]":x_axis,"absorption": y_axis, "group": data2draw.loc[i,'group'], "sample": f"{data2draw.loc[i,'group']} {data2draw.loc[i,'description']}"})
        all_rows.append(df_temp)
    df = pd.concat(all_rows, ignore_index=True)
    decision = str(input("plot individual water data (w) or glasses data (g) or everything (e)?: "))
    if decision == "w":
        df_draw = df.query("group == 'water'")
        choice= ""
    elif decision == "g":
        df_draw = df.query("group == 'glasses'")
        choice = str(input("is there data from glasses to compare to a mean? [Y/N]: "))
    elif decision == "e":
        df_draw = df
        choice= ""
    print(df)
    titlename="Comparison between all measurements"
    style(df_draw,titlename)
    if choice == "Y":
        plot_mean_comp(data2draw)

def plot_mean_comp(data2draw):
    data2use = data2draw.query("group == 'glasses'")
    mean_rows = []
    x_axis = data2use.columns[3:]
    for i in range(len(data2use.index)-1):
        y_axis = data2use.iloc[i][3:]
        df_temp = pd.DataFrame({"wavelength [nm]":x_axis,"absorption": y_axis, "sample": data2use.index[i]})
        mean_rows.append(df_temp)
    dfmean = pd.concat(mean_rows, ignore_index=True)

    df_mean_line = dfmean.groupby("wavelength [nm]", as_index=False)["absorption"].mean()
    df_mean_line["sample"] = "mean"

    y_axis_comp = data2use.iloc[-1][3:]
    df_comp = pd.DataFrame({"wavelength [nm]":x_axis,"absorption": y_axis_comp, "sample": str(data2use["description"][-1])}) # for Timmestamp .index[-1]
    df_draw = pd.concat([df_mean_line,df_comp])
    titlename="Comparison between last measurement and the mean of all others"
    style(df_draw,titlename)

if __name__ == "__main__":
    status = 1
    comp_clip = pd.DataFrame()
    data = pd.DataFrame()
    while status != 0:
        command = str(input("type: 'go' to start | 'save' to save the csv file | 'load' to load data (be sure that only one and the right .csv is in the load folder) | 'plot' to show graph(s) | 'end' to stop program: "))
        if command == "go":
            clipboardContent = getClipboard()
            # check wether clipboard contains the same data as last time or conatining data already in the data dataframe
            if not clipboardContent.equals(comp_clip) and not clipboardContent.index.isin(data.index):
                data, status, comp_clip = data_append(data, clipboardContent)
            print(data)
        elif command == "save":
            prefix=datetime.now().strftime('%Y-%m-%d %H_%M_%S')
            data.to_csv(f"data {prefix}.csv",header=True, index=True, mode="w") # always truncate the old file with same name
        elif command == "load":
            attention = str(input("Are you sure to load data in and replace the current data variable? [Y/N]: "))
            if attention == "Y":
                load_directory=listdir(r"load")
                if len(load_directory) == 1:
                    data = pd.read_csv(path.join("load",load_directory[0]), header=0, index_col=0)
                print(data)
        elif command == "plot":
            data2draw = data
            plot_all_seperate(data2draw)
        elif command == "end":
            status = 0
