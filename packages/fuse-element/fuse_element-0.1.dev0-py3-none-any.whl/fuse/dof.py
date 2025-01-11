from FIAT.quadrature_schemes import create_quadrature
from FIAT.quadrature import FacetQuadratureRule
from FIAT.functional import PointEvaluation, FrobeniusIntegralMoment
from fuse.utils import sympy_to_numpy
import numpy as np
import sympy as sp


class Pairing():
    """
    Akin to an inner product, the pairing combines a kernel and an input function
    """

    def __init__(self):
        self.entity = None

    def _to_dict(self):
        o_dict = {"entity": self.entity}
        return o_dict


class DeltaPairing(Pairing):
    """
    The delta pairing allows the evaluation at a single points

    Calling method:
    :param: kernel: Normally a PointKernel
    """

    def __init__(self):
        super(DeltaPairing, self).__init__()

    def __call__(self, kernel, v, cell):
        assert isinstance(kernel, PointKernel)
        return v(*kernel.pt)

    def convert_to_fiat(self, ref_el, dof, interpolant_deg):
        pt = dof.eval(MyTestFunction(lambda *x: x))
        return PointEvaluation(ref_el, pt)

    def add_entity(self, entity):
        res = DeltaPairing()
        res.entity = entity
        return res

    def __repr__(self):
        return "{fn}({kernel})"

    def dict_id(self):
        return "Delta"

    def _from_dict(obj_dict):
        new_obj = DeltaPairing()
        new_obj.add_entity(obj_dict["entity"])
        return new_obj


class L2Pairing(Pairing):
    """ need to think about the abstraction level here -
    are we wanting to define them as quadrature now? or defer this?
    """
    def __init__(self):
        super(L2Pairing, self).__init__()

    def __call__(self, kernel, v, cell):
        # print(self.entity)
        # if cell == self.entity:
        #     # print("evaluating", kernel, v, "on", self.entity)
        #     quadrature = create_quadrature(self.entity.to_fiat(), 5)
        #     # need quadrature here too - therefore need the information from the triple.
        # else:
        #     ref_el = cell.to_fiat()
        #     print(cell)
        #     ent_id = self.entity.id - ref_el.fe_cell.get_starter_ids()[self.entity.dim()]
        #     entity = ref_el.construct_subelement(self.entity.dim())
        #     Q_ref = create_quadrature(entity, 5)
        #     quadrature = FacetQuadratureRule(ref_el, self.entity.dim(), ent_id, Q_ref)
        quadrature = create_quadrature(self.entity.to_fiat(), 5)

        def kernel_dot(x):
            return np.dot(kernel(*x), v(*x))

        return quadrature.integrate(kernel_dot)

    def tabulate(self):
        pass

    def add_entity(self, entity):
        res = L2Pairing()
        res.entity = entity
        return res

    def convert_to_fiat(self, ref_el, dof, interpolant_degree):
        total_deg = interpolant_degree + dof.kernel.degree()
        ent_id = self.entity.id - ref_el.fe_cell.get_starter_ids()[self.entity.dim()]
        entity = ref_el.construct_subelement(self.entity.dim())
        Q_ref = create_quadrature(entity, total_deg)
        Q = FacetQuadratureRule(ref_el, self.entity.dim(), ent_id, Q_ref)
        Jdet = Q.jacobian_determinant()
        qpts, _ = Q.get_points(), Q.get_weights()
        print(qpts)
        print(dof.tabulate(qpts))
        f_at_qpts = dof.tabulate(qpts).T / Jdet
        print(len(Q.pts))
        print(f_at_qpts.shape)
        functional = FrobeniusIntegralMoment(ref_el, Q, f_at_qpts)
        return functional

    def __repr__(self):
        return "integral_{}({{kernel}} * {{fn}}) dx)".format(str(self.entity))

    def dict_id(self):
        return "L2Inner"

    def _from_dict(obj_dict):
        new_obj = L2Pairing()
        new_obj.add_entity(obj_dict["entity"])
        return new_obj


class BaseKernel():

    def __init__(self):
        self.attachment = False

    def permute(self, g):
        raise NotImplementedError("This method should be implemented by the subclass")

    def __repr__(self):
        return "BaseKernel"

    def __call__(self, *args):
        raise NotImplementedError("This method should be implemented by the subclass")


class PointKernel(BaseKernel):

    def __init__(self, x):
        if not isinstance(x, tuple):
            x = (x,)
        self.pt = x
        super(PointKernel, self).__init__()

    def __repr__(self):
        x = list(map(str, list(self.pt)))
        return ','.join(x)

    def degree(self):
        return 1

    def permute(self, g):
        return PointKernel(g(self.pt))

    def __call__(self, *args):
        return self.pt

    def tabulate(self, Qpts):
        return np.array([self.pt for _ in Qpts]).astype(np.float64)

    def _to_dict(self):
        o_dict = {"pt": self.pt}
        return o_dict

    def dict_id(self):
        return "PointKernel"

    def _from_dict(obj_dict):
        return PointKernel(tuple(obj_dict["pt"]))


class PolynomialKernel(BaseKernel):

    def __init__(self, fn, symbols=[]):
        if len(symbols) != 0 and not sp.sympify(fn).as_poly():
            raise ValueError("Function argument must be able to be interpreted as a sympy polynomial")
        self.fn = sp.sympify(fn)
        self.syms = symbols
        super(PolynomialKernel, self).__init__()

    def __repr__(self):
        return str(self.fn)

    def degree(self):
        if len(self.fn.free_symbols) == 0:
            return 1
        return self.fn.as_poly().total_degree()

    def permute(self, g):
        new_fn = self.fn.subs({self.syms[i]: g(self.syms)[i] for i in range(len(self.syms))})
        return PolynomialKernel(new_fn, symbols=self.syms)

    def __call__(self, *args):
        res = sympy_to_numpy(self.fn, self.syms, args[:len(self.syms)])
        if not hasattr(res, '__iter__'):
            return [res]
        return res

    def tabulate(self, Qpts):
        return np.array([self(*pt) for pt in Qpts]).astype(np.float64)

    def _to_dict(self):
        o_dict = {"fn": self.fn}
        return o_dict

    def dict_id(self):
        return "PolynomialKernel"

    def _from_dict(obj_dict):
        return PolynomialKernel(obj_dict["fn"])


class DOF():

    def __init__(self, pairing, kernel, entity=None, attachment=None, target_space=None, g=None, immersed=False, generation=None, sub_id=None, cell=None):
        self.pairing = pairing
        self.kernel = kernel
        self.immersed = immersed
        self.trace_entity = entity
        self.attachment = attachment
        self.target_space = target_space
        self.g = g
        self.id = None
        self.sub_id = sub_id
        self.cell = cell

        if generation is None:
            self.generation = {}
        else:
            self.generation = generation
        if entity is not None:
            self.pairing = self.pairing.add_entity(entity)

    def __call__(self, g):
        new_generation = self.generation.copy()
        return DOF(self.pairing, self.kernel.permute(g), self.trace_entity, self.attachment, self.target_space, g, self.immersed, new_generation, self.sub_id, self.cell)

    def eval(self, fn, pullback=True):
        return self.pairing(self.kernel, fn, self.cell)

    def tabulate(self, Qpts):
        return self.kernel.tabulate(Qpts)

    def add_context(self, dof_gen, cell, space, g, overall_id=None, generator_id=None):
        # For some of these, we only want to store the first instance of each
        self.generation[cell.dim()] = dof_gen
        self.cell = cell
        if self.trace_entity is None:
            self.trace_entity = cell
            self.pairing = self.pairing.add_entity(cell)
        if self.target_space is None:
            self.target_space = space
        if self.id is None and overall_id is not None:
            self.id = overall_id
        if self.sub_id is None and generator_id is not None:
            self.sub_id = generator_id

    def convert_to_fiat(self, ref_el, interpolant_degree):
        return self.pairing.convert_to_fiat(ref_el, self, interpolant_degree)
        raise NotImplementedError("Fiat conversion only implemented for Point eval")

    def __repr__(self, fn="v"):
        return str(self.pairing).format(fn=fn, kernel=self.kernel)

    def immerse(self, entity, attachment, target_space, g, triple):
        new_generation = self.generation.copy()
        return ImmersedDOF(self.pairing, self.kernel, entity, attachment, target_space, g, triple, new_generation, self.sub_id, self.cell)

    def _to_dict(self):
        """ almost certainly needs more things"""
        o_dict = {"pairing": self.pairing, "kernel": self.kernel}
        return o_dict

    def dict_id(self):
        return "DOF"

    def _from_dict(obj_dict):
        return DOF(obj_dict["pairing"], obj_dict["kernel"])


class ImmersedDOF(DOF):
    # probably need to add a convert to fiat method here to capture derivatives from immersion
    def __init__(self, pairing, kernel, entity=None, attachment=None, target_space=None, g=None, triple=None, generation=None, sub_id=None, cell=None):
        self.immersed = True
        self.triple = triple
        super(ImmersedDOF, self).__init__(pairing, kernel, entity=entity, attachment=attachment, target_space=target_space, g=g, immersed=True, generation=generation, sub_id=sub_id, cell=cell)

    def eval(self, fn, pullback=True):
        attached_fn = fn.attach(self.attachment)

        if pullback:
            attached_fn = self.target_space(attached_fn, self.trace_entity, self.g)

        return self.pairing(self.kernel, attached_fn, self.cell)

    def tabulate(self, Qpts):
        immersion = self.target_space.tabulate(Qpts, self.trace_entity, self.g)
        res = self.kernel.tabulate(Qpts)
        return immersion*res

    def __call__(self, g):
        permuted = self.cell.permute_entities(g, self.trace_entity.dim())
        index_trace = self.cell.d_entities_ids(self.trace_entity.dim()).index(self.trace_entity.id)
        new_trace_entity = self.cell.get_node(permuted[index_trace][0]).orient(permuted[index_trace][1])

        return ImmersedDOF(self.pairing, self.kernel.permute(permuted[index_trace][1]), new_trace_entity,
                           self.attachment, self.target_space, g, self.triple, self.generation, self.sub_id, self.cell)

    def __repr__(self):
        fn = "tr_{1}_{0}(v)".format(str(self.trace_entity), str(self.target_space))
        return super(ImmersedDOF, self).__repr__(fn)

    def immerse(self, entity, attachment, trace, g):
        raise RuntimeError("Error: Immersing twice not supported")


class MyTestFunction():

    def __init__(self, eq, attach_func=None, symbols=None):
        self.eq = eq
        self.attach_func = attach_func
        self.symbols = symbols

    def __call__(self, *x, sym=False):
        if self.symbols:
            if self.attach_func and not sym:
                res = self.eq.subs({symb: val for (symb, val) in zip(self.symbols, self.attach_func(*x))})
            else:
                res = self.eq.subs({symb: val for (symb, val) in zip(self.symbols, x)})
            if res.free_symbols == set():
                array = np.array(res).astype(np.float64)
                return array
            else:
                return res
        if self.attach_func and not sym:
            return self.eq(*self.attach_func(*x))
        else:
            # TODO remove this as will already be symbolic
            return self.eq(*x)

    def attach(self, attachment):
        if not self.attach_func:
            return MyTestFunction(self.eq, attach_func=attachment, symbols=self.symbols)
        else:
            old_attach = self.attach_func
            if self.symbols:
                return MyTestFunction(self.eq,
                                      attach_func=attachment(old_attach(*self.symbols)),
                                      symbols=self.symbols)
            else:
                return MyTestFunction(self.eq,
                                      attach_func=lambda *x: attachment(old_attach(*x)))

    def __repr__(self):
        if self.attach_func:
            return "v(G(x))"
        else:
            return "v(x)"

    def _to_dict(self):
        return {"eq": self.eq}

    def dict_id(self):
        return "Function"
