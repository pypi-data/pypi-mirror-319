import numpy as np
from . import nettracer
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, as_completed




def get_reslice_indices(args):
    """Internal method used for the secondary algorithm that finds dimensions for subarrays around nodes"""

    indices, dilate_xy, dilate_z, array_shape = args
    try:
        max_indices = np.amax(indices, axis = 0) #Get the max/min of each index.
    except ValueError: #Return Nones if this error is encountered
        return None, None, None
    min_indices = np.amin(indices, axis = 0)

    z_max, y_max, x_max = max_indices[0], max_indices[1], max_indices[2]

    z_min, y_min, x_min = min_indices[0], min_indices[1], min_indices[2]

    y_max = y_max + ((dilate_xy-1)/2) + 1 #Establish dimensions of intended subarray, expanding the max/min indices to include
    y_min = y_min - ((dilate_xy-1)/2) - 1 #the future dilation space (by adding/subtracting half the dilation kernel for each axis)
    x_max = x_max + ((dilate_xy-1)/2) + 1 #an additional index is added in each direction to make sure nothing is discluded.
    x_min = x_min - ((dilate_xy-1)/2) - 1
    z_max = z_max + ((dilate_z-1)/2) + 1
    z_min = z_min - ((dilate_z-1)/2) - 1

    if y_max > (array_shape[1] - 1): #Some if statements to make sure the subarray will not cause an indexerror
        y_max = (array_shape[1] - 1)
    if x_max > (array_shape[2] - 1):
        x_max = (array_shape[2] - 1)
    if z_max > (array_shape[0] - 1):
        z_max = (array_shape[0] - 1)
    if y_min < 0:
        y_min = 0
    if x_min < 0:
        x_min = 0
    if z_min < 0:
        z_min = 0

    y_vals = [y_min, y_max] #Return the subarray dimensions as lists
    x_vals = [x_min, x_max]
    z_vals = [z_min, z_max]

    return z_vals, y_vals, x_vals

def reslice_3d_array(args):
    """Internal method used for the secondary algorithm to reslice subarrays around nodes."""

    input_array, z_range, y_range, x_range = args
    z_start, z_end = z_range
    z_start, z_end = int(z_start), int(z_end)
    y_start, y_end = y_range
    y_start, y_end = int(y_start), int(y_end)
    x_start, x_end = x_range
    x_start, x_end = int(x_start), int(x_end)
    
    # Reslice the array
    resliced_array = input_array[z_start:z_end+1, y_start:y_end+1, x_start:x_end+1]
    
    return resliced_array



def _get_node_node_dict(label_array, label, dilate_xy, dilate_z):
    """Internal method used for the secondary algorithm to find which nodes interact 
    with which other nodes based on proximity."""
    
    # Create a boolean mask where elements with the specified label are True
    binary_array = label_array == label
    binary_array = nettracer.dilate_3D(binary_array, dilate_xy, dilate_xy, dilate_z) #Dilate the label to see where the dilated label overlaps
    label_array = label_array * binary_array  # Filter the labels by the node in question
    label_array = label_array.flatten()  # Convert 3d array to 1d array
    label_array = nettracer.remove_zeros(label_array)  # Remove zeros
    label_array = label_array[label_array != label]
    label_array = set(label_array)  # Remove duplicates
    label_array = list(label_array)  # Back to list
    return label_array

def process_label(args):
    """Internal method used for the secondary algorithm to process a particular node."""
    nodes, label, dilate_xy, dilate_z, array_shape = args
    print(f"Processing node {label}")
    indices = np.argwhere(nodes == label)
    z_vals, y_vals, x_vals = get_reslice_indices((indices, dilate_xy, dilate_z, array_shape))
    if z_vals is None: #If get_reslice_indices ran into a ValueError, nothing is returned.
        return None, None, None
    sub_nodes = reslice_3d_array((nodes, z_vals, y_vals, x_vals))
    return label, sub_nodes


def create_node_dictionary(nodes, num_nodes, dilate_xy, dilate_z):
    """Internal method used for the secondary algorithm to process nodes in parallel."""
    # Initialize the dictionary to be returned
    node_dict = {}

    array_shape = nodes.shape

    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
        # First parallel section to process labels
        # List of arguments for each parallel task
        args_list = [(nodes, i, dilate_xy, dilate_z, array_shape) for i in range(1, num_nodes + 1)]

        # Execute parallel tasks to process labels
        results = executor.map(process_label, args_list)

        # Second parallel section to create dictionary entries
        for label, sub_nodes in results:
            executor.submit(create_dict_entry, node_dict, label, sub_nodes, dilate_xy, dilate_z)

    return node_dict

def create_dict_entry(node_dict, label, sub_nodes, dilate_xy, dilate_z):
    """Internal method used for the secondary algorithm to pass around args in parallel."""

    if label is None:
        pass
    else:
        node_dict[label] = _get_node_node_dict(sub_nodes, label, dilate_xy, dilate_z)

def find_shared_value_pairs(input_dict):
    """Internal method used for the secondary algorithm to look through discrete 
    node-node connections in the various node dictionaries"""
    # List comprehension approach
    return [[key, value, 0] for key, values in input_dict.items() for value in values]
