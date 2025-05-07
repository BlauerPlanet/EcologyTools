# Base: Spectrolyzer let you copy the data in the clipboard 
# Step 1: retrieve data from clipboard to pandas dataframe (via GUI or cammnd prompt)
# Step 2: append clipboard content to another dataframe, check wether clipboard content is the same #important not to measure the same sample twice --> could be that same values and therefore not appended to dataframe
# Step 3: interesting Graphics with plotly(+ seaborn, matplotlib, ...?)

# To-Do: 
# - no do:
# - create a tkinter gui interface for selecting stuff from the dataset to draw
# - maybe store data (currently the script must be running at all time)
# - yes do:
# - vertivcal lines for seperating wavelengths (VIS, UV, ...) with small textbox and trasparency color in spektrum color
# - visuelle erklärungen der achsen (y-axis high/low absorption)
# - export as csv maybe also load and save
# - max will das script gerne haben xD --> hab mal so den Hiwi angesprochen als ITler

# coded with assist of ChatGPT for getting along with errors and some of the code logic needed (instad of looking in the docs)

import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
#import tkinter as tk


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
    elif decision == "g":
        df_draw = df.query("group == 'glasses'")
    elif decision == "e":
        df_draw = df
    print(df)
    fig = px.line(df_draw, x="wavelength [nm]", y="absorption", color="sample",title="Comparison between all measurements")
    fig.add_annotation(text="100 - 280 nm: UV-C | 280 - 315 nm: UV-B | 315 - 400 nm: UV-A | 400 - 800 nm: VIS (violet to blue)", xref="paper", yref="paper", x=0.5, y=-0.35, showarrow=False)
    fig.update_layout(margin=dict(b=200))
    fig.show()

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
    df = pd.concat([df_mean_line,df_comp])
    fig = px.line(df, x="wavelength [nm]", y="absorption", color="sample", title="Comparison between last measurement and the mean of all others")
    fig.add_annotation(text="100 - 280 nm: UV-C | 280 - 315 nm: UV-B | 315 - 400 nm: UV-A | 400 - 800 nm: VIS (violet to blue)", xref="paper", yref="paper", x=0.5, y=-0.35, showarrow=False)
    fig.update_layout(margin=dict(b=125))
    fig.show()

if __name__ == "__main__":
    status = 1
    comp_clip = pd.DataFrame()
    data = pd.DataFrame()
    while status != 0:
        command = str(input("type: 'go' to start | 'plot' to show graph(s) | 'end' to stop program: "))
        if command == "go":
            clipboardContent = getClipboard()
            # check wether clipboard contains the same data as last time or conatining data already in the data dataframe
            if not clipboardContent.equals(comp_clip) and not clipboardContent.index.isin(data.index):
                data, status, comp_clip = data_append(data, clipboardContent)
            print(data)
        elif command == "plot":
            data2draw = data
            plot_all_seperate(data2draw)
            choice = str(input("is there data from glasses to compare to a mean? [Y/N]: "))
            if choice == "Y":
                plot_mean_comp(data2draw)

        elif command == "end":
            status = 0
