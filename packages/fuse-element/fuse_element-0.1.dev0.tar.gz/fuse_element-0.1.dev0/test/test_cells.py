from fuse import *
import pytest
import numpy as np


@pytest.fixture(scope='module', params=[0, 1, 2])
def C(request):
    dim = request.param
    if dim == 0:
        return Point(0)
    elif dim == 1:
        return Point(1, [Point(0), Point(0)], vertex_num=2)
    elif dim == 2:
        return polygon(3)


def test_vertices(C):
    verts = C.vertices()
    assert len(verts) == C.dimension + 1


def test_basis_vectors(C):
    if C.dimension == 0:
        with pytest.raises(ValueError):
            bv_ids = C.basis_vectors()
        with pytest.raises(ValueError):
            bv_coords = C.basis_vectors(return_coords=True)
    else:
        bv_ids = C.basis_vectors()
        bv_coords = C.basis_vectors(return_coords=True)
        assert len(bv_ids) == len(bv_coords)


def test_orientation():
    cell = Point(1, [Point(0), Point(0)], vertex_num=2)
    print(cell.get_topology())
    for g in cell.group.members():
        if not g.perm.is_Identity:
            oriented = cell.orient(g)
            assert np.allclose(np.array(oriented.basis_vectors(return_coords=True)[0]), -1)


def test_sub_basis_vectors():
    cell = polygon(3)

    edges = cell.edges(get_class=True)
    print(cell.vertices())
    print(cell.vertices(return_coords=True))
    for e in edges:
        print(e)
        print(e.vertices())
        print(cell.basis_vectors(entity=e))


def test_permute_entities():
    cell = polygon(3)
    # cell.plot(filename="test_cell.png")

    # for dof in nd.generate():
    # print(dof, "->", dof(reflect), "eval p2 ", dof(reflect).eval(phi_2), "eval p0 ", dof(reflect).eval(phi_0), "eval p1 ", dof(reflect).eval(phi_1))
    # print(dof.convert_to_fiat(cell.to_fiat(), 1)(lambda x: np.array([1/3 - (np.sqrt(3)/6)*x[1], (np.sqrt(3)/6)*x[0]])))

    print(cell.vertices(return_coords=True))
    print([c.point.connections for c in cell.connections])
    print([[c.point.get_node(c2.point.id, return_coords=True) for c2 in c.point.connections] for c in cell.connections])
    # cell.plot(filename="test_cell_flipped.png")
    # import matplotlib.pyplot as plt
    for i, g in enumerate(cell.group.members()):
        print(i, g)
        print(cell.permute_entities(g, 0))
        print(cell.permute_entities(g, 1))
    #     oriented = cell.orient(g)
    #     print("Edges", oriented.connections)
    #     fig, ax = plt.subplots()
    #     oriented.plot(ax = ax, filename=f"test_cell{i}.png")
    #     oriented.hasse_diagram(filename=f"test_hasse{i}.png")


def test_oriented_verts():
    edge = Point(1, [Point(0), Point(0)], vertex_num=2)

    for g in edge.group.members():
        oriented = edge.orient(g)
        assert g.permute(edge.ordered_vertices()) == oriented.ordered_vertices()

    tri = polygon(3)
    cyclic_tri = C3.add_cell(tri)

    for g in tri.group.members():
        oriented = tri.orient(g)
        if g in cyclic_tri.members():
            # test that rotating does not change the order of edges
            permuted = oriented.permute_entities(g, 1)
            assert all([o.perm.is_Identity for (e, o) in permuted])
        assert g.permute(tri.ordered_vertices()) == oriented.ordered_vertices()

    sq = polygon(4)
    for g in sq.group.members():
        oriented = sq.orient(g)
        print(oriented.permute_entities(g, 1))
        assert g.permute(sq.ordered_vertices()) == oriented.ordered_vertices()

    tetra = make_tetrahedron()
    for g in tetra.group.members():
        oriented = tetra.orient(g)
        permuted = oriented.permute_entities(g, 0)
        print(g, permuted)
        assert g.permute(tetra.ordered_vertices()) == oriented.ordered_vertices()
