"""From the ../Code/ directory, run: python -m src.model_checker src/model_checker/champollion.py"""

import z3

from src.model_checker.utils import (
    ForAll,
    Exists,
    bitvec_to_substates,
)

from src.model_checker import model

from src.model_checker import syntactic

class ChampollionSemantics(model.SemanticDefaults):
    def __init__(self, N):
        # Initialize the superclass to set defaults
        super().__init__(N)

        self.verify = z3.Function(
            "verify",  # name
            z3.BitVecSort(N),  # first argument type: bitvector
            syntactic.AtomSort,  # second argument type: sentence letter
            z3.BoolSort(),  # return type: boolean
        )
        self.excludes = z3.Function(
            "excludes",  # name
            z3.BitVecSort(N),  # first argument type: bitvector
            z3.BitVecSort(N),  # second argument type: bitvector
            z3.BoolSort(),  # return type: boolean
        )
        self.main_world = z3.BitVec("w", N)

        # Define frame constraints
        x, y = z3.BitVecs("frame_x frame_y", self.N)
        actuality = self.is_world(self.main_world)
        exclusion_symmetry = ForAll(
            [x, y],
            z3.Implies(
                self.excludes(x, y),
                self.excludes(y, x)
            )
        )
        harmony = ForAll( 
            [x, y],
            z3.Implies(
                z3.And(
                    self.is_world(x),
                    self.coheres(x, y)
                ),
                self.possible(y)
            )
        )
        rashomon = ForAll(
            [x, y],
            z3.Implies(
                z3.And(
                    self.possible(x),
                    self.possible(y),
                    self.coheres(x, y)
                ),
                self.possible(self.fusion(x, y)),
            ),
        )
        cosmopolitanism = ForAll( # NOTE: should be redundant given finiteness
            x,                    # B: Adding the negation of this is unsat and 
            z3.Implies(           # so we don't need to impose cosmopolitanism  
                self.possible(x),
                Exists(
                    y,
                    z3.And(
                        self.is_world(y),
                        self.is_part_of(x, y)
                    )
                )
            )
        )
        neg_actuality = z3.Not(actuality)
        neg_exclusion_symmetry = z3.Not(exclusion_symmetry)
        neg_cosmopolitanism = z3.Not(cosmopolitanism)
        neg_harmony = z3.Not(harmony)
        neg_rashomon = z3.Not(rashomon)
        # Set frame constraints
        self.frame_constraints = [
            actuality,
            # neg_actuality, # NOTE: this is satisfiable
            exclusion_symmetry,
            # neg_exclusion_symmetry, # NOTE: this is satisfiable
            harmony,
            # neg_harmony, # NOTE: this is satisfiable
            rashomon, # guards against emergent impossibility (pg 538)
            # neg_rashomon, # NOTE: this is satisfiable
            # cosmopolitanism, # B: see note above
            # neg_cosmopolitanism, # NOTE: this is unsatisfiable
        ]

        # Define invalidity conditions
        self.premise_behavior = self.true_at
        self.conclusion_behavior = lambda x,y: z3.Not(self.true_at(x,y))

    def conflicts(self, bit_e1, bit_e2):
        f1, f2 = z3.BitVecs("f1 f2", self.N)
        return Exists(
            [f1, f2],
            z3.And(
                self.is_part_of(f1, bit_e1),
                self.is_part_of(f2, bit_e2),
                self.excludes(f1, f2),
            ),
        )

    def coheres(self, bit_e1, bit_e2):
        return z3.Not(self.conflicts(bit_e1, bit_e2))

    def possible(self, bit_e):
        return self.coheres(bit_e, bit_e)

    def compossible(self, bit_e1, bit_e2):
        return self.possible(self.fusion(bit_e1, bit_e2))

    # B: compossible => coheres but not vice versa
    # would they be equivalent if the following constraint were added:
    # (CON_REF) if x and y are parts of s that exclude each other, then s excludes s

    def is_world(self, bit_s):
        m = z3.BitVec("m", self.N)
        return z3.And(
            self.possible(bit_s),
            z3.Not(
                Exists(
                    m,
                    z3.And(
                        self.is_proper_part_of(bit_s, m),
                        self.possible(m)
                    )
                )
            )
        )

    def necessary(self, bit_e1):
        x = z3.BitVec("nec_x", self.N)
        return ForAll(x, z3.Implies(self.possible(x), self.compossible(bit_e1, x)))

    def collectively_excludes(self, bit_s, set_P):
        return self.excludes(bit_s, self.total_fusion(set_P))

    def individually_excludes(self, bit_s, set_P):
        sub_s, p = z3.BitVecs("sub_s p", self.N)
        P = self.z3_set(set_P, self.N)
        cond_a = Exists(
            [sub_s, p],
            z3.And(self.is_part_of(sub_s, bit_s), P[p], self.excludes(sub_s, p)),
        )
        # Sigma is upper bound on excluders of set P
        Sigma = z3.BitVec(str(set_P), self.N)
        x, y, z, p = z3.BitVecs("x y z p", self.N)
        Sigma_UB = ForAll(
            x,
            z3.Implies(
                Exists(
                    p,
                    z3.And(
                        P[p],
                        self.excludes(x, p)
                    )
                ),
                self.is_part_of(x, Sigma)
            ),
        )
        # Sigma is the least upper bound on excluders of set P
        Sigma_LUB = ForAll(
            z,
            z3.Implies(
                ForAll(
                    y,
                    z3.Implies(
                        Exists(
                            p,
                            z3.And(
                                P[p],
                                self.excludes(y, p)
                            )
                        ),
                        self.is_part_of(y, z),
                    ),
                ),
                z == Sigma
            ),
        )

        return z3.And(
            cond_a,
            Sigma_UB,
            Sigma_LUB,
            self.is_part_of(bit_s, Sigma)
        )

    def emergently_excludes(self, bit_s, set_P):
        return z3.And(
            self.collectively_excludes(bit_s, set_P),
            z3.Not(self.individually_excludes(bit_s, set_P)),
        )

    def precludes(self, state, set_S):
        h = z3.Function(
            f"h_{(state, set_S)}*", # unique name
            z3.BitVecSort(self.N), # argument type: bitvector
            z3.BitVecSort(self.N) # return type: bitvector
        )
        s, x, y, z, f, u = z3.BitVecs("s x y z f u", self.N) # bitvector variables
        return Exists(
            [h, s],
            z3.And(
                ForAll( # (A) h(x) part of s for all x in set_P
                    x,
                    z3.Implies(
                        set_S[x],
                        self.is_part_of(h(x), s)
                    )
                ),
                ForAll( # (B) s is the smallest state to satisfy condition (A)
                    z,
                    z3.Implies(
                        ForAll(
                            y,
                            z3.Implies(
                                set_S[y],
                                self.is_part_of(h(y), z)
                            )
                        ),
                        z == s
                    )
                ),
                ForAll(
                    f,
                    z3.Implies(
                        set_S[f],
                        Exists(
                            u,
                            z3.And(
                                self.excludes(h(f), u),
                                self.is_part_of(u, f)
                            )
                        )
                    )
                )
            )
        )

    def occurs(self, bit_s):
        return self.is_part_of(bit_s, self.main_world)
    
    def true_at(self, sentence, eval_world):
        sentence_letter = sentence.sentence_letter
        if sentence_letter is not None:
            x = z3.BitVec("t_atom_x", self.N)
            return Exists(
                x,
                z3.And(
                    self.is_part_of(x, eval_world),
                    self.verify(x, sentence_letter)
                )
            )
        operator = sentence.operator
        arguments = sentence.arguments or ()
        return operator.true_at(*arguments, eval_world)

    def extended_verify(self, state, sentence, eval_world):
        sentence_letter = sentence.sentence_letter
        if sentence_letter is not None:
            return self.verify(state, sentence_letter)
        operator = sentence.operator
        arguments = sentence.arguments or ()
        return operator.extended_verify(state, *arguments, eval_world)


class ChampollionProposition(model.PropositionDefaults):
    """Defines the proposition assigned to the sentences of the language.
    all user has to keep for their own class is super().__init__ and super().__poster_init__
    in the __init__ method.
    """

    def __init__(self, sentence_obj, model_structure, eval_world='main'):
        """TODO"""

        super().__init__(sentence_obj, model_structure)
        self.eval_world = model_structure.main_world if eval_world == 'main' else eval_world
        self.verifiers = self.find_proposition()

    def __eq__(self, other):
        return (self.verifiers == other.verifiers)

    def proposition_constraints(self, sentence_letter):
        """
        Generates Z3 constraints for a sentence letter including the classical
        constraints and optionally the non-null, contingent, and disjoint
        constraints depending on the user settings."""
        semantics = self.semantics

        def get_fusion_closure_constraint():
            x, y = z3.BitVecs("cl_prop_x cl_prop_y", semantics.N)
            """The classical_constraints rule out truth_value gaps and gluts."""
            verifier_fusion_closure = ForAll(
                [x, y],
                z3.Implies(
                    z3.And(semantics.verify(x, sentence_letter), semantics.verify(y, sentence_letter)),
                    semantics.verify(semantics.fusion(x, y), sentence_letter),
                ),
            )
            return [verifier_fusion_closure]

        def get_non_empty_constraints():
            """The non_empty_constraints are important to avoid trivializing
            the disjoin_constraints, but are entailed by the contingent_constraints."""
            x = z3.BitVec("ct_empty_x", semantics.N)
            return [
                z3.Exists(
                    x,
                    semantics.verify(x, sentence_letter)
                )
            ]

        def get_non_null_constraints():
            """The non_null_constraints are important to avoid trivializing
            the disjoin_constraints, but are entailed by the contingent_constraints."""
            return [z3.Not(semantics.verify(0, sentence_letter))]

        def get_possible_constraints():
            """The possible_constraint entail the non_null_constraints."""
            x = z3.BitVec("ps_prop_x", semantics.N)
            possible_verifier = Exists(
                x,
                z3.And(
                    semantics.possible(x),
                    semantics.verify(x, sentence_letter)
                )
            )
            return [possible_verifier]

        def get_contingent_constraint():
            """The contingent_constraint entail the possible_constraint."""
            x, y, z = z3.BitVecs("ct_prop_x ct_prop_y ct_prop_z", semantics.N)
            possibly_true = Exists(
                x,
                z3.And(
                    semantics.possible(x),
                    semantics.verify(x, sentence_letter)
                )
            )
            possibly_false = Exists(
                y,
                z3.And(
                    semantics.is_world(y),
                    z3.ForAll(
                        z,
                        z3.Implies(
                            semantics.is_part_of(z, y),
                            z3.Not(semantics.verify(z, sentence_letter))
                        )
                    )
                )
            )
            return [possibly_true, possibly_false]

        def get_disjoint_constraints():
            """The non_null_constraints are included in disjoin_constraints."""
            x, y, z = z3.BitVecs("dj_prop_x dj_prop_y dj_prop_z", semantics.N)
            disjoint_constraints = []
            for other_sentence in self.sentence_letters:
                # TODO: make sentence_letters not sentence_objects?
                other_letter = other_sentence.sentence_letter
                if other_letter is not sentence_letter:
                    other_disjoint_atom = ForAll(
                        [x, y],
                        z3.Implies(
                            z3.And(
                                semantics.non_null_part_of(x, y),
                                semantics.verify(y, sentence_letter),
                            ),
                            ForAll(
                                z,
                                z3.Implies(
                                    semantics.verify(z, other_letter),
                                    z3.Not(semantics.is_part_of(x, z)),
                                )
                            )
                        )
                    )
                    disjoint_constraints.append(other_disjoint_atom)
            return disjoint_constraints

        # Collect constraints
        constraints = []
        non_empty_needed = True
        non_null_needed = True
        if self.settings['contingent']:
            constraints.extend(get_contingent_constraint())
            non_empty_needed = False
        if self.settings['possible'] and not self.settings['contingent']:
            constraints.extend(get_possible_constraints())
            non_empty_needed = False
        if self.settings['non_empty'] and non_empty_needed:
            constraints.extend(get_non_empty_constraints())
        if self.settings['disjoint']:
            constraints.extend(get_disjoint_constraints())
            constraints.extend(get_non_null_constraints())
            non_null_needed = False
        if self.settings['non_null'] and non_null_needed:
            constraints.extend(get_non_null_constraints())
        if self.settings['fusion_closure']:
            constraints.extend(get_fusion_closure_constraint())
        return constraints

    def find_proposition(self):
        """takes self, returns the V, F tuple
        used in find_verifiers"""
        all_bits = self.model_structure.all_bits
        model = self.model_structure.z3_model
        semantics = self.semantics
        eval_world = self.eval_world
        operator = self.operator
        arguments = self.arguments or ()
        sentence_letter = self.sentence_letter
        if sentence_letter is not None:
            V = {
                bit for bit in all_bits
                if model.evaluate(semantics.verify(bit, sentence_letter))
            }
            return V
        if operator is not None:
            return operator.find_verifiers(*arguments, eval_world)
        raise ValueError(f"Their is no proposition for {self.name}.")

    def truth_value_at(self, world):
        """Checks if there is a verifier in world."""
        semantics = self.model_structure.semantics
        z3_model = self.model_structure.z3_model
        for ver_bit in self.verifiers:
            if z3_model.evaluate(semantics.is_part_of(ver_bit, world)):
                return True
        return False

    def print_proposition(self, eval_world, indent_num, use_colors):
        N = self.model_structure.semantics.N
        truth_value = self.truth_value_at(eval_world)
        world_state = bitvec_to_substates(eval_world, N)
        RESET, FULL, PART = self.set_colors(self.name, indent_num, truth_value, world_state, use_colors)
        print(
            f"{'  ' * indent_num}{FULL}|{self.name}| = {self}{RESET}"
            f"  {PART}({truth_value} in {world_state}){RESET}"
        )


class ExclusionOperator(syntactic.Operator):
    """doc string place holder"""

    name = "\\exclude"
    arity = 1

    def true_at(self, arg, eval_world):
        """doc string place holder"""
        x = z3.BitVec(f"ver \\exclude {arg}", self.semantics.N) # think this has to be a unique name
        return Exists(
            x,
            z3.And(
                self.extended_verify(x, arg, eval_world),
                self.semantics.is_part_of(x, eval_world)
            )
        )

    def extended_verify(self, state, arg, eval_world):
        sem = self.semantics
        N, extended_verify, excludes = sem.N, sem.extended_verify, sem.excludes
        is_part_of = sem.is_part_of
        h = z3.Function(f"h_{(state, arg)}", z3.BitVecSort(N), z3.BitVecSort(N))
        v, x, y, z, s = z3.BitVecs("v x y z s", N)
        # return self.precludes(state, arg_set)
        return z3.And(
            ForAll( # 1. every extended_verier v for arg has a part s where
                v,  # h(v) excludes s
                z3.Implies(
                    extended_verify(v, arg, eval_world), # member of argument's set of verifiers
                    Exists(
                        s,
                        z3.And(
                            excludes(h(v), s),
                            is_part_of(s, v)
                        )
                    )
                )
            ),
            ForAll( # 2. h(x) is a part of the state for all extended_veriers x of arg
                x,
                z3.Implies(
                    extended_verify(x, arg, eval_world),
                    is_part_of(h(x), state),
                )
            ),
            ForAll( # 3. the state is the smallest state to satisfy condition 2
                z,
                z3.Implies(
                    ForAll(
                        y,
                        z3.Implies(
                            extended_verify(y, arg, eval_world),
                            is_part_of(h(y), state)
                        )
                    ),
                    z == state
                )
            )
        )

    def find_verifiers(self, argsent, eval_world):
        eval = argsent.proposition.model_structure.z3_model.evaluate
        all_bits = self.semantics.all_bits
        return {x for x in all_bits if eval(self.extended_verify(x, argsent, eval_world))}

    def print_method(self, sentence_obj, eval_world, indent_num, use_colors):
        """Prints the proposition for sentence_obj, increases the indentation
        by 1, and prints the argument."""
        self.general_print(sentence_obj, eval_world, indent_num, use_colors)


class UniAndOperator(syntactic.Operator):
    """doc string place holder"""

    name = "\\uniwedge"
    arity = 2

    def true_at(self, leftarg, rightarg, eval_world):
        """doc string place holder
        args are derived_objects I think, def original_type or derived_object
        (ie of second or third kind)
        """
        sem = self.semantics
        return z3.And(
            sem.true_at(leftarg, eval_world),
            sem.true_at(rightarg, eval_world)
        )

    def extended_verify(self, state, leftarg, rightarg, eval_world):
        x = z3.BitVec("ex_ver_x", self.semantics.N)
        y = z3.BitVec("ex_ver_y", self.semantics.N)
        return Exists(
            [x, y],
            z3.And(
                self.semantics.fusion(x, y) == state,
                self.semantics.extended_verify(x, leftarg, eval_world),
                self.semantics.extended_verify(y, rightarg, eval_world),
            ),
        )

    def find_verifiers(self, left_sent_obj, right_sent_obj, eval_world):
        """Takes sentences objects as arguments, finds their verifiers and
        falsifiers, and returns the verifiers and falsifiers for the operator"""
        Y_V = left_sent_obj.proposition.find_proposition()
        Z_V = right_sent_obj.proposition.find_proposition()
        return self.semantics.product(Y_V, Z_V)

    def print_method(self, sentence_obj, eval_world, indent_num, use_colors):
        """Prints the proposition for sentence_obj, increases the indentation
        by 1, and prints both of the arguments."""
        self.general_print(sentence_obj, eval_world, indent_num, use_colors)


class UniOrOperator(syntactic.Operator):
    """doc string place holder"""

    name = "\\univee"
    arity = 2

    def true_at(self, leftarg, rightarg, eval_world):
        """doc string place holder"""
        sem = self.semantics
        return z3.Or(
            sem.true_at(leftarg, eval_world), sem.true_at(rightarg, eval_world)
        )

    def extended_verify(self, state, leftarg, rightarg, eval_world):
        return z3.Or(
            self.semantics.extended_verify(state, leftarg, eval_world),
            self.semantics.extended_verify(state, rightarg, eval_world),
            # same as bilateral except no And in def
        )

    def find_verifiers(self, left_sent_obj, right_sent_obj, eval_world):
        Y_V = left_sent_obj.proposition.find_proposition()
        Z_V = right_sent_obj.proposition.find_proposition()
        return Y_V.union(Z_V)

    def print_method(self, sentence_obj, eval_world, indent_num, use_colors):
        """Prints the proposition for sentence_obj, increases the indentation
        by 1, and prints both of the arguments."""
        self.general_print(sentence_obj, eval_world, indent_num, use_colors)

class UniIdentityOperator(syntactic.Operator):
    """doc string place holder"""

    name = "\\uniequiv"
    arity = 2

    def true_at(self, leftarg, rightarg, eval_world):
        """doc string place holder"""
        N = self.semantics.N
        sem = self.semantics
        x = z3.BitVec("t_id_x", N)
        return z3.And(
            ForAll(
                x,
                z3.Implies(
                    sem.extended_verify(x, leftarg, eval_world),
                    sem.extended_verify(x, rightarg, eval_world)
                ),
            ),
            ForAll(
                x,
                z3.Implies(
                    sem.extended_verify(x, rightarg, eval_world),
                    sem.extended_verify(x, leftarg, eval_world)
                ),
            ),
        )

    def extended_verify(self, state, leftarg, rightarg, eval_world):
        return z3.And(
            state == self.semantics.null_bit,
            self.true_at(leftarg, rightarg, eval_world)
        )

    def find_verifiers(self, left_sent_obj, right_sent_obj, eval_world):
        Y_V = left_sent_obj.proposition.find_proposition()
        Z_V = right_sent_obj.proposition.find_proposition()
        return {self.semantics.null_bit} if Y_V == Z_V else set()
    
    def print_method(self, sentence_obj, eval_world, indent_num, use_colors):
        """Prints the proposition for sentence_obj, increases the indentation
        by 1, and prints both of the arguments."""
        self.general_print(sentence_obj, eval_world, indent_num, use_colors)


########################
### DEFAULT SETTINGS ###
########################

settings = {
    'N' : 3, # number of atomic states
    'possible' : False, # every sentence letter is possible
    'contingent' : True, # every sentence letter is contingent
    'non_empty' : True, # every sentence letter has a verifier
    'non_null' : False, # null_state does not verify sentence_letters
    'disjoint' : True, # sentence letters have disjoint subject-matters
    'fusion_closure' : False, # verifiers are closed under fusion
    'print_impossible' : True, # show impossible states
    'max_time' : 1, # max time before z3 will stop looking
}

# premises = []
# conclusions = []
# conclusions = ['\\exclude A']
# conclusions = ['A']
# conclusions = ['(A \\uniwedge B)']
# conclusions = ['(B \\uniwedge C)']

# premises = ['\\exclude (A \\univee B)']
# conclusions = ['(\\exclude A \\uniwedge \\exclude B)']

# premises = ['\\exclude (A \\uniwedge B)']
# conclusions = ['(\\exclude A \\univee \\exclude B)']

# premises = ['(A \\uniequiv B)']

# premises = []
# conclusions = ["(\\exclude (A \\uniwedge B) \\uniequiv (\\exclude A \\univee \\exclude B))"]
# settings['N'] = 4

# premises = []
# conclusions = ["(\\exclude (A \\univee B) \\uniequiv (\\exclude A \\uniwedge \\exclude B))"]

# premises = []
# conclusions = ["((A \\univee (B \\uniwedge C)) \\uniequiv ((A \\univee B) \\uniwedge (A \\univee C)))"]
# settings['N'] = 4

# premises = []
# conclusions = ["((A \\uniwedge (B \\univee C)) \\uniequiv ((A \\uniwedge B) \\univee (A \\uniwedge C)))"]

# premises = ['(A \\uniwedge (B \\univee C))']
# conclusions = ['((A \\univee B) \\uniwedge (A \\univee C))']

# premises = ['\\exclude (A \\uniwedge B)']
# conclusions = ['(\\exclude A \\univee \\exclude B)']

# NOTE: this is a versatile way to store examples for comparison later
# as in `example.py` 
EX_CM_1_premises = ['((A \\univee B) \\uniwedge (A \\univee C))']
EX_CM_1_conclusions = ['(A \\uniwedge (B \\univee C))']
EX_CM_1_example = [EX_CM_1_premises, EX_CM_1_conclusions]

# TODO: good to explain what each piece does

operators = syntactic.OperatorCollection(
    UniAndOperator,
    ExclusionOperator,
    UniOrOperator,
    UniIdentityOperator,
)

premises, conclusions = EX_CM_1_example

syntax = syntactic.Syntax(premises, conclusions, operators)

semantics = ChampollionSemantics(settings['N'])

model_constraints = model.ModelConstraints(
    settings,
    syntax,
    semantics,
    ChampollionProposition,
)

model_structure = model.ModelStructure(model_constraints)

model_structure.print_all()
