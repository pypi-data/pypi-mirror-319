import numpy as np
from scipy.stats import norm
from scipy.stats import zscore
from scipy.special import softmax
import numpy as np
from scipy.stats import gaussian_kde, dirichlet

def weighted_sampling_cpd(weights, variable_card, parents_card):
    """
    Perform weighted sampling based on the probability distribution of the weights.
    Arguments:
    - weights: Array of weight values (treated as probabilities).
    - variable_card: Cardinality of the variable to which the CPD corresponds.
    - parents_card: Cardinalities of the parent variables.
    
    Returns:
    - A conditional probability distribution matrix.
    """
    total_parent_states = np.prod(parents_card) if parents_card else 1
    desired_shape = (variable_card, total_parent_states)
    weights_normalized = weights / np.sum(weights)
    sample_indices = np.random.choice(
        len(weights), size=np.prod(desired_shape), p=weights_normalized, replace=True
    )
    sampled_weights = weights[sample_indices].reshape(desired_shape)
    cpd = sampled_weights / sampled_weights.sum(axis=0, keepdims=True)
    return cpd

def stratified_sampling_cpd(weights, variable_card, parents_card, num_bins=10):
    """
    Perform stratified sampling by dividing weights into strata (bins).
    Arguments:
    - weights: Array of weight values.
    - variable_card: Cardinality of the variable to which the CPD corresponds.
    - parents_card: Cardinalities of the parent variables.
    - num_bins: Number of bins to divide the weight space into.
    
    Returns:
    - A conditional probability distribution matrix.
    """
    total_parent_states = np.prod(parents_card) if parents_card else 1
    desired_shape = (variable_card, total_parent_states)
    bins = np.linspace(min(weights), max(weights), num=num_bins + 1)
    strata_indices = np.digitize(weights, bins) - 1
    sampled_weights = []
    
    for i in range(num_bins):
        stratum_weights = weights[strata_indices == i]
        if len(stratum_weights) > 0:
            sampled = np.random.choice(
                stratum_weights, size=len(stratum_weights), replace=True
            )
            sampled_weights.extend(sampled)
    
    sampled_weights = np.array(sampled_weights[:np.prod(desired_shape)])
    cpd = sampled_weights.reshape(desired_shape)
    cpd /= cpd.sum(axis=0, keepdims=True)
    return cpd

def kde_based_sampling_cpd(weights, variable_card, parents_card, bandwidth=0.2):
    """
    Perform sampling using a kernel density estimate (KDE) of the weights.
    Arguments:
    - weights: Array of weight values.
    - variable_card: Cardinality of the variable to which the CPD corresponds.
    - parents_card: Cardinalities of the parent variables.
    - bandwidth: Bandwidth parameter for the KDE (affects smoothness).
    
    Returns:
    - A conditional probability distribution matrix.
    """
    total_parent_states = np.prod(parents_card) if parents_card else 1
    desired_shape = (variable_card, total_parent_states)
    kde = gaussian_kde(weights, bw_method=bandwidth)
    sampled_weights = kde.resample(size=np.prod(desired_shape)).flatten()
    sampled_weights = np.abs(sampled_weights)  # Ensure non-negative
    cpd = sampled_weights.reshape(desired_shape)
    cpd /= cpd.sum(axis=0, keepdims=True)
    return cpd

def bayesian_dirichlet_cpd(weights, variable_card, parents_card, prior=1.0):
    """
    Perform Bayesian sampling using a Dirichlet distribution.
    Arguments:
    - weights: Array of weight values.
    - variable_card: Cardinality of the variable to which the CPD corresponds.
    - parents_card: Cardinalities of the parent variables.
    - prior: Scalar or array to adjust the prior counts (higher values enforce stronger priors).
    
    Returns:
    - A conditional probability distribution matrix.
    """
    total_parent_states = np.prod(parents_card) if parents_card else 1
    desired_shape = (variable_card, total_parent_states)
    alpha = weights * prior + 1e-5
    sampled_weights = []
    for _ in range(total_parent_states):
        sampled_weights.append(dirichlet(alpha).rvs(size=1).flatten())
    cpd = np.vstack(sampled_weights).T
    return cpd

def execute_sampling_method(weights, variable_card, parents_card, method, **kwargs):
    """
    Executes the specified sampling method based on user input with error handling.
    Arguments:
    - weights: Array of weight values.
    - variable_card: Cardinality of the variable to which the CPD corresponds.
    - parents_card: Cardinalities of the parent variables.
    - method: Identifier for the sampling method. Accepted formats:
        * '1', '2', '3', '4'
        * Full method names ('weighted', 'stratified', 'kde', 'bayesian')
        * First letters ('w', 's', 'k', 'b')
    - kwargs: Additional parameters for specific methods (optional).
    
    Returns:
    - A conditional probability distribution matrix or an error message.
    """
    method_mapping = {
        "1": "weighted",
        "2": "stratified",
        "3": "kde",
        "4": "bayesian",
        "w": "weighted",
        "s": "stratified",
        "k": "kde",
        "b": "bayesian",
        "weighted": "weighted",
        "stratified": "stratified",
        "kde": "kde",
        "bayesian": "bayesian",
    }

    if isinstance(method, str):
        method = method.lower().strip()
    
    if isinstance(method, int):
        method_key = str(method)
    
    method_key = method_mapping.get(method)
    
    if not method_key:
        method_key = "stratified"  # Default to stratified sampling
        print(
            f"Invalid method '{method}'. Defaulting to 'stratified' (method '2'). Choose from: "
            f"1, 2, 3, 4, 'weighted', 'stratified', 'kde', or 'bayesian'."
        )

    
    sampling_methods = {
        "weighted": weighted_sampling_cpd,
        "stratified": stratified_sampling_cpd,
        "kde": kde_based_sampling_cpd,
        "bayesian": bayesian_dirichlet_cpd
    }
    
    selected_method = sampling_methods[method_key]
    try:
        return selected_method(weights, variable_card, parents_card, **kwargs)
    except TypeError as e:
        raise ValueError(
            f"Error calling '{method_key}' method. Check the additional parameters: {e}"
        )

def remove_outliers(data, method='iqr', threshold=3):
    """
    Remove outliers from a dataset using either the z-score or IQR method.
    
    Args:
    - data (np.array): The input data from which to remove outliers.
    - method (str): Method to use for outlier detection ('z-score' or 'iqr').
    - threshold (float): The threshold value for the z-score or multiplier for the IQR.
    
    Returns:
    - non_outliers (np.array): The data with outliers removed.
    - outliers (np.array): The data points identified as outliers.
    """
    if method not in ['z-score', 'iqr']:
        raise ValueError("Method must be either 'z-score' or 'iqr'.")

    if method == 'z-score':
        zs = zscore(data)
        is_outlier = np.abs(zs) > threshold
    else:  # method == 'iqr'
        Q1, Q3 = np.percentile(data, [25, 75])
        IQR = Q3 - Q1
        lower_bound = Q1 - (IQR * threshold)
        upper_bound = Q3 + (IQR * threshold)
        is_outlier = (data < lower_bound) | (data > upper_bound)
    
    non_outliers = data[~is_outlier]
    outliers = data[is_outlier]

    return non_outliers, outliers

def minmax_process_model_weights(model):
    """
    Process the weights of a trained deep learning model.

    Parameters:
    - model: The trained deep learning model.

    Returns:
    - processed_weights: The processed weights suitable for CPD creation.
    """
    raw_weights = np.concatenate([array.flatten() for array in model.get_weights()])

    # Normalize weights to range [0, 1]
    min_weight = raw_weights.min()
    max_weight = raw_weights.max()
    processed_weights = (raw_weights - min_weight) / (max_weight - min_weight)

    return processed_weights

def softmax(x):
    """Compute softmax values for each set of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def softmax_process_model_weights(model):
    """
    Process the weights of a trained deep learning model using softmax normalization.

    Parameters:
    - model: The trained deep learning model.

    Returns:
    - processed_weights: The softmax-normalized weights suitable for CPD creation.
    """
    # Concatenate all model weights into a single 1D array
    raw_weights = np.concatenate([array.flatten() for array in model.get_weights()])
    
    # Apply softmax to normalize weights
    processed_weights = softmax(raw_weights)

    return raw_weights

def flatten_weights(model):
    """
    Process weights and flatten them into a 1D array.

    Parameters:
    - model: The trained deep learning model.

    Returns:
    - flat_weights: 1D array of flattened weights.
    """
    # Concatenate all model weights into a single 1D array
    flat_weights = np.concatenate([array.flatten() for array in model.get_weights()])
    
    return flat_weights
