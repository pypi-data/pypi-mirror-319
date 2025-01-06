from __future__ import annotations

import numpy as np
from ase.units import Bohr, Ha

from gpaw.core.arrays import DistributedArrays as XArray
from gpaw.core.atom_arrays import AtomArrays, AtomDistribution
from gpaw.core.domain import Domain as XDesc
from gpaw.core import PWArray, UGArray, UGDesc
from gpaw.mpi import MPIComm, broadcast_float
from gpaw.new import zips


class Potential:
    def __init__(self,
                 vt_sR: UGArray,
                 dH_asii: AtomArrays,
                 dedtaut_sR: UGArray | None,
                 energies: dict[str, float],
                 vHt_x: XArray | None = None):
        self.vt_sR = vt_sR
        self.dH_asii = dH_asii
        self.dedtaut_sR = dedtaut_sR
        self.energies = energies
        self.vHt_x = vHt_x  # initial guess for Hartree potential

    def __repr__(self):
        return (f'Potential({self.vt_sR}, {self.dH_asii}, '
                f'{self.dedtaut_sR}, {self.energies})')

    def __str__(self) -> str:
        return (f'potential:\n'
                f'  grid points: {self.vt_sR.desc.size}\n')

    def update_from(self, potential):
        self.vt_sR = potential.vt_sR
        self.dH_asii = potential.dH_asii
        self.dedtaut_sR = potential.dedtaut_sR
        self.energies = potential.energies
        self.vHt_x = potential.vHt_x

    def dH(self, P_ani, out_ani, spin):
        if len(P_ani.dims) == 1:  # collinear wave functions
            P_ani.block_diag_multiply(self.dH_asii, out_ani, spin)
            return

        # Non-collinear wave functions:
        P_ansi = P_ani
        out_ansi = out_ani

        for (a, P_nsi), out_nsi in zips(P_ansi.items(), out_ansi.values()):
            v_ii, x_ii, y_ii, z_ii = (dh_ii.T for dh_ii in self.dH_asii[a])
            assert v_ii.dtype == complex
            out_nsi[:, 0] = (P_nsi[:, 0] @ (v_ii + z_ii) +
                             P_nsi[:, 1] @ (x_ii - 1j * y_ii))
            out_nsi[:, 1] = (P_nsi[:, 1] @ (v_ii - z_ii) +
                             P_nsi[:, 0] @ (x_ii + 1j * y_ii))
        return out_ansi

    def move(self, atomdist: AtomDistribution) -> None:
        """Move atoms inplace."""
        self.dH_asii = self.dH_asii.moved(atomdist)

    def redist(self,
               grid: UGDesc,
               desc: XDesc,
               atomdist: AtomDistribution,
               comm1: MPIComm,
               comm2: MPIComm) -> Potential:
        return Potential(
            self.vt_sR.redist(grid, comm1, comm2),
            self.dH_asii.redist(atomdist, comm1, comm2),
            None if self.dedtaut_sR is None else self.dedtaut_sR.redist(
                grid, comm1, comm2),
            self.energies.copy(),
            None if self.vHt_x is None else self.vHt_x.redist(
                desc, comm1, comm2))

    def _write_gpw(self, writer, ibzwfs, precision='double'):
        from gpaw.new.calculation import combine_energies
        energies = combine_energies(self, ibzwfs)
        energies['band'] = ibzwfs.energies['band']
        if 'stress' in self.energies:
            energies['stress'] = self.energies['stress']
        dH_asp = self.dH_asii.to_cpu().to_lower_triangle().gather()
        vt_sR = self.vt_sR.to_xp(np).gather()
        if self.dedtaut_sR is not None:
            dedtaut_sR = self.dedtaut_sR.to_xp(np).gather()
        if self.vHt_x is not None:
            vHt_x = self.vHt_x.to_xp(np).gather()
        if dH_asp is None:
            return

        vt_sR_data = vt_sR.data
        if precision == 'single':
            from gpaw.new.gpw import as_single_precision
            vt_sR_data = as_single_precision(vt_sR_data)
        writer.write(
            potential=vt_sR_data * Ha,
            atomic_hamiltonian_matrices=dH_asp.data * Ha,
            **{f'e_{name}': val * Ha for name, val in energies.items()})
        if self.vHt_x is not None:
            vHt_x_data = vHt_x.data
            if precision == 'single':
                vHt_x_data = as_single_precision(vHt_x_data)
            writer.write(electrostatic_potential=vHt_x_data * Ha)
        if self.dedtaut_sR is not None:
            dedtaut_sR_data = dedtaut_sR.data
            if precision == 'single':
                dedtaut_sR_data = as_single_precision(dedtaut_sR_data)
            writer.write(mgga_potential=dedtaut_sR_data * Bohr**3)

    def get_vacuum_level(self) -> float:
        grid = self.vt_sR.desc
        if grid.pbc_c.all():
            return np.nan
        if grid.zerobc_c.any():
            return 0.0
        if self.vHt_x is None:
            raise ValueError('No electrostatic potential')
        if isinstance(self.vHt_x, UGArray):
            vHt_r = self.vHt_x.gather()
        elif isinstance(self.vHt_x, PWArray):
            vHt_g = self.vHt_x.gather()
            if vHt_g is not None:
                vHt_r = vHt_g.ifft(grid=vHt_g.desc.minimal_uniform_grid())
            else:
                vHt_r = None
        else:
            return np.nan  # TB-mode
        vacuum_level = 0.0
        if vHt_r is not None:
            for c, periodic in enumerate(grid.pbc_c):
                if not periodic:
                    xp = vHt_r.xp
                    vacuum_level += float(xp.moveaxis(vHt_r.data,
                                                      c, 0)[0].mean())

            vacuum_level /= (3 - grid.pbc_c.sum())

        return broadcast_float(vacuum_level, grid.comm) * Ha
