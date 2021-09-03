import os
import glob
import pandas as pd

os.chdir("/Users/Douglas/Dropbox/Current Activities/Research/Gypsy Moths/trap_coords")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.DataFrame()

#combine all files in the list
for i in all_filenames:
    temp = pd.read_csv(i)
    yr = i[:-4]
    yr = yr[-4:]
    temp['year'] = yr
    combined_csv = combined_csv.append(temp, ignore_index=True)
combined_csv = combined_csv.sort_values(by=['year'], ignore_index=True)
print(combined_csv)
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

# for each file
#     obtain the year
#     add the year to those data
#     append