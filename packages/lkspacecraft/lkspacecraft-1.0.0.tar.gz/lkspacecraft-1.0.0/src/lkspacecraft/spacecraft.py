"""Classes for working with the orbits of spacecraft"""

from typing import Union

import astropy.units as u
import numpy as np
import numpy.typing as npt
import spiceypy
from astropy.constants import c
from astropy.time import Time
from astropy.utils.data import cache_contents


class BadEphemeris(Exception):
    def __init__(self, message):
        super().__init__(message)


class Spacecraft(object):
    """
    A base class for handling spacecraft ephemeris data and calculations.

    This class provides methods to retrieve spacecraft position, velocity, light travel time,
    and related calculations using SPICE kernels. It supports transformations between
    time formats and computes barycentric time corrections and velocity aberration effects.

    Attributes
    ----------
    start_time : astropy.time.Time
        The start time of the loaded SPICE kernel data.
    end_time : astropy.time.Time
        The end time of the loaded SPICE kernel data.

    Methods
    -------
    get_spacecraft_position(time, observer="SOLAR SYSTEM BARYCENTER")
        Returns the position vector (x, y, z) in kilometers relative to the specified observer.
    get_spacecraft_velocity(time, observer="SOLAR SYSTEM BARYCENTER")
        Returns the velocity vector (vx, vy, vz) in kilometers per second relative to the observer.
    get_spacecraft_light_travel_time(time, observer="SOLAR SYSTEM BARYCENTER")
        Computes the one-way light travel time to the observer in seconds.
    get_barycentric_time_correction(time, ra, dec)
        Calculates the barycentric time correction for a target specified by RA and Dec.
    get_velocity_aberrated_positions(time, ra, dec)
        Computes the RA and Dec of a target after applying velocity aberration.
    """

    def __init__(self):
        """
        Initializes the Spacecraft object and loads SPICE kernels.

        This method clears any previously loaded SPICE kernels, loads the kernels specified
        in the `Meta.txt` file, and determines the start and end times of the kernel data.

        Raises
        ------
        Exception
            If there is an issue loading the SPICE kernels or retrieving the kernel time coverage.
        """
        meta_kernel = cache_contents(pkgname="lkspacecraft")[
            "https://github.com/lightkurve/lkspacecraft/src/lkspacecraft/data/Meta.txt"
        ]
        spiceypy.kclear()
        spiceypy.furnsh(meta_kernel)
        self.start_time, self.end_time = self._get_kernel_start_and_end_times()

    def _get_kernel_start_and_end_times(self):
        # Get a list of loaded kernels
        kernel_list = spiceypy.ktotal("ALL")  # Get the count of all loaded kernels
        start_et = float("inf")
        end_et = float("-inf")

        for i in range(kernel_list):
            kernel_name = spiceypy.kdata(i, "ALL")[0]

            # Check if the kernel is SPK or CK to calculate coverage
            kernel_type = spiceypy.kdata(i, "ALL")[1]

            if kernel_type in ["SPK", "CK"]:
                # Create a window for coverage
                coverage_window = spiceypy.stypes.SPICEDOUBLE_CELL(2**10)

                # Query coverage for the specific kernel
                try:
                    if kernel_type == "SPK":
                        spiceypy.spkcov(
                            kernel_name, self.spacecraft_code, coverage_window
                        )  # Replace with your NAIF ID
                    else:
                        continue

                    # Extract start and end times for the current kernel
                    interval_start = spiceypy.wnfetd(coverage_window, 0)[0]
                    interval_end = spiceypy.wnfetd(coverage_window, 0)[1]

                    # Update the global start and end times
                    start_et = min(start_et, interval_start)
                    end_et = max(end_et, interval_end)
                except Exception:
                    continue
        start_time = Time(spiceypy.et2datetime(start_et))
        end_time = Time(spiceypy.et2datetime(end_et))
        return start_time, end_time

    def __repr__(self):
        return "KeplerSpacecraft"

    def _process_time(self, time: Time):
        # convert to astropy.time.Time if needed
        if not isinstance(time, Time):
            try:
                time = Time(time, format="jd")
            except ValueError:
                try:
                    time = Time(time)
                except Exception:
                    raise ValueError(
                        "Can not parse input time. Pass an `astropy.time.Time` object."
                    )
        if time.ndim == 0:
            time = Time([time])
        return time

    def _get_state_vector(self, time: Time, observer="SOLAR SYSTEM BARYCENTER"):
        time = self._process_time(time)
        et = spiceypy.str2et(time.isot)
        try:
            state, light_travel_time = spiceypy.spkezr(
                f"{self.spacecraft_code}",
                et,
                "J2000",
                "NONE",
                observer,
            )
        except spiceypy.SpiceSPKINSUFFDATA:
            raise BadEphemeris(
                "The time you have requested is outside of the time range where data exists for this spacecraft."
            )
        return np.asarray(state), np.asarray(light_travel_time)

    def get_spacecraft_position(
        self, time: Time, observer="SOLAR SYSTEM BARYCENTER"
    ) -> npt.NDArray:
        """Returns the position vector (x, y, z) in [km] for all `time` w.r.t the observer.

        Parameters:
        -----------
        time: astropy.time.Time
            Time array at which to estimate position. Time must be in UTC.
        observer: string
            Observer body. Common options include "SOLAR SYSTEM BARYCENTER", "EARTH BARYCENTER", "MOON BARYCENTER"
        """
        return self._get_state_vector(time=time, observer=observer)[0][:, :3]

    def get_spacecraft_velocity(
        self, time: Time, observer="SOLAR SYSTEM BARYCENTER"
    ) -> npt.NDArray:
        """Returns the position vector (vx, vy, vz) in [km/s] for all `time` w.r.t the observer.

        Parameters:
        -----------
        time: astropy.time.Time
            Time array at which to estimate velocity. Time must be in UTC.
        observer: string
            Observer body. Common options include "SOLAR SYSTEM BARYCENTER", "EARTH BARYCENTER", "MOON BARYCENTER"
        """
        return self._get_state_vector(time=time, observer=observer)[0][:, 3:]

    def get_spacecraft_light_travel_time(
        self, time: Time, observer="SOLAR SYSTEM BARYCENTER"
    ) -> npt.NDArray:
        """Returns the one-way light travel time in seconds for all `time` w.r.t the observer.

        Parameters:
        -----------
        time: astropy.time.Time
            Time array at which to estimate position. Time must be in UTC.
        observer: string
            Observer body. Common options include "SOLAR SYSTEM BARYCENTER", "EARTH BARYCENTER", "MOON BARYCENTER"
        """
        return self._get_state_vector(time=time, observer=observer)[1] / 2

    def get_barycentric_time_correction(
        self, time: Time, ra: Union[float, npt.NDArray], dec: Union[float, npt.NDArray]
    ) -> npt.NDArray:
        """Returns the barycentric time correction in days for observations of a particular target specified by RA and Dec.

        Note that `time` here must be time in spacecraft time, in UTC format.
        This means that for SPOC data this should be the time without the SPOC barycentric correction applied.

        Parameters:
        -----------
        time: astropy.time.Time
            Time array at which to estimate position. Time must be in UTC.
        ra: float, np.ndarray
            The right ascention of the target in degrees
        dec: float, np.ndarray
            The declination of the target in degrees
        """

        star_vector = np.array(
            [
                np.cos(np.deg2rad(dec)) * np.cos(np.deg2rad(ra)),
                np.cos(np.deg2rad(dec)) * np.sin(np.deg2rad(ra)),
                np.sin(np.deg2rad(dec)),
            ]
        )
        star_vector /= np.linalg.norm(star_vector, axis=0)
        position = self.get_spacecraft_position(time=time)
        return ((position * u.km).dot(star_vector) / (c)).to(u.s).value

    def get_velocity_aberrated_positions(
        self, time: Time, ra: float, dec: float
    ) -> npt.NDArray:
        """Returns the RA and Dec after velocity aberration has been applied.

        Note that `time` here must be time in spacecraft time, in UTC format.

        Parameters:
        -----------
        time: astropy.time.Time
            Time array at which to estimate position. Time must be in UTC.
        ra: float, np.ndarray
            The right ascention of the target in degrees
        dec: float, np.ndarray
            The declination of the target in degrees
        """

        # Compute the star vector (normalized direction vector for the target)
        star_vector = np.array(
            [
                np.cos(np.deg2rad(dec)) * np.cos(np.deg2rad(ra)),
                np.cos(np.deg2rad(dec)) * np.sin(np.deg2rad(ra)),
                np.sin(np.deg2rad(dec)),
            ]
        )

        # Normalize star_vector for safety (though it should already be normalized)
        star_vector /= np.linalg.norm(star_vector, axis=0)

        # Get the spacecraft velocity in m/s
        velocity = self.get_spacecraft_velocity(time=time) * 1000  # Convert km/s to m/s

        # Compute beta vector (velocity / speed of light)
        beta = velocity / c.value

        # Compute the scalar product beta \cdot star_vector
        beta_dot_star = np.sum(beta * star_vector, axis=-1)

        # Compute the relativistic factor gamma
        gamma = 1 / np.sqrt(1 - np.sum(beta**2, axis=-1))

        # Apply the aberration formula
        factor = 1 / (1 + beta_dot_star)

        star_vector_ab = factor[:, None] * (gamma[:, None] * star_vector + beta)

        # Normalize the aberrated vector
        star_vector_ab /= np.linalg.norm(star_vector_ab, axis=-1, keepdims=True)

        # Convert back to RA and Dec
        ra_aberrated = np.rad2deg(
            np.arctan2(star_vector_ab[:, 1], star_vector_ab[:, 0])
        )
        dec_aberrated = np.rad2deg(np.arcsin(star_vector_ab[:, 2]))

        # Ensure RA is in [0, 360] range
        ra_aberrated = np.mod(ra_aberrated, 360)

        # Reshape output to match input dimensions
        return (
            ra_aberrated,
            dec_aberrated,
        )


class KeplerSpacecraft(Spacecraft):
    """
    A class representing the Kepler spacecraft.

    This class extends the `Spacecraft` base class and includes spacecraft-specific
    configurations and calculations, such as correcting for timing errors unique to the
    Kepler mission.

    Attributes
    ----------
    spacecraft_code : int
        The SPICE NAIF ID code for the Kepler spacecraft.

    Methods
    -------
    get_barycentric_time_correction(time, ra, dec)
        Returns the barycentric time correction in days for observations of a target,
        applying mission-specific timing corrections.
    """

    spacecraft_code = -227
    time_offset = 2454833

    def get_barycentric_time_correction(
        self, time: Time, ra: Union[float, npt.NDArray], dec: Union[float, npt.NDArray]
    ) -> npt.NDArray:
        """Returns the barycentric time correction in days for observations of a particular target specified by RA and Dec.

        Note that `time` here must be time in spacecraft time, in UTC format.
        This means that for SPOC data this should be the time without the SPOC barycentric correction applied.

        Note this also corrects the timing error in the Kepler TIME column, see https://archive.stsci.edu/kepler/timing_error.html

        Parameters:
        -----------
        time: astropy.time.Time
            Time array at which to estimate position. Time must be in UTC.
        ra: float, np.ndarray
            The right ascention of the target in degrees
        dec: float, np.ndarray
            The declination of the target in degrees
        """
        time = self._process_time(time)
        tcorr = super().get_barycentric_time_correction(time, ra, dec)
        tcorr += 66.184
        k = time.jd > Time("2012-06-30 23:59:60", format="iso").jd
        tcorr[k] += 1
        return tcorr


class TESSSpacecraft(Spacecraft):
    """
    A class representing the TESS spacecraft.

    This class extends the `Spacecraft` base class and includes spacecraft-specific
    configurations, such as the unique SPICE NAIF ID code for the TESS mission.

    Attributes
    ----------
    spacecraft_code : int
        The SPICE NAIF ID code for the TESS spacecraft.
    """

    spacecraft_code = -95
    time_offset = 2457000
