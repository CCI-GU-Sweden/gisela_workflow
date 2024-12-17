# general considerations

structures to work on:
- 'Myelin': This is the master layer, it sets the whole analysis, once I find a Mye-obj 
then I look into the other layers to see what is available
- 'Axon'
- 'Dystrophic_myelin'
- 'Mitochondria'

# about calculations
- Label (integer): id that you gave to the myelin segmented region in webknossos.
- myelin_area (float): number of pixels in the myelin region.
- myelin_eccentricity (float): Eccentricity of the ellipse that has the same second-moments as the region. The eccentricity is the ratio of the focal distance (distance between focal points) over the major axis length. The value is in the interval [0, 1). When it is 0, the ellipse becomes a circle. (maybe this figure explains better: https://stackoverflow.com/questions/52406661/eccentricity-of-a-2d-convex-hull-in-python)
- myelin_solidity (float): Ratio of pixels in the region to pixels of the convex hull image.
- myelin_intensity_mean (float): Value with the mean intensity in the region. E.g. how dark/bright the region was.
- myelin_axis_major_length (float): The length of the major axis of the ellipse that has the same normalized second central moments as the region. Note: we now use this mainly as a sanity check for other calculations.
- myelin_axis_minor_length (float): The length of the minor axis of the ellipse that has the same normalized second central moments as the region. Note: we now use this mainly as a sanity check for other calculations.
- myelin_feret_diameter_max (float): Maximum Feret’s diameter computed as the longest distance between points around a region’s convex hull contour as determined by find_contours. Note: we now use this mainly as a sanity check for other calculations.
-myelin_filled_area (int): Number of pixels occupied by the “myelin area” if I fill the hole inside of it. In other words, it is the area of all pixels inside the myelin external boundary.
- myelin_feret_max (float): Maximum Feret’s diameter computed as the longest distance between points around a region’s bounding box as determined by custom code using the rotating calipers algorithm, this is the value we will report from now own and that is demonstrated in the figures.
- myelin_feret_min (float): Minimum Feret’s diameter computed as the longest distance between points around a region’s bounding box as determined by custom code using the rotating calipers algorithm, this is the value we will report from now own and that is demonstrated in the figures.
- myelin_AR (float): Aspect ratio, ratio between the feret minor and major length AR = myelin_feret_max / myelin_feret_min
- myelin_width (float): Median value of the width distribution for the segmented object. This is calculated via the skeleton method + distance to the edge.
-myelin_hole_area (int): Number of pixels occupied by the hole inside the myelin “doughnut”. If the user did not draw a more details axon this should be equal to the axon area.
- myelin_width_min_feret_direction (float): mean value of the width of the axon if I only look at the direction defined by the min feret. In the figure below that would be difference between the blue and orange rectangles along their short axis.
- myelin_width_max_feret_direction (float): mean value of the width of the axon if I only look at the direction defined by the max feret. In the figure below that would be difference between the blue and orange rectangles along their long axis.
- axon_area (float): number of pixels in the user defined axon, if the user did not define an axon we use the end of the myelin as the start of the axon. 
- axon_feret_max (float): Maximum Feret’s diameter computed as the longest distance between points around a region’s bounding box as determined by custom code using the rotating callipers algorithm, this is the value we will report from now own and that is demonstrated in the figures.
- axon_feret_min (float): Minimum Feret’s diameter computed as the longest distance between points around a region’s bounding box as determined by custom code using the rotating callipers algorithm, this is the value we will report from now own and that is demonstrated in the figures.
- axon_AR (float): Aspect ratio, ratio between the feret minor and major length AR = axon_feret_max / axon_feret_min
- mito_total_area (float): number of pixels in all the mito annotated.
- mito_number (float): number of isolated mito objects annotated.
- is_dystrophic (float): was this neuron dystrophic as annotated by the user
For each myelin label I report a figure that shows the bounding box of the myelin in blue, or the “axon_area” as defined by the end of the myelin in orange, and of the actual axon in gree. Please note that some times the bounding boxes might be displaces a few pixels, this is something small I have to fix but it is just the plot, the calculations are correct.



# to implement
When the axon layer exists then calculate the myelin tongue. This will be the iner part that is neither Myelin nor Axon

# from gisela
| Annotaion Layer: | Data wanted:|
| -----------------|-------------|
|Myelin            | Thickness (Width float)|
|Axon              | Diameter (Axis)|
|Mitochondria      | Area        |
|Dystrophic myelin |  Yes/No  |

# about python
will create an env called Gisela, same as COMULIS so far
python v 3.10 to follow recomendation for napari

## env
conda-forge
- python==3.10
- napari
- pyqt
- matplotlib
- jupyterlab==4.1.0
- openjdk
- httpx=0.24
- openpyxl

pip
- webknossos
- pyometiff
- napari-bioformats
