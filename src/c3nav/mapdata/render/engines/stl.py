import numpy as np

from c3nav.mapdata.render.engines.base3d import Base3DEngine


class STLEngine(Base3DEngine):
    facet_template = (b'  facet normal %f %f %f\n'
                      b'    outer loop\n'
                      b'     vertex %f %f %f\n'
                      b'      vertex %f %f %f\n'
                      b'      vertex %f %f %f\n'
                      b'    endloop\n'
                      b'  endfacet')

    def _create_facet(self, facet) -> bytes:
        return self.facet_template % tuple(facet.flatten())

    def render(self) -> bytes:
        facets = np.vstack(self.vertices)
        facets = np.hstack((np.cross(facets[:, 1]-facets[:, 0], facets[:, 2]-facets[:, 1]).reshape((-1, 1, 3))*1e10,
                            facets))
        return (b'solid c3nav_export\n' +
                b'\n'.join((self._create_facet(facet) for facet in facets)) +
                b'\nendsolid c3nav_export\n')
