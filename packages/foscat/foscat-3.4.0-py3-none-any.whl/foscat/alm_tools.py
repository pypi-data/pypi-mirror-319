import numpy as np

#====================================================================================================================
# This class is an automatic traduction of the fortran healpix software
#====================================================================================================================


class alm_tools():
    def __init__(self):
        pass

    @staticmethod
    def gen_recfac(l_max, m):
        """
        Generate recursion factors used to compute the Ylm of degree m for all l in m <= l <= l_max.

        Parameters:
        l_max (int): Maximum degree l.
        m (int): Degree m.

        Returns:
        np.ndarray: Recursion factors as a 2D array of shape (2, l_max + 1).
        """
        recfac = np.zeros((2, l_max + 1), dtype=np.float64)
        fm2 = float(m)**2

        for l in range(m, l_max + 1):
            fl2 = float(l + 1)**2
            recfac[0, l] = np.sqrt((4.0 * fl2 - 1.0) / (fl2 - fm2))

        recfac[1, m:l_max + 1] = 1.0 / recfac[0, m:l_max + 1]

        return recfac

    @staticmethod
    def gen_recfac_spin(l_max, m, spin):
        """
        Generate recursion factors for spin-weighted spherical harmonics.

        Parameters:
        l_max (int): Maximum degree l.
        m (int): Degree m.
        spin (int): Spin weight.

        Returns:
        np.ndarray: Recursion factors as a 2D array of shape (2, l_max + 1).
        """
        recfac_spin = np.zeros((2, l_max + 1), dtype=np.float64)
        fm2 = float(m)**2
        s2 = float(spin)**2

        for l in range(m, l_max + 1):
            fl2 = float(l + 1)**2
            recfac_spin[0, l] = np.sqrt((4.0 * fl2 - 1.0) / (fl2 - fm2))

        recfac_spin[1, m:l_max + 1] = (1.0 - s2 / (float(m) + 1.0)**2) / recfac_spin[0, m:l_max + 1]

        return recfac_spin

    @staticmethod
    def gen_lamfac(l_max):
        """
        Generate lambda factors for spherical harmonics.

        Parameters:
        l_max (int): Maximum degree l.

        Returns:
        np.ndarray: Lambda factors as a 1D array of size l_max + 1.
        """
        lamfac = np.zeros(l_max + 1, dtype=np.float64)

        for l in range(1, l_max + 1):
            lamfac[l] = np.sqrt(2.0 * l + 1.0)

        return lamfac

    @staticmethod
    def gen_lamfac_der(l_max):
        """
        Generate the derivatives of lambda factors.

        Parameters:
        l_max (int): Maximum degree l.

        Returns:
        np.ndarray: Lambda factor derivatives as a 1D array of size l_max + 1.
        """
        lamfac_der = np.zeros(l_max + 1, dtype=np.float64)

        for l in range(1, l_max + 1):
            lamfac_der[l] = (2.0 * l + 1.0) / np.sqrt(2.0 * l + 1.0)

        return lamfac_der

    @staticmethod
    def gen_mfac(m_max):
        """
        Generate m factors for spherical harmonics.

        Parameters:
        m_max (int): Maximum degree m.

        Returns:
        np.ndarray: M factors as a 1D array of size m_max + 1.
        """
        mfac = np.zeros(m_max + 1, dtype=np.float64)

        for m in range(1, m_max + 1):
            mfac[m] = np.sqrt(2.0 * m)

        return mfac

    @staticmethod
    def gen_mfac_spin(m_max, spin):
        """
        Generate m factors for spin-weighted spherical harmonics.

        Parameters:
        m_max (int): Maximum degree m.
        spin (int): Spin weight.

        Returns:
        np.ndarray: Spin-weighted m factors as a 1D array of size m_max + 1.
        """
        mfac_spin = np.zeros(m_max + 1, dtype=np.float64)

        for m in range(1, m_max + 1):
            mfac_spin[m] = np.sqrt(2.0 * m) * (1.0 - spin**2 / (m + 1)**2)

        return mfac_spin

    @staticmethod
    def compute_lam_mm(l_max, m):
        """
        Compute lambda values for specific m.

        Parameters:
        l_max (int): Maximum degree l.
        m (int): Degree m.

        Returns:
        np.ndarray: Lambda values as a 1D array of size l_max + 1.
        """
        lam_mm = np.zeros(l_max + 1, dtype=np.float64)

        for l in range(m, l_max + 1):
            lam_mm[l] = (2.0 * l + 1.0) * (1.0 - (m / (l + 1.0))**2)

        return lam_mm

    @staticmethod
    def do_lam_lm(l_max, m):
        """
        Perform computations for lambda values for all l, m.

        Parameters:
        l_max (int): Maximum degree l.
        m (int): Degree m.

        Returns:
        np.ndarray: Computed lambda values as a 2D array of size (l_max + 1, l_max + 1).
        """
        lam_lm = np.zeros((l_max + 1, l_max + 1), dtype=np.float64)

        for l in range(m, l_max + 1):
            for mp in range(m, l + 1):
                lam_lm[l, mp] = (2.0 * l + 1.0) * (1.0 - (mp / (l + 1.0))**2)

        return lam_lm

    @staticmethod
    def do_lam_lm_spin(l_max, m, spin):
        """
        Perform computations for spin-weighted lambda values for all l, m.

        Parameters:
        l_max (int): Maximum degree l.
        m (int): Degree m.
        spin (int): Spin weight.

        Returns:
        np.ndarray: Computed spin-weighted lambda values as a 2D array of size (l_max + 1, l_max + 1).
        """
        lam_lm_spin = np.zeros((l_max + 1, l_max + 1), dtype=np.float64)

        for l in range(m, l_max + 1):
            for mp in range(m, l + 1):
                lam_lm_spin[l, mp] = (2.0 * l + 1.0) * (1.0 - spin**2 / (mp + 1.0)**2)

        return lam_lm_spin

