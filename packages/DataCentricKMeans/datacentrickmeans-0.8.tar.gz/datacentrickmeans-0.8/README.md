 # DataCentricKMeans Package Documentation

 ## Introduction

 Introducing **DataCentricKmeans**: A fast, eco-friendly clustering solution that harnesses the power of geometry to revolutionize the classic k-means algorithm. Designed for both speed and sustainability, it offers unparalleled performance for your clustering needs—from small to big data sets. The package also provides API calls to existing faster alternatives of k-means.

 ### Advantages of DataCentricKmeans

 - Significantly faster convergence and reduced runtime, especially for large datasets.
 - Significant reduction in the number of distance computations.
 - Maintains the same clustering quality as traditional k-means.
 - Lower energy consumption, making it more environmentally friendly.
 - Effective on both low and high-dimensional data.
 - Performs well on real-world and synthetic data.
 - Scales efficiently with increasing data size and number of clusters.
 - Does not rely on distance bounds, avoiding the need to maintain and validate them.
 - Uses geometric principles to focus on the most influential data points, reducing computational overhead.

 ---

 ## Existing Algorithms

 Before the function calls of other algorithms, here is a brief introduction to each one of them. The text within brackets, for example (**Lloyd, 1982**), is a link to the corresponding citation.

 ### Lloyd's k-means ([Lloyd, 1982](https://doi.org/10.1109/TIT.1982.1056489))
 The classic k-means algorithm that serves as the baseline for comparison. It iteratively assigns data points to the nearest centroid and recalculates centroids until convergence. While simple and widely used, it can be slow for large datasets due to numerous distance calculations.

 **Citation:**
 Lloyd S (1982) Least squares quantization in pcm. IEEE Transactions on Information Theory 28(2):129–137. [https://doi.org/10.1109/TIT.1982.1056489](https://doi.org/10.1109/TIT.1982.1056489)

 ### Elkan's Algorithm ([Elkan, 2003](http://www.aaai.org/Papers/ICML/2003/ICML03-022.pdf))
 Focuses on reducing the number of distance calculations required during k-means clustering. The key idea is to use the triangle inequality to avoid unnecessary distance computations. Specifically, it maintains upper and lower bounds on the distances between each data point and each cluster center. Elkan's method is particularly effective for datasets with a moderate number of dimensions and clusters. It provides the exact same results as standard k-means but often with substantially reduced computational cost. While later algorithms have built upon and refined Elkan's approach, it remains a seminal work in the optimization of k-means clustering.

 **Citation:**
 Elkan, C. (2003). Using the triangle inequality to accelerate k-means. In *Proceedings of the 20th International Conference on Machine Learning (ICML-03)* (pp. 147–153).

 ### Hamerly ([Hamerly, 2010](https://www.siam.org/proceedings/datamining/2010/dm10_13_HamerlyG.pdf))
 An improvement on Elkan's algorithm, Hamerly's method uses fewer bounds per data point and tighter bounds that remain valid for longer. It performs well in low-dimensional spaces but can struggle with high-dimensional data.

 **Citation:**
 Hamerly G (2010) Making k-means even faster. In: *Proceedings of the 2010 SIAM international conference on data mining*, SIAM, pp 130–140

 ### Annulus ([Drake, 2013](https://baylor-ir.tdl.org/server/api/core/bitstreams/b6f270e1-66c3-4523-80a9-28b3ae8c10de/content))
 This algorithm utilizes an annular region centered on the origin and the triangle inequality to reduce the number of centroids considered during distance computations. It offers a good balance between speed and accuracy for well-distributed data.

 **Citation:**
 Drake J (2013) *Faster k-means clustering*. MS thesis [https://baylor-ir.tdl.org/server/api/core/bitstreams/b6f270e1-66c3-4523-80a9-28b3ae8c10de/content](https://baylor-ir.tdl.org/server/api/core/bitstreams/b6f270e1-66c3-4523-80a9-28b3ae8c10de/content)

 ### Exponion ([Newling and Fleuret, 2016](http://proceedings.mlr.press/v48/newling16.pdf))
 An extension of Elkan's and Hamerly's ideas, Exponion defines a spherical region centered on cluster centroids and uses tighter bounds to reduce distance calculations. It shows good performance across various datasets.

 **Citation:**
 Newling J, Fleuret F (2016) *Fast k-means with accurate bounds*. In: *Proceedings of the 33rd International Conference on International Conference on Machine Learning - Volume 48.* JMLR.org, ICML’16, p 936–944

 ---

 ### Summary of Existing Methods
 Each of these algorithms represents a significant advancement in k-means clustering, focusing on reducing distance computations and improving overall efficiency. However, **DataCentricKmeans** builds upon these ideas and introduces novel geometric principles to achieve even better performance and energy efficiency.

 ---

 ## Installation

 You can install the package from PyPI:

```bash
 pip install DataCentricKMeans
```

 ---

 ## Usage

 This package allows you to run various k-means algorithms using the provided functions. All functions take similar parameters and return similarly structured results.

 ---

 ### `run_geokmeans` Function

 **Function Definition:**
```python
 def run_geokmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
```

 **Parameters:**

 1. `num_iterations` (int):
    - **Description:** Maximum number of iterations for the algorithm.
    - **Condition:** Must be 1 or greater.

 2. `threshold` (float):
    - **Description:** Convergence threshold for the algorithm.
    - **Condition:** Must be 0 or greater.

 3. `num_clusters` (int):
    - **Description:** The number of clusters.
    - **Condition:** Must be 2 or greater and less than the number of samples in the data.

 4. `seed` (int, optional):
    - **Description:** The seed value for the random number generator. If not provided, the default value of 42 is used.
    - **Condition:** Must be a positive integer.

 5. `file_paths` (list of str):
    - **Description:** The file paths of the data files to be processed.
    - **Condition:** The file paths must be valid and the files must exist.

 **Example Usage:**
```python
 import DataCentricKMeans

 results = DataCentricKMeans.run_geokmeans(
     100,
     0.0001,
     12,
     17,
     [
         "./Breastcancer.csv",
         "./CreditRisk.csv",
         "./census.csv",
         "./birch.csv"
     ]
 )

 # Accessing results
 print(results[0].loop_counter)
 print(results[0].to_dict())
```

 **Outputs:**
 The `run_geokmeans` function returns a list of `KMeansResult` objects, one for each data file. Each `KMeansResult` object contains the following information:

 - `loop_counter` (int): The number of iterations the algorithm ran.
 - `num_dists` (int): The number of distances computed.
 - `assignments` (list of int): The cluster assignment for each data point.
 - `centroids` (list of list of float): The coordinates of each cluster's centroid.
 - `sse` (float): The sum of squared errors (SSE).

 **Accessing the Results:**
```python
 result = results[0]
 print(result.loop_counter)  # Number of iterations
 print(result.to_dict())     # All results as a dictionary
```

 ---

 ### `run_lloyd_kmeans` Function

 **Function Definition:**
```python
 def run_lloyd_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
```

 The `run_lloyd_kmeans` function takes the same parameters as `run_geokmeans` and follows a similar structure. Its usage and outputs are the same.

 **Example Usage:**
```python
 import DataCentricKMeans

 results = DataCentricKMeans.run_lloyd_kmeans(
     100,
     0.0001,
     12,
     17,
     [
         "./Breastcancer.csv",
         "./CreditRisk.csv",
         "./census.csv",
         "./birch.csv"
     ]
 )

 # Accessing results
 print(results[0].loop_counter)
 print(results[0].to_dict())
```

 ---

 ### `run_elkan_kmeans` Function

 **Function Definition:**
```python
 def run_elkan_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
```

 The `run_elkan_kmeans` function takes the same parameters as `run_geokmeans` and follows a similar structure. Its usage and outputs are the same.

 **Example Usage:**
```python
 import DataCentricKMeans

 results = DataCentricKMeans.run_elkan_kmeans(
     100,
     0.0001,
     12,
     17,
     [
         "./Breastcancer.csv",
         "./CreditRisk.csv",
         "./census.csv",
         "./birch.csv"
     ]
 )

 # Accessing results
 print(results[0].loop_counter)
 print(results[0].to_dict())
```

 ---

 ### `run_hamerly_kmeans` Function

 **Function Definition:**
```python
 def run_hamerly_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
```

 The `run_hamerly_kmeans` function takes the same parameters as `run_geokmeans` and follows a similar structure. Its usage and outputs are the same.

 **Example Usage:**
```python
 import DataCentricKMeans

 results = DataCentricKMeans.run_hamerly_kmeans(
     100,
     0.0001,
     12,
     17,
     [
         "./Breastcancer.csv",
         "./CreditRisk.csv",
         "./census.csv",
         "./birch.csv"
     ]
 )

 # Accessing results
 print(results[0].loop_counter)
 print(results[0].to_dict())
```

 ---

 ### `run_annulus_kmeans` Function

 **Function Definition:**
```python
 def run_annulus_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
```

 The `run_annulus_kmeans` function takes the same parameters as `run_geokmeans` and follows a similar structure. Its usage and outputs are the same.

 **Example Usage:**
```python
 import DataCentricKMeans

 results = DataCentricKMeans.run_annulus_kmeans(
     100,
     0.0001,
     12,
     17,
     [
         "./Breastcancer.csv",
         "./CreditRisk.csv",
         "./census.csv",
         "./birch.csv"
     ]
 )

 # Accessing results
 print(results[0].loop_counter)
 print(results[0].to_dict())
```

 ---

 ### `run_exponion_kmeans` Function

 **Function Definition:**
```python
 def run_exponion_kmeans(num_iterations, threshold, num_clusters, seed=None, file_paths=[]):
```

 The `run_exponion_kmeans` function takes the same parameters as `run_geokmeans` and follows a similar structure. Its usage and outputs are the same.

 **Example Usage:**
```python
 import DataCentricKMeans

 results = DataCentricKMeans.run_exponion_kmeans(
     100,
     0.0001,
     12,
     17,
     [
         "./Breastcancer.csv",
         "./CreditRisk.csv",
         "./census.csv",
         "./birch.csv"
     ]
 )

 # Accessing results
 print(results[0].loop_counter)
 print(results[0].to_dict())
```

 ---

 ### Detailed Output Description

 Each `KMeansResult` object contains the following attributes:

 - **`loop_counter`**: Indicates the number of iterations the algorithm ran.
 - **`num_dists`**: The total number of distances computed.
 - **`assignments`**: A list indicating the cluster assignment for each data point.
 - **`centroids`**: A list of lists, where each inner list contains the coordinates of a cluster centroid.
 - **`ballkm_centroids`**: Ball KMeans centroid information in string format.
 - **`timeout`**: A boolean indicating if the algorithm timed out.
 - **`sse`**: The sum of squared errors (SSE).

 ---

 ### Example of Processing Results
```python
 # Get results for the first data file
 result = results[0]

 # Print the number of iterations
 print(f"Loop Counter: {result.loop_counter}")

 # Print the SSE value
 print(f"SSE: {result.sse}")

 # Print all results as a dictionary
 print(result.to_dict())

 # Print centroid information
 for centroid in result.centroids:
     print(centroid)
```

 ---

 ## Summary

 The `DataCentricKMeans` package provides easy-to-use functions for running various k-means algorithms and accessing their results in Python. With its focus on geometric principles and sustainability, **DataCentricKmeans** aims to deliver both high performance and reduced energy consumption—making it an excellent choice for a wide range of clustering tasks.

 ---
 
 ## Authors
 - Vasfi Tataroglu (vtatarog@iu.edu)  
 - Parichit Sharma (parishar@iu.edu)  
 - Hasan Kurban (hasan.kurban@qatar.tamu.edu)  
 - Mehmet M. Dalkilic (dalkilic@iu.edu)

