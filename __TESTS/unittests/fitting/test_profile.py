# coding: utf8
# Copyright 2019 CERN. This software is distributed under the
# terms of the GNU General Public Licence version 3 (GPL Version 3),
# copied verbatim in the file LICENCE.md.
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.
# Project website: http://blond.web.cern.ch/

"""
Unit-test for the blond_common.fitting.profile module

- TODO: include the changes from interfaces.beam.analytic_distribution

:Authors: **Alexandre Lasheen**

"""

# General imports
# ---------------
import sys
import unittest
import numpy as np
import os

this_directory = os.path.dirname(os.path.realpath(__file__)) + "/"

# BLonD_Common imports
# --------------------
if os.path.abspath(this_directory + '../../../../') not in sys.path:
    sys.path.insert(0, os.path.abspath(this_directory + '../../../../'))

from blond_common.interfaces.beam.analytic_distribution import (
    Gaussian, parabolicAmplitude, binomialAmplitudeN, _binomial_full_to_rms,
    _binomial_full_to_fwhm)
from blond_common.fitting.profile import RMS, FWHM


class TestFittingProfile(unittest.TestCase):

    # Initialization ----------------------------------------------------------

    def setUp(self):
        '''
        We generate three different distributions, Gaussian, Parabolic
        Amplitude, and Binomial that will be used to test the fitting functions
        '''

        self.time_array = np.arange(0, 25e-9, 0.1e-9)

        self.amplitude_gauss = 1.
        self.position_gauss = 13e-9
        self.length_gauss = 2e-9
        self.initial_params_gauss = [self.amplitude_gauss, self.position_gauss,
                                     self.length_gauss]
        self.gaussian_dist = Gaussian(*self.initial_params_gauss).profile(
            self.time_array)
        self.sigma_gauss = self.length_gauss
        self.fwhm_gauss = Gaussian(*self.initial_params_gauss).FWHM

        self.amplitude_parabamp = 1.3
        self.position_parabamp = 4e-9
        self.length_parabamp = 5e-9
        self.initial_params_parabamp = [self.amplitude_parabamp,
                                        self.position_parabamp,
                                        self.length_parabamp]
        self.parabamp_dist = parabolicAmplitude(self.time_array,
                                                *self.initial_params_parabamp)
        self.sigma_parabamp = _binomial_full_to_rms(self.length_parabamp, 1.5)
        self.fwhm_parabamp = _binomial_full_to_fwhm(self.length_parabamp, 1.5)

        self.amplitude_binom = 0.77
        self.position_binom = 18.3e-9
        self.length_binom = 3.45e-9
        self.exponent_binom = 3.4
        self.initial_params_binom = [self.amplitude_binom, self.position_binom,
                                     self.length_binom, self.exponent_binom]
        self.binom_dist = binomialAmplitudeN(self.time_array,
                                             *self.initial_params_binom)
        self.sigma_binom = _binomial_full_to_rms(self.length_binom,
                                                 self.exponent_binom)
        self.fwhm_binom = _binomial_full_to_fwhm(self.length_binom,
                                                 self.exponent_binom)

    # Tests for RMS -----------------------------------------------------------
    '''
    Testing the RMS function on the three profiles, the absolute precision
    required was set manually for the time being.

    The test consists of 6 assertions comparing the mean and rms obtained
    from the RMS function compared to the analytical expectation for the
    3 profiles.

    TODO: the precision is set manually atm and should be reviewed

    '''

    def test_RMS_gauss(self):
        '''
        Checking the mean,rms obtained from RMS function for the Gaussian
        profile
        '''

        mean_gauss, rms_gauss = RMS(self.time_array, self.gaussian_dist)

        np.testing.assert_almost_equal(
            mean_gauss*1e9, self.position_gauss*1e9, decimal=8)

        np.testing.assert_almost_equal(
            rms_gauss*1e9, self.length_gauss*1e9, decimal=7)

    def test_RMS_parabamp(self):
        '''
        Checking the mean,rms obtained from RMS function for the Parabolic
        Amplitude profile
        '''

        mean_parabamp, rms_parabamp = RMS(self.time_array, self.parabamp_dist)

        np.testing.assert_almost_equal(
            mean_parabamp*1e9, self.position_parabamp*1e9, decimal=8)

        np.testing.assert_almost_equal(
            rms_parabamp*1e9, self.sigma_parabamp*1e9, decimal=4)

    def test_RMS_binom(self):
        '''
        Checking the mean,rms obtained from RMS function for a Binomial profile
        '''

        mean_binom, rms_binom = RMS(self.time_array, self.binom_dist)

        np.testing.assert_almost_equal(
            mean_binom*1e9, self.position_binom*1e9, decimal=8)

        np.testing.assert_almost_equal(
            rms_binom*1e9, self.sigma_binom*1e9, decimal=6)

    # Tests for FWHM ----------------------------------------------------------
    '''
    Testing the FWHM function on the three profiles, the absolute precision
    required was set manually for the time being.

    The test consists of 6 assertions comparing the center and fwhm obtained
    from the FWHM function compared to the the analytical expectation for the
    3 profiles.

    TODO: the precision is set manually atm and should be reviewed

    '''

    def test_FWHM_gauss(self):
        '''
        Checking the center,fwhm obtained from FWHM function for the Gaussian
        profile.
        '''

        center_gauss, fwhm_gauss = FWHM(self.time_array, self.gaussian_dist)

        np.testing.assert_almost_equal(
            center_gauss*1e9, self.position_gauss*1e9, decimal=8)

        np.testing.assert_almost_equal(
            fwhm_gauss*1e9, self.fwhm_gauss*1e9, decimal=3)

    def test_FWHM_parabamp(self):
        '''
        Checking the center,fwhm obtained from FWHM function for the Parabolic
        Amplitude profile.
        '''

        center_parabamp, fwhm_parabamp = FWHM(self.time_array,
                                              self.parabamp_dist)

        np.testing.assert_almost_equal(
            center_parabamp*1e9, self.position_parabamp*1e9, decimal=8)

        np.testing.assert_almost_equal(
            fwhm_parabamp*1e9, self.fwhm_parabamp*1e9, decimal=3)

    def test_FWHM_binom(self):
        '''
        Checking the center,fwhm obtained from FWHM function for a Binomial
        profile.
        '''

        center_binom, fwhm_binom = FWHM(self.time_array, self.binom_dist)

        np.testing.assert_almost_equal(
            center_binom*1e9, self.position_binom*1e9, decimal=8)

        np.testing.assert_almost_equal(
            fwhm_binom*1e9, self.fwhm_binom*1e9, decimal=3)


if __name__ == '__main__':

    unittest.main()
