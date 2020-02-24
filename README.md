# SG transit analysis

## Plan

use public transport flow data (bus OD and train OD) in Singapore, from the LTA Datamall API, to analyze the human movement pattern in SG, and its effect on spatial disease transmission. 

### Target: find the super-spreader and super-receiver

super-spreader and super-receiver should have the ability to connect to/from high neighborhood-diversity and high location-density places. 

neighborhood-diversity: 

- zone diversity: neighborhood from different "community"
- core-level diversity: neighborhood include location from different core-level

location-density:

- flow density: the density of incoming/outgoing flow