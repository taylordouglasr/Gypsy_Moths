# Lymantria
This repository contains the code for data and animations of Lymantria dispar data from the Stop The Spread project. 

The repository is divided into three sections, /data, /scripts and /analysis, with files more or less where you would expect/

DRT was provided with a series of .csv files that contained the X coordinates, Y coordinates, and number of moths trapped for a given year. I don’t have those raw files uploaded here but can provide them upon request.

“Lymantria data.py” is a script that combines all the files in that directory into a single file, “combined_csv.csv”. The same script is also in a Jupyter Notebook, "Combine Trap Data.ipynb"

“Lymantria Static.py” creates an interactive map for the 2016 data. The year can be changed by modifying the script. "2016.html” is the output. The same script is also in the Jupyter Notebook, "Lymantria Single Year Map.ipynb", and it has the same outputs.

Animations across years, "Animated Maps.ipynb" are in progress.

Defoliation data, data from within the native range, and other data in raster format, are works in progress.
