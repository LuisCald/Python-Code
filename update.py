"""Functions for the update step of a square root unscented Kalman filter.

The functions use pandas for most of the calculations. This means that for
most operations the order of columns or the index is irrelevant. Nevertheless,
the order might be relevant whenever matrix factorizations are involved!

"""
import numpy as np
import pandas as pd


def square_root_linear_update(state, root_cov, measurement, loadings, meas_var):
    """Update *state* and *root_cov with* with a *measurement*.

    Args:
        state (pd.Series): pre-update estimate of the unobserved state vector
        root_cov (pd.DataFrame): lower triangular matrix square-root of the
            covariance matrix of the state vector before the update
        measurement (float): the measurement to incorporate
        loadings (pd.Series): the factor loadings
        meas_var (float): The variance of the incorporated measurement.

    Returns:
        updated_state (pd.Series)
        updated_root_cov (pd.DataFrame)

    """

    residual = _calculate_residual(measurement)
    f = _intermediate_result_f(root_cov, loadings)
    kalman_gain = _calculate_kalman_gain(meas_var, f)
    updated_state = _update_state(state, kalman_gain, residual)
    M = _intermediate_result_M(state, f, root_cov)
    updated_root_cov = _update_root_cov(M)

    return updated_state, updated_root_cov


factors = list("cni")


def _calculate_residual(measurement):
    """ Calculate the residual from the true measurement and *measurement*.

    Args:
        measurement (float): the measurement to incorporate

    Returns:
        residual (float)

    """

    true_measurement = 160
    residual = true_measurement - measurement
    return residual


def _intermediate_result_f(root_cov, loadings):
    """Return f to use in the *_calculate_kalman_gain* function.

    Args:
        root_cov (pd.DataFrame): lower triangular matrix square-root of the
            covariance matrix of the state vector before the update
        loadings (pd.Series): the factor loadings

    Returns:
        f (pd.Series)

    """

    f = root_cov.T.dot(loadings)
    return f


def _calculate_kalman_gain(meas_var, f):
    """Derive kalman gain to scale residual in the update state step.

    Args:
        meas_var (strictly positive float): The variance of the incorporated
                                            measurement
        f (pd.Series): intermediate result

    Returns:
        kalman_gain (pd.Series)

    """

    kalman_gain = 1 / meas_var * f
    return kalman_gain


def _update_state(state, kalman_gain, residual):
    """Update state given the previous measurement, residual and kalman gain.

    Args:
        state (pd.Series): period t estimate of the unobserved state vector
        kalman_gain (pd.Series): a weight placed on the residual based on the
            variance of the measurement
        residual (float): the difference between the true measurement and
            predicted measurement

    Returns:
        kalman_gain (pd.Series)

    """

    updated_state = state + kalman_gain * residual
    return updated_state


def _intermediate_result_M(state, f, root_cov):
    """First derive M, consisting of 4 components:
        the square root of the error variance,
        a zero-vector of length N, where N = how many factors,
        f, the intermediate result derived above and the root_cov.

    Args:
        state (pd.Series): period t estimate of the unobserved state vector
        f (pd.Series): intermediate result
        root_cov (pd.DataFrame): lower triangular matrix square-root of the
            covariance matrix of the state vector before the update

    Returns:
        M (pd.DataFrame): necessary for the QR decomposition step and
        to extract the updated square-root lower triangual covariance matrix

    """

    error_var = 10
    n = len(factors)
    zero_vector = pd.Series(data=[0] * n, index=factors)
    error_var = pd.Series(data=np.sqrt(error_var))
    intermediate_row = pd.concat([error_var, zero_vector], axis=0)
    top_row = pd.DataFrame(intermediate_row).transpose()  # To keep index
    bottom_rows_M = pd.concat([f, root_cov.transpose()], axis=1)
    M = pd.concat([top_row, bottom_rows_M], axis=0)
    return M


def _update_root_cov(M):
    """Uppdate the square root covariance matrix.

    Args:
        M (pd.DataFrame): necessary for the QR decomposition step and
        to extract the updated square-root lower triangual covariance matrix

    Returns:
        updated_root_cov (pd.DataFrame)

    """

    index = [0] + factors
    U = pd.DataFrame(data=np.linalg.qr(M, mode="r"), columns=index, index=index)
    updated_root_cov = pd.DataFrame(
        data=np.array(U)[1:, 1:].T, columns=factors, index=factors
    )
    return updated_root_cov
