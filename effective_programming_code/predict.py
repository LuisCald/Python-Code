"""Functions for the predict step of a square root unscented Kalman filter.

The functions use pandas for most of the calculations. This means that for
most operations the order of columns or the index is irrelevant. Nevertheless,
the order might be relevant whenever matrix factorizations are involved!

"""
import numpy as np
import pandas as pd


def square_root_unscented_predict(state, root_cov, params, shock_sds, kappa):
    """Predict *state* in next period and adjust *root_cov*.

    Args:
        state (pd.Series): period t estimate of the unobserved state vector
        root_cov (pd.DataFrame): lower triangular matrix square-root of the
            covariance matrix of the state vector in period t
        params (dict): keys are the names of the states (latent
            factors), values are series with parameters for the transition
            equation of that state.
        shock_sds (pd.Series): standard deviations of the shocks
        kappa (float): scaling parameter for the unscented predict

    Returns:
        predicted_state (pd.Series)
        predicted_root_cov (pd.DataFrame)

    """

    points = _calculate_sigma_points(state, root_cov, kappa)
    weights = _calculate_sigma_weights(state, kappa)
    transformed = _transform_sigma_points(points, params)
    predicted_state = _predict_state(transformed, weights)
    predicted_root_cov = _predict_root_cov(
        transformed,
        weights,
        shock_sds,
        predicted_state,  # DANGEROUS: change order of shock and predict
    )
    return predicted_state, predicted_root_cov


# Nice bug: index size 2N+1.
def _calculate_sigma_points(state, root_cov, kappa):
    """Generate sigma points to be later transformed and used in the
       update state step.

    Args:
        state (pd.Series): period t estimate of the unobserved state vector
        root_cov (pd.DateFrame): lower triangular matrix square-root of the
            covariance matrix of the state vector in period t
        kappa (float): scaling parameter for the unscented predict to see
            how far from the mean we choose our sigma points

    Returns:
        sigma_points (pd.Series)

    """

    n = len(state)
    scale = np.sqrt(n + kappa)
    sigma_points = pd.concat(
        [state.to_frame().T, state + scale * root_cov.T, state - scale * root_cov.T]
    )
    sigma_points.index = range(2 * n + 1)  # added +1
    return sigma_points


# Dangerous Bug: appropriate type of parenthesis in other_weights. (corrected)
def _calculate_sigma_weights(state, kappa):
    """Return a 2N+1 vector of weights to be applied to the sigma points.
        Would be a matrix if there were multiple state dimensions.
        The vector of weights must sum to 1.

    Args:
        state (pd.Series): period t estimate of the unobserved state vector
        kappa (float): scaling parameter for the unscented predict to see
            how far from the mean we choose our sigma points

    Returns:
        sigma_weights (pd.Series)

    """

    n = len(state)
    first_weight = kappa / (n + kappa)
    other_weights = 1 / (2 * (n + kappa))  # DANGEROUS: here is a mistake: 2*(n+kappa)
    weight_list = [first_weight] + [other_weights] * 2 * n
    sigma_weights = pd.Series(data=weight_list, index=range(2 * n + 1))

    return sigma_weights


# Nice bug: wrong type of parenthesis, to_concat is a list .
def _transform_sigma_points(sigma_points, params):
    """Perform unscented transform to sigma points necessary for
       the predict step.

    Args:
        sigma_points (pd.Series): the sample points that will be used in
            the predict state step
        params (dictionary): Contains parameters for Cobb-douglas
            estimation

    Returns:
        out (pd.DataFrame): a 2N+1 x N matrix of transformed sigma_points

    """

    factors = sigma_points.columns
    to_concat = []  # replace () with []
    for factor in factors:
        transformed = _cobb_douglas(sigma_points, **params[factor])
        to_concat.append(transformed.rename(factor))
    out = pd.concat(to_concat, axis=1)
    return out


# Dangerous bug: ** instead of *.
def _cobb_douglas(sigma_points, gammas, a):
    """Transform the sigma points to estimate the distribution.

    Args:
        sigma_points (pd.Series): the sample points that will be used in
            the predict state step
        gammas (pd.Series): the elasticity of the factors in
            the Cobb-Douglas function
        a (float): a constant factor loading

    Returns:
        transformed_sigma_points (pd.Series): a column vector

    """

    return a * (sigma_points ** gammas).product(axis=1)


# Nice bug: Matrix sizes need to fit.
def _predict_state(transformed_sigma_points, sigma_weights):
    """The predict step of the kalman filter.

    Args:
        transformed_sigma_points (pd.DataFrame): sigma points transformed to
            estimate the predicted state distribution
        sigma_weights (pd.Series): weights applied to the sigma points

    Returns:
        the predicted state

    """

    return transformed_sigma_points.T.dot(sigma_weights)


# Dangerous bug: Helper matrix is lower triangular.
# Dangerous bug: Arrangement of arguments.
def _predict_root_cov(
    transformed_sigma_points, sigma_weights, shock_sds, predicted_state
):
    """Predict the square root, lower triangular covariance matrix to construct
        the full covariance matrix in the unit-test.

    Args:
        transformed_sigma_points (pd.DataFrame): sigma points transformed to
            estimate the predicted state distribution
        sigma_weights (pd.Series): weights applied to the sigma points
        shock_sds (pd.Series):
        predicted_state (pd.Series): the new state distribution predicted
            from the transformed sigma points and weights

    Returns:
        predicted_cov (pd.DataFrame): A lower triangular matrix, generated
            to be numerically stable and later used to get the
            actual predicted_cov

    """

    sqrt_weights = sigma_weights.apply(np.sqrt)
    deviations = transformed_sigma_points - predicted_state
    weighted_deviations = deviations.multiply(sqrt_weights, axis=0)
    # Sorting is important here.
    factors = transformed_sigma_points.columns
    shocks_root_cov = pd.DataFrame(
        data=np.diag(shock_sds[factors]), columns=factors, index=factors
    )
    helper_matrix = pd.concat([weighted_deviations, shocks_root_cov])

    predicted_cov = pd.DataFrame(
        data=np.linalg.qr(helper_matrix, mode="r").T, columns=factors, index=factors,
    )
    return predicted_cov

