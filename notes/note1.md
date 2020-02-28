## Identifying spatial super-spreader and super-receiver in commuting network of Singapore. 

## Highlights

1. The aim of this study is to identify spatial super-spreader and super-receiver from commuting network (public transport flow).
2. Spatial super spreader is the subzones that have stronger ability to spread the disease to the rest of the country in a short time period, i.e. the potential source of outbreak.
3. Spatial super receiver is the subzones that are easily get influences by other places, i.e. the vulnerable places. 
4. Technically, the spreader/receiver index are the integration of the density (local degree centralities),  and the diversity of the outgoing/incoming links, in terms of varying zones and coreness (e.g. city cores and peripheries). 
5. In discussion, the results could be used to suggest the spatially allocation of medical resources and to provide advises for disease control. 

## Introduction

When a new infectious disease strikes a country or a city, the local public health sector authority would need to prevent the spreading of the disease and contain the outbreak situation. A infectious disease which could transmit from human to human, its spreading happens when people closely interact with one another, therefore the people are advise to not oppose themselves in a public space with high density of people, and not to attend or held activities with a large amount of people. 

But, before reaching the city/country lock-down condition, the peoples are still need to go to work or school as usual. In other words, the commuting process would happen as usual. When the commuting process is still working, it indicates the interactions between people would happens and if there is some unidentified patients or infected but asymptomatic persons in the crowds, the spreading of the disease may still occur. In most cases, the government authorities would try to control the disease situation by monitoring the health-care system (sick person is advised to go to doctors) and monitoring the incoming travelers from the airports or checkpoints. From the perspective of spatial governance, it is also important to knows that which part of the city is more vulnerable or has the capability to spread the disease in a short time period; those places should get more attentions in terms of local monitoring and resource allocations. 

The commuting flow of a city is a network representation of people flow in a city. A commuting flow network connect two places with a number indicating the number of people move from the origin to the destination. It could be used to capture the flow of people between places, and also the location where the interaction of people occurs. Therefore, the commuting flow network could be used to identify the places that are more dangerous in terms of spreading disease, namely super-spreader; and the vulnerable places that is easier to get infected, namely super-receiver. 

The aim of this study is to identify the super-spreader and super-receiver in a commuting network. A spatial super-spreader is a location where a lot of people are moving from, and those people are moving to different places; a spatial super-receiver is the destination of a large number of commuters, who come from different places. In other words, there is two keys to identify super-spreader and super-receiver, which is local density and neighborhood diversity. The local densities  of a location are the number of people leaving from or reaching to the location. The neighborhood diversities contains two type of diversity, one of which is the diversity of zones, i.e. are the people come from different parts of the country; another is the diversity of coreness, i.e. are the people come from different types of the country in terms of core or peripheral areas. 

In this study, we present the analysis of Singapore public transport flow network, and identify the spatial super-spreaders and super-receivers using the spreader and receiver indexes, which were calculated based on the local densities and neighborhood diversities measurements. The population flow pattern may be different for weekday and weekend. Thus, the flow data were separated into two parts, weekday and weekend, to show the differences of super-spreaders and super receivers during weekdays and weekends. 



## Methods

The section contain three parts: (a) brief description of the study area, (b) the flow data, and (c) the four steps calculation of the spreader-index and receiver index. 

### Study area

This study focused on the Singapore commuting network flow in Singapore, using the subzone level spatial boundaries (from Master Plan 2014) as the analysis unit. The residential population density were shown in figure 1. There were five regions (Central, West, North, North East, and East), 55 planning areas, and 323 subzones. Some of the subzones contain no residential population (white areas), which includes airports and airbases (e.g. Changi Airport at the East Region) and industrial parks or ports (e.g. Jurong Island and Bukom at the south of the West Region, and Simpang North and South at the North Region). Although these places contain zero residential population, they were the work places (destinations) of a lot of commuters. 

<img src="figures/fig1-population_density_map.png" style="zoom:40%;" />

Figure 1. The subzone residential population density map of Singapore. 

### Flow Data

We used the origin-destination (OD) riderships data of train and bus to create a public transport commuting network. The OD riderships data were collected from the Singapore Land Transport Authority (LTA) through API calls. In this study, we used the riderships data of January 2020. The OD riderships data contains the hourly passenger flows between each pair of train stations and bus stops, and is aggregated into weekday (23 days) or weekend (8 days). 

As the raw data records the flow between bus stops or train stations, we spatially aggregated the data into subzones to subzones flow, according to the bus stops or train stations locations. A total of 303 subzones contains at least one bus stop or one train station. These subzones were used as the nodes (303 nodes) in the commuting network, with the flows between them as the directed and weighted edges (a total of 30331 edges, of which 288 are self-loops and 30043 are inter-subzones edges). 



### Calculation framework

The calculation flow of the spreader and receiver indexes is shown in Figure 2. The first part is to aggregate the bus and train OD flow data to subzones as aforementioned. Then, we got the main data for the calculation, i.e. two weighted and directed networks: weekday and weekend flow network. These networks were used to calculate three network characteristic measurements, including degree centralities (step 1), community detection (step 2), and k-shell decomposition (step 3), which were described in the following subsections. The degree centralities were used as the local out and in flow densities, whereas the community detection and k-shell decomposition results were used to calculate the neighborhood diversities, including zone-entropy and coreness-entropy. Finally, the three network characteristics were used to calculate the spreader index and receiver index. 

<img src="figures/fig2-calculation_flowchart.png" style="zoom:90%;" />

Figure 2. The calculation flow chart of the spreader and receiver index.

#### Step 1: Degree centralities







#### Step 2: Zone-entropy



mapequation



need to change the ln(N) part to the global number of community not neighborhood

zone-entropy
$$
H^{Zone}_{Neigh}(i) = \frac{-\sum_{Z\in Zone(Neigh)} P_i(Z) ln P_i(Z)}{ln |Zone(Neigh)|}
\\
Neigh = \{ OutNeigh, InNeigh \}
\\
P_i(Z) =
    \begin{cases}
      \frac{\sum_{j\in Z \cap Neigh(i)} w(i,j)}{\sum_{k\in Neigh(i)}w(i,k)}, & \text{if}\ Neigh=OutNeigh \\
      \frac{\sum_{j\in Z \cap Neigh(i)} w(j,i)}{\sum_{k\in Neigh(i)}w(k,i)}, & \text{if}\ Neigh=InNeigh
    \end{cases}
$$




#### Step 3: Coreness-entropy

K-shell decomposition is a method to label the coreness of nodes in a network based on the connectivity structure. The weighted k-shell decomposition (Garas et al. 2012) is a extended version that consider both the number of links (degree) and the weights of links (weighted degree). 

1. run weighted K-shell decomposition, use the in/out-degree and weighted in/out-degree (from step 1) to calculate the in/out-k-shell values of each subzone. 
2. use the in/out-k-shell values separately, group the subzones into two parts (coreness): high k-shell (as in/out-core) and low k-shell (as in/out-non-core).
3. For each node (i), check its incoming/outgoing neighbors' coreness, calculate the normalized entropy by using the edge weight (flow) as the probability according to the category of coreness (is the neighbor a core or non-core). Calculation equation is shown as below:


$$
H^{Core}_{Neigh}(i) = \frac{-\sum_{C\in Core(Neigh)} P_i(C) ln P_i(C)}{ln |Core(Neigh)|}
\\
Neigh = \{ OutNeigh, InNeigh \}
\\
P_i(C) =
    \begin{cases}
      \frac{\sum_{j\in C \cap Neigh(i)} w(i,j)}{\sum_{k\in Neigh(i)}w(i,k)}, & \text{if}\ Neigh=OutNeigh \\
      \frac{\sum_{j\in C \cap Neigh(i)} w(j,i)}{\sum_{k\in Neigh(i)}w(k,i)}, & \text{if}\ Neigh=InNeigh
    \end{cases}
$$






#### Step 4: Spreader & receiver index


$$
SpreaderIndex(i) = \sqrt[3]{OutDegree(i) \times H^{Zone}_{OutNeigh}(i) \times H^{Core}_{OutNeigh}(i)}
$$

$$
ReceiverIndex(i) = \sqrt[3]{InDegree(i) \times H^{Zone}_{InNeigh}(i) \times H^{Core}_{InNeigh}(i)}
$$








## Results



#### Degree centralities

<img src="figures/fig3-degree_centralities.png" style="zoom: 50%;" />

Figure 3. The frequency distribution of the degree centralities: first column (a, c, e, g) showed the distribution for weekday dataset, second column (b, d, f, h) showed the distribution for weekend dataset; first row (a, b) showed the non-weighted in-degree, second row (c, d) showed the non-weighted out-degree, third row (e, f) showed the weighted in-degree, and forth row (g, h) showed the weighted out-degree. 



#### Community detection

<img src="figures/fig4-community_detection_result.png" style="zoom:50%;" />

Figure 4. The detected communities for (a) weekday flow data and (b) weekend flow data. The colors indicates the communities. 



#### Coreness

<img src="figures/fig5-kshell_result.png" style="zoom:50%;" />

Figure 5. The coreness of for (a) weekday flow data and (b) weekend flow data. Red color area showed the subzones which were identified as core area for both incoming and outgoing direction, purple color area showed the outgoing core subzones, and pink color showed the incoming core subzones.



#### Spreader & receiver index

<img src="figures/fig6-density_and_diversity.png" style="zoom:50%;" />

Figure 6. The frequency distributions of the six variables for the two datasets: (a-f) weekday and (g-l) weekend. (a, g) showed the local weighted out-degree, (b, h) showed the zone-entropy of the outgoing neighbors, (c, i) showed the outgoing-coreness-entropy of the outgoing neighbors; the three variable were used to calculate the spreader index. (d, j) showed the local weighted in-degree, (e, k) showed the zone-entropy of the incoming neighbors, (f, l) showed the incoming-coreness-entropy of the incoming neighbors; the three variables were used to calculate the receiver index. 



<img src="figures/fig7-SR_index.png" style="zoom: 33%;" />

Figure 7. The frequency distribution of the spreader index (a, b) on the first row, and receiver index (c, d) on the second row, for the two datasets: first column (a, c) for weekday, and second column (b, d) for weekend. The vertical solid lines indicated the mean of the distributions, and the vertical dashed lines showed the two times of standard deviation larger than the mean of the distributions. The subzones lie outside the dashed lines are the subzones with the highest spreader or receiver indexes, which were identified as the super-spreaders and super-receivers. 



#### Super-spreader and super-receiver

<img src="figures/fig8-SR_result_map.png" style="zoom: 40%;" />

Figure 8. The map of the super-spreader and super receiver for: (a) weekday, (b) weekend. The red patches indicated that the subzones were both super-spreader and super-receiver; the purple patches were the super-spreaders; the pink patches were the super receivers. 



## Discussions and conclusion

*core contribution of this study*

This study used 

*limitations*

1. This study covered only the public transportation commuters, specifically, only bus and train riderships were included. Other ways of transportation, including the private or hired automobiles (cars, motorcycles, shuttle buses or vans), and active transportation (by walking, bicycles, skateboards, scooters, etc.) were not included. 
2. Cross-border flows were not included. Many workers in Singapore come from Malaysia and commute in a daily basis. There are some bus services connecting stations in Johor Bahru, Malaysia and various places in Singapore (Woodlands, Jurong East etc.). The in/out flows of these places in Singapore would be underestimated. 



