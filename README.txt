
## General information about the dataset.

"Instances for the Pickup and Delivery Problem with Time Windows 
 based on open data"

===============================================================================
===============================================================================

The instances in this dataset contain information from real-world addresses 
obtained from two different (open) sources:
    (1) The OpenAdresses project. URL: https://openaddresses.io/
    (2) Donovan, B., Work, D., 2016. New york city trip data (2010 to 2013).
        URL: https://doi.org/10.13012/J8PN93H8

Each instance was generated in a specific city, either:
 Barcelona, Berlin, New York, or Porto Alegre.

Travel times were computed using the realistic urban network available for
each city with maps from the OpenStreetMaps project[1], using the Open Source
Routing Machine (OSRM)[2] to compute the shortest paths.

Other characteristics for the instances are detailed in the reference paper.
The file "configurations.txt" also contains detailed attributes for each one
of the instance files.

===============================================================================
===============================================================================

The folder "Instances/" contains all the 300 files grouped by total number
of locations (12 in total): 100, 200, 400, 600, 800, 1000, 1500, 2000, 2500,
3000, 4000, and 5000 locations. There are 25 instances per group.

The folder "Solutions/" contains solutions obtained from the reference paper.

===============================================================================
===============================================================================

Up-to-date tables with best-known solutions can be found in the repository

    https://github.com/cssartori/pdptw-instances

New solutions may be submitted to the referred repository for recording.

===============================================================================
===============================================================================

References:
[1]: OpenStreetMap project, 2017. OSM contributors. Planet dump retrieved
     from https://planet.osm.org. URL: https://www.openstreetmap.org.

[2]: Luxen, D., Vetter, C., 2011. Real-time routing with openstreetmap data. 
     In: Proceedings of the 19th ACM SIGSPATIAL International Conference 
     on Advances in Geographic Information Systems. GIS ’11. ACM, New York, 
     NY, USA, pp. 513–516.

===============================================================================
===============================================================================

## Carlo Sartori and Luciana Buriol (2019).



