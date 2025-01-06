# -*- coding: utf-8 -*-
# Copyright 2024 - Michaël Baudin.
"""
Class to define Shi, Xie, Xuan & Nocedal algorithm for the forward formula
"""

import numpy as np
import numericalderivative as nd
import math


class ShiXieXuanNocedalForward:
    r"""
    Compute an approximately optimal step for the forward F.D. formula of the first derivative

    Uses forward finite difference to compute an approximate value of f'(x):

    .. math::

        f'(x) \approx \frac{f(x + h) - f(x)}{h}

    where :math:`f` is the function, :math:`x \in \mathbb{R}` is the point
    and :math:`h > 0` is the differentiation step.
    If :math:`f''(x) \neq 0`, then the step which minimizes the total error is
    (see (Shi, Xie, Xuan & Nocedal, 2022) eq. 2.2 page 4):

    .. math::

        h^\star = 2 \sqrt{\frac{\epsilon_f}{\left|f''(x)\right|}}

    where :math:`\epsilon_f > 0` is the absolute error of the function evaluation.
    If the order of magnitude of the second derivative can be guessed,
    then :meth:`~numericalderivative.FirstDerivativeForward.compute_step` can be used.
    Alternatively, the goal of :class:`~numericalderivative.ShiXieXuanNocedalForward`
    is to compute :math:`h^\star` using
    function evaluations only and without estimating :math:`f''(x)`.

    The algorithm considers the test ratio
    (see (Shi, Xie, Xuan & Nocedal, 2022) eq. 2.3 page 4):

    .. math::

        r(h) = \frac{\left|f(x + 4h) - 4f(x + h) + 3f(x)\right|}{8 \epsilon_f}

    where :math:`h > 0` is the step and :math:`\epsilon_f> 0` is the absolute precision of evaluation
    of the function.
    The goal of the algorithm is to find the step such that
    (see (Shi, Xie, Xuan & Nocedal, 2022) eq. 2.4 page 4):

    .. math::

        r_\ell \leq r(h) \leq r_u

    where :math:`r_\ell > 0` is the lower bound of the test ratio
    and :math:`r_u` is the upper bound.
    The algorithm is based on bisection.

    If the algorithm succeeds, the method produces a step
    :math:`\widetilde{h}` such that:

    .. math::

        \widetilde{h} \in \frac{1}{\sqrt{3}} \left[\sqrt{r_\ell - 1}, \sqrt{r_u + 1}\right] h^\star.

    With :math:`r_\ell = 1.5` and :math:`r_u = 6`, the previous interval is:

    .. math::

        \widetilde{h} \in \left[0.41, 1.5\right] h^\star.

    This method can fail if the value of the second derivative of the function
    is equal to zero.
    In this case, the test ratio is zero and there is no value of the
    step :math:`h` which satisfies the required inequalities.
    For example, the function :math:`f(x) = \sin(x)` for any
    real number :math:`x` has a zero derivative at the point :math:`x = \pm \pi`.
    This algorithm will fail to compute a suitable step in this case.

    The method can fail if the absolute precision of the function value
    is set to zero.
    This can happen if the user computes it depending on the relative precision
    and the absolute value of the function: if the value of the function
    at point :math:`x` is zero, then the absolute precision is zero.
    For example, the function :math:`f(x) = x^2` for any
    real number :math:`x` has a zero value at the point :math:`x = 0`.

    Parameters
    ----------
    function : function
        The function to differentiate.
    x : float
        The point where the derivative is to be evaluated.
    absolute_precision : float, > 0, optional
        The absolute precision of evaluation of f.
        If the function value is close to zero (e.g. for the sin function
        at x = np.pi where f(x) is close to 1.0e-32), then the absolute
        precision cannot always be computed from the relative precision.
    minimum_test_ratio : float, > 1
        The minimum value of the test ratio.
    maximum_test_ratio : float, > minimum_test_ratio
        The maximum value of the test ratio.
    args : list
        A list of optional arguments that the function takes as inputs.
        By default, there is no extra argument and calling sequence of
        the function must be y = function(x).
        If there are extra arguments, then the calling sequence of
        the function must be y = function(x, arg1, arg2, ...) where
        arg1, arg2, ..., are the items in the args list.
    verbose : bool, optional
        Set to True to print intermediate messages.

    Returns
    -------
    None.

    References
    ----------
    - Shi, H. J. M., Xie, Y., Xuan, M. Q., & Nocedal, J. (2022). Adaptive finite-difference interval estimation for noisy derivative-free optimization. SIAM Journal on Scientific Computing, 44 (4), A2302-A2321.

    See also
    --------
    FirstDerivativeForward

    Examples
    --------
    Compute the step of a badly scaled function.

    >>> import numericalderivative as nd
    >>>
    >>> def scaled_exp(x):
    >>>     alpha = 1.e6
    >>>     return np.exp(-x / alpha)
    >>>
    >>> x = 1.0e-2
    >>> algorithm = nd.ShiXieXuanNocedalForward(
    >>>     scaled_exp, x,
    >>> )
    >>> h_optimal, number_of_iterations = algorithm.find_step()
    >>> f_prime_approx = algorithm.compute_first_derivative(h_optimal)

    Set the initial step.

    >>> initial_step = 1.0e8
    >>> h_optimal, number_of_iterations = algorithm.find_step(initial_step)
    """

    def __init__(
        self,
        function,
        x,
        absolute_precision=1.0e-15,
        minimum_test_ratio=1.5,
        maximum_test_ratio=6.0,
        args=None,
        verbose=False,
    ):
        if absolute_precision <= 0.0:
            raise ValueError(
                f"The absolute precision must be > 0. "
                f"here absolute precision = {absolute_precision}"
            )
        self.absolute_precision = absolute_precision
        self.verbose = verbose
        self.first_derivative_forward = nd.FirstDerivativeForward(function, x, args)
        self.function = nd.FunctionWithArguments(function, args)
        self.x = x
        self.step_history = []
        if minimum_test_ratio <= 1.0:
            raise ValueError(
                f"The minimum test ratio must be > 1, "
                f"but minimum_test_ratio = {minimum_test_ratio}"
            )
        if maximum_test_ratio <= minimum_test_ratio:
            raise ValueError(
                f"The maximum test ratio must be greater than the minimum, "
                f"but minimum_test_ratio = {minimum_test_ratio} "
                f" and maximum_test_ratio = {maximum_test_ratio}"
            )
        self.minimum_test_ratio = minimum_test_ratio
        self.maximum_test_ratio = maximum_test_ratio
        return

    def get_ratio_min_max(self):
        r"""
        Return the minimum and maximum of the test ratio

        Returns
        -------
        minimum_test_ratio : float, > 0
            The lower bound of the test ratio.
        maximum_test_ratio : float, > 0
            The upper bound of the test ratio.
        """
        return [self.minimum_test_ratio, self.maximum_test_ratio]

    def compute_test_ratio(self, step, function_values=None):
        r"""
        Compute the test ratio

        Parameters
        ----------
        step : float, > 0
            The finite difference step
        function_values : list(3 floats)
            The function values f(x), f(x + h), f(x + 4h).
            If function_values is None, then compute the funtion
            values.

        Returns
        -------
        test_ratio : float, > 0
            The test ratio
        """
        if function_values is None:
            f0 = self.function(self.x)
            f1 = self.function(self.x + step)
            f4 = self.function(self.x + 4.0 * step)
            function_values = [f0, f1, f4]

        f0, f1, f4 = function_values
        test_ratio = abs(f4 - 4 * f1 + 3 * f0) / (8 * self.absolute_precision)
        return test_ratio

    def find_step(
        self,
        initial_step=None,
        iteration_maximum=53,
        logscale=True,
    ):
        r"""
        Compute an approximate optimum step for forward F.D. formula

        If it is not provided by the user, the default initial step is based
        on the hypothesis that the second derivative is equal to 1 and is
        computed from :meth:`~numericalderivative.FirstDerivativeForward.compute_step`.
        This is slightly different from the one suggested in (Shi, Xie, Xuan & Nocedal, 2022)
        which involves a :math:`\sqrt{3}`.
        This initial guess is not always accurate and can lead to failure
        of the algorithm.

        Parameters
        ----------
        initial_step : float, > 0
            The initial step in the algorithm.
        iteration_maximum : int, optional
            The number of number_of_iterations.
        logscale : bool, optional
            Set to True to use a logarithmic scale when updating the step k
            during the search. Set to False to use a linear scale when
            updating the step k during the search.

        Returns
        -------
        estim_step : float
            A step size which is near to optimal.
        number_of_iterations : int
            The number of iterations required to reach that optimum.

        """
        if iteration_maximum < 1:
            raise ValueError(
                f"The maximum number of iterations must be > 1, "
                f"but iteration_maximum = {iteration_maximum}"
            )
        fractional_part, _ = math.modf(iteration_maximum)
        if fractional_part != 0.0:
            raise ValueError(
                f"The maximum number of iterations must be an integer, "
                f"but its fractional part is {fractional_part}"
            )

        if initial_step is None:
            second_derivative_value = 1.0
            estim_step = nd.FirstDerivativeForward.compute_step(
                second_derivative_value, self.absolute_precision
            )
        if initial_step < 0.0:
            raise ValueError(
                f"The initial step must be > 0, "
                f"but initial_step = {initial_step:.3e}"
            )
        estim_step = initial_step
        # Compute function value
        f0 = self.function(self.x)
        f1 = self.function(self.x + estim_step)
        f4 = self.function(self.x + 4.0 * estim_step)
        if self.verbose:
            print(f"x = {self.x}")
            print(f"f(x) = {f0}")
            print(f"f(x + h) = {f1}")
            print(f"f(x + 4 * h) = {f4}")
            print(f"absolute_precision = {self.absolute_precision:.3e}")
            print(f"estim_step={estim_step:.3e}")
        lower_bound = 0.0
        upper_bound = np.inf
        self.step_history = []
        found = False
        for number_of_iterations in range(iteration_maximum):
            """
            # Check that the upper bound of the step is not too small
            # This would prevent the magic trick to be used, indicating
            # that the problem is inconsistent with the method.
            actual_step = (self.x + estim_step) - self.x  # Magic trick
            if actual_step == 0.0:
                raise ValueError(f"The actual step is zero at x = {self.x}. "
                                 f"The method cannot be used for this problem.")
            """
            # Update history
            self.step_history.append(estim_step)
            test_ratio = self.compute_test_ratio(estim_step, [f0, f1, f4])
            if self.verbose:
                print(
                    f"+ Iter.={number_of_iterations}, "
                    f"lower_bound={lower_bound:.3e}, "
                    f"upper_bound={upper_bound:.3e}, "
                    f"estim_step={estim_step:.3e}, "
                    f"r = {test_ratio:.3e}"
                )
            if test_ratio < self.minimum_test_ratio:
                if self.verbose:
                    print(
                        "    - test_ratio < self.minimum_test_ratio. "
                        "Set lower bound to h."
                    )
                lower_bound = estim_step
            elif test_ratio > self.maximum_test_ratio:
                if self.verbose:
                    print(
                        "    - test_ratio > self.minimum_test_ratio. "
                        "Set upper bound to h."
                    )
                upper_bound = estim_step
            else:
                if self.verbose:
                    print(f"    - Step = {estim_step} is OK: stop.")
                found = True
                break
            if upper_bound == np.inf:
                if self.verbose:
                    print("    - upper_bound == np.inf: increase h.")
                estim_step *= 4.0
                f1 = f4
                f4 = self.function(self.x + 4.0 * estim_step)
            elif lower_bound == 0.0:
                if self.verbose:
                    print("    - lower_bound == 0: decrease h.")
                estim_step /= 4.0
                f4 = f1
                f1 = self.function(self.x + estim_step)
            else:
                if logscale:
                    log_step = (np.log(lower_bound) + np.log(upper_bound)) / 2.0
                    estim_step = np.exp(log_step)
                else:
                    estim_step = (lower_bound + upper_bound) / 2.0
                if self.verbose:
                    print(f"    - Bisection: estim_step = {estim_step:.3e}.")
                f1 = self.function(self.x + estim_step)
                f4 = self.function(self.x + 4 * estim_step)

        if not found:
            raise ValueError(
                f"Unable to find satisfactory step_second_derivative "
                f"after {iteration_maximum} iterations. "
                f"Please increase iteration_maximum = {iteration_maximum}."
            )
        return estim_step, number_of_iterations

    def compute_first_derivative(self, step):
        """
        Compute an approximate value of f'(x) using central finite difference.

        Parameters
        ----------
        step : float, > 0
            The step size.

        Returns
        -------
        f_prime_approx : float
            The approximation of f'(x).
        """
        f_prime_approx = self.first_derivative_forward.compute(step)
        return f_prime_approx

    def get_number_of_function_evaluations(self):
        """
        Returns the number of function evaluations.

        Returns
        -------
        number_of_function_evaluations : int
            The number of function evaluations.
        """
        finite_difference_feval = (
            self.first_derivative_forward.get_function().get_number_of_evaluations()
        )
        function_eval = self.function.get_number_of_evaluations()
        total_feval = finite_difference_feval + function_eval
        return total_feval

    def get_step_history(self):
        """
        Return the history of steps during the bissection search.

        Returns
        -------
        step_history : list(float)
            The list of steps k during intermediate iterations of the bissection search.
            This is updated by :meth:`find_step`.

        """
        return self.step_history

    def get_absolute_precision(self):
        """
        Return the absolute precision of the function evaluation

        Returns
        -------
        absolute_precision : float
            The absolute precision of evaluation of f.

        """
        return self.absolute_precision
