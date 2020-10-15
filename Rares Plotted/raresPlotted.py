import pandas as pd  # (version 1.0.0)
import plotly.express as px  # (version 4.7.0)
import plotly.io as pio
import numpy as np
import plotly.graph_objects as go

df = pd.read_csv('raresPlottedFinal.csv')

fig = px.scatter_3d(
    data_frame=df,
    x='x',
    y='y',
    z='z',
    color="Category",
    # color_discrete_sequence=['magenta'],
    color_discrete_map={'Food': 'green', 'Medicine': 'blue', 'Legal Other': 'orange', 'Weapon': 'red', 'Carthage': 'white'},
    opacity=0.7,                                                # opacity values range from 0 to 1
    # symbol='Distance from Carthage',                                      # symbol used for bubble
    # symbol_map={"0": "diamond"},
    size='Profit',                                              # size of bubble
    size_max=15,                                                # set the maximum mark size when using size
    # log_x=True,   
    # log_y=True,
    # log_z=True,                                               # you can also set log_y and log_z as a log scale
    range_z=[-200,200],                                         # you can also set range of range_y and range_x
    range_x=[-200,200],
    range_y=[-200,200],
    template='plotly_dark', 
    # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
    # 'plotly_white', 'plotly_dark', 'presentation',
    # 'xgridoff', 'ygridoff', 'gridon', 'none'
    title='Rares',
    hover_data={'Commodity': True, 'Station': True, 'Distance from Carthage': True, 'x': False, 'y': False, 'z': False},
    hover_name='System',                                        # values appear in bold in the hover tooltip                                        
)
fig.update_layout(
    scene=dict(
        xaxis=dict(showticklabels=False, showbackground=False, showspikes=False, showgrid=False, zeroline=False, showaxeslabels=False, title=''),
        yaxis=dict(showticklabels=False, showbackground=False, showspikes=False, showgrid=False, zeroline=False, showaxeslabels=False, title=''),
        zaxis=dict(showticklabels=False, showbackground=False, showspikes=False, showgrid=False, zeroline=False, showaxeslabels=False, title=''),
    )
)
pio.show(fig)


# import plotly.express as px
# import plotly.io as pio
# import requests, json, pprint, csv, operator

# systems_populated_api = "https://eddb.io/archive/v6/systems_populated.json"
# systems_populated = requests.get(systems_populated_api).json()

# data = []



# with open('raresPlotted.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     system_array = []
#     for row in csv_reader:
#         if (line_count == 0):
#             line_count += 1
#         else:
#             # system_array.append(row[2])
#             line_count += 1
#     print(f'Processed {line_count} lines.')

# for system in systems_populated:
#     for systems in system_array:
#         if system['name'] == systems:
#             data.append(system)

# with open('raresPlottedW.csv', mode='w') as coordinates_file:
#     coordinates_writer = csv.writer(coordinates_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     coordinates_writer.writerow(['name', 'x', 'y', 'z'])

#     for system in data:
#         coordinates_writer.writerow([system['name'], system['x'], system['y'], system['z']])

# csv1 = open('raresPlottedW.csv', 'r')
# csv_reader = csv.reader(csv1, delimiter=',')
# sort = sorted(csv_reader, key=operator.itemgetter(0))

# for each in sort:
#     print(each)

# details = []
# coordinates = []

# csv_rares_detailed = open('raresPlottedSorted.csv', 'r')
# csv_rares_coordinates = open('raresPlottedWSorted.csv', 'r')
# csv_rares_final = open('raresPlottedFinal.csv', 'w')

# csv_rares_detailed_reader = csv.reader(csv_rares_detailed, delimiter=',')
# csv_rares_coordinates_reader = csv.reader(csv_rares_coordinates, delimiter=',')
# csv_rares_final_writer = csv.writer(csv_rares_final, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


# for rare_details in csv_rares_detailed_reader:
#     details.append(rare_details)

# for rare_coordinates in csv_rares_coordinates_reader:
#     coordinates.append(rare_coordinates)

# # print(details[0][2])
# # print(coordinates[0][0])

# for d in details:
#     for c in coordinates:
#         if d[2] == c[0]:
#             csv_rares_final_writer.writerow([
#                 d[0],
#                 d[1],
#                 d[2],
#                 d[3],
#                 d[4],
#                 d[5],
#                 d[6],
#                 c[1],
#                 c[2],
#                 c[3]
#             ])
