import pandas as pd
import streamlit as sl, subprocess
from rpy2.robjects import pandas2ri, r 
from rpy2 import robjects
import plotly.graph_objects as pg

pandas2ri.activate()

network_frame = pd.read_csv("test_network.csv")
print(network_frame.head())

# pandas df to R 
r_network_frame = pandas2ri.py2rpy(network_frame)

# r code 
r_code = """
library(dplyr)
library(igraph)
library(centiserve)

# Use the network_frame from Python
network_frame <- as.data.frame(network_frame)

# Add the Layer Discount Score to the dataframe
network_frame <- network_frame |>
  mutate(layer_discount = case_when(layer_number == 1 ~ 0.110,
                                    layer_number == 2 ~ 0.051,
                                    layer_number == 3 ~ 0.049,
                                    TRUE ~ 0))

# Create the graph
network_graph <- graph_from_data_frame(network_frame, directed = TRUE)

aS <- .75 # alignment score

# Create a dataframe with the individual node scores and layer scores
node_frame <- network_frame |>
  select(-from) |> # remove the from column
  distinct(to, .keep_all = TRUE) |> # keep only unique node numbers
  rename(node = to) |> # rename the to column to "node"
  arrange(node) |> # order by node number
  mutate(dd = diffusion.degree(network_graph)) |> # calculate the diffusion degree of each node
  mutate(pr = page_rank(network_graph, directed = TRUE)$vector) |> # calculate the page rank score of each node
  mutate(node_mu = dd * pr) # calculate the individual node score

# Create a dataframe for calculating the layer scores
mu_frame <- node_frame |>
  group_by(layer_number) |>
  mutate(layer_mu = sum(node_mu) * layer_discount) |> # calculate the layer node scores
  distinct(layer_number, layer_mu) |> # only keep unique layers
  ungroup() |>
  mutate(layer_mu = round(layer_mu, 3)) # round the layer scores to 3 decimal places

project_mu <- round(sum(mu_frame$layer_mu) * aS, 3) # calculate the overall project score
project_mu
"""

#layer node score - scaled from 1 - 100


# running R code
robjects.globalenv['network_frame'] = r_network_frame
project_score = robjects.r(r_code)

# Display the result in Streamlit
sl.write(f"Project Score: {project_score[0]}")

# ripple effect visualization
fig = pg.Figure()

# Parameters for the ripple effect
num_ripples = 10
max_radius = 10
ripple_spacing = max_radius / num_ripples

# Add circles to simulate ripples
for i in range(1, num_ripples + 1):
    fig.add_trace(pg.Scatter(
        x=[0],
        y=[0],
        mode='markers+lines',
        marker=dict(size=1, color='rgba(0, 0, 255, 0)'),
        line=dict(color=f'rgba(0, 0, 255, {1 - i / num_ripples})', width=2),
        fill='toself',
        hoverinfo='none',
        showlegend=False,
    ))
    fig.update_layout(
        shapes=[dict(
            type='circle',
            xref='x', yref='y',
            x0=-i * ripple_spacing, y0=-i * ripple_spacing,
            x1=i * ripple_spacing, y1=i * ripple_spacing,
            line_color=f'rgba(0, 0, 255, {1 - i / num_ripples})',
        ) for i in range(1, num_ripples + 1)]
    )

# Layout settings
fig.update_layout(
    xaxis=dict(range=[-max_radius, max_radius], zeroline=False),
    yaxis=dict(range=[-max_radius, max_radius], zeroline=False),
    height=600,
    width=600,
    title="Ripple Effect Visualization",
    paper_bgcolor="white",
    plot_bgcolor="white",
    showlegend=False,
)

# Display the plot in Streamlit
sl.plotly_chart(fig)