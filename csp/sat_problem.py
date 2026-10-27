from typing import List, Set, Dict, Optional, Union, Any
from collections import defaultdict


class Variable:
    """
    A class to represent a variable in a CNF formula.
    A variable is the smallest building block in SAT formulas.
    This class contains useful methods for working with variables, 
    including methods for printing, checking equality,
    and hashing (for use in dictionaries).

    Attributes:
        name (str): The name of the variable.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Variable):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Literal:
    """
    A class to represent a literal in a CNF formula.
    A literal is a variable with a flag indicating whether it is negated or not.
    This class contains methods for checking if two literals are equal and a hash function (for use in dictionaries).

    Attributes:
        variable (Variable): The variable associated with the literal.
        is_positive (bool): A boolean indicating whether the literal is positive or negated.
    """

    def __init__(self, variable: Variable, is_positive: bool) -> None:
        self.variable = variable
        self.is_positive = is_positive

    def __str__(self) -> str:
        return f"{'~' if not self.is_positive else ''}{self.variable}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Literal):
            return False
        return self.variable == other.variable and self.is_positive == other.is_positive

    def __hash__(self) -> int:
        return hash((self.variable, self.is_positive))


class Clause:
    """
    A class to represent a clause in a CNF formula.
    Note: a clause is assumed to be a disjunction of literals.

    Attributes:
        literals (list): A list of literals in the clause.
        variables_set (set): A set of variables in the clause.
    """

    def __init__(self, literals: List[Literal]) -> None:
        # frozen sets used for hashing performance.
        # frozensets can be hashed and used as keys in a dictionary.
        self.literals = frozenset(literals)
        self.variables_set = frozenset(
            literal.variable for literal in literals)

    def __str__(self) -> str:
        return "(" + " Or ".join(map(str, self.literals)) + ")"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.literals)

    def get_variables(self) -> List[Variable]:
        """
        Get list of variables in clause

        Returns:
            List of variables in the clause
        """
        return list(self.variables_set)


class CNF:
    """
    A class to represent a CNF formula. A CNF formula is a conjunction of disjunctive clauses 
    (i.e., clauses with only ORs that are ANDed together).
    CNF formulae should be constructed using the add_clause method to add clauses (do not manually add to clauses set).

    Attributes:
        clauses (list): A list of clauses in the CNF formula.
        variables (dict): A dictionary mapping variables to the clauses they appear in.
        literal_clause_map (dict): A dictionary mapping literals to the clauses they appear in.
    """

    def __init__(self, clauses: Optional[List[Clause]] = None) -> None:
        self.clauses = set(clauses) if clauses else set()
        self.variables: Dict[Variable, Set[Clause]] = defaultdict(set)
        self.literal_clause_map: Dict[Literal, Set[Clause]] = defaultdict(set)

        for clause in self.clauses:
            for literal in clause.literals:
                self.variables[literal.variable].add(clause)
                self.literal_clause_map[literal].add(clause)

    def add_clause(self, clause: Clause) -> None:
        """
        Add clause to CNF and update appropriate attributes.

        Args:
            clause: The clause to add to the CNF
        """
        self.clauses.add(clause)
        for literal in clause.literals:
            self.variables[literal.variable].add(clause)
            self.literal_clause_map[literal].add(clause)

    def __str__(self) -> str:
        return " And ".join(map(str, self.clauses))


class Model:
    """
    A class to represent a model for a CNF formula.
    Contains methods for checking if a model satisfies a CNF formula,
    and methods for updating the model when a variable is assigned or "flipped".

    Attributes:
        CNF (CNF): The CNF formula that the model is for.
        variables (list): A list of variables in the CNF formula.
        assignments (dict): A dictionary mapping variables to their assigned values.
        unsatisfied_clauses (set): A set of clauses that are not satisfied by the current model.
        satisfied_literals (dict): A dictionary mapping clauses to the literals that satisfy them. (for internal use)
        flipped (list): A list of variables that have been flipped in the model. (for internal use)
    """

    def __init__(self, CNF: CNF) -> None:
        self.CNF = CNF
        self.variables = list(CNF.variables.keys())
        self.assignments: Dict[Variable, int] = {v: -1 for v in CNF.variables.keys()}
        self.unsatisfied_clauses: Set[Clause] = set(CNF.clauses)
        self.satisfied_literals: Dict[Clause, Set[Literal]] = defaultdict(set)
        self.flipped: List[Variable] = []


    def assign(self, variable: Variable, value: bool) -> None:
        """
        Assign a value to a variable in the model.
        
        Updates satisfied clauses in Model based on the new assignment.

        Args:
            variable: The variable to assign a value to
            value: The boolean value to assign to the variable
        """
        old_value = self.assignments[variable]
        self.assignments[variable] = int(value)
        self._update_clause_satisfaction(variable, old_value, int(value))

    def flip(self, variable: Variable) -> None:
        """
        Flip a variable (from True to False or from False to True).
        
        Updates satisfied clauses in Model based on the flipped assignment.

        Args:
            variable: The variable to flip
        """
        old_value = self.assignments[variable]
        new_value = 1 - old_value if old_value != -1 else 1
        self.assignments[variable] = new_value
        self.flipped.append(variable)
        self._update_clause_satisfaction(variable, old_value, new_value)

    def _update_clause_satisfaction(self, variable: Variable, old_value: int, new_value: int) -> None:
        """
        Update satisfied and unsatisfied clauses after variable assignment.
        
        This approach of tracking satisfied clauses significantly improves performance
        over checking clause satisfaction every time is_satisfied() is called.

        Args:
            variable: The variable that was flipped or assigned
            old_value: The old value of the variable
            new_value: The new value of the variable
        """
        positive_literal = Literal(variable, True)
        negative_literal = Literal(variable, False)

        affected_clauses = self.CNF.variables[variable]

        for clause in affected_clauses:
            # If it used to satisfy clause, remove literal from set of literals that was satisfying clause
            if old_value == 1:
                self.satisfied_literals[clause].discard(positive_literal)
            elif old_value == 0:
                self.satisfied_literals[clause].discard(negative_literal)

            # If it now satisfies the clause, add to set of literals that satisfy the clause
            if new_value == 1 and positive_literal in clause.literals:
                self.satisfied_literals[clause].add(positive_literal)
            elif new_value == 0 and negative_literal in clause.literals:
                self.satisfied_literals[clause].add(negative_literal)

            if self.satisfied_literals[clause]:
                self.unsatisfied_clauses.discard(clause)
            else:
                self.unsatisfied_clauses.add(clause)

    def is_satisfied(self) -> bool:
        """
        Check if the model satisfies the CNF formula.
        
        Returns:
            True if all clauses are satisfied, False otherwise
        """
        return not self.unsatisfied_clauses

    def change_in_num_clauses_sat_if_flipped(self, var: Variable) -> int:
        """
        Calculate the change in number of satisfied clauses if variable is flipped.
        
        Args:
            var: The variable to consider flipping
            
        Returns:
            The change in number of satisfied clauses (positive means more satisfied)
        """
        current_value = self.assignments[var]
        flipped_value = 1 - current_value if current_value != -1 else 1

        positive_literal = Literal(var, True)
        negative_literal = Literal(var, False)

        affected_clauses = self.CNF.variables[var]
        delta = 0

        for clause in affected_clauses:
            # Was it previously satisfied?
            was_satisfied = bool(self.satisfied_literals[clause])
            
            # Will it be satisfied after flipping var?
            # Need to check if OTHER variables still satisfy it
            would_be_satisfied = False
            
            # First check if other literals still satisfy it
            for lit in self.satisfied_literals[clause]:
                if lit.variable != var:  # Other variables still satisfy it
                    would_be_satisfied = True
                    break
                    
            # Then check if the flipped value of var would satisfy it
            if not would_be_satisfied:
                if flipped_value == 1 and positive_literal in clause.literals:
                    would_be_satisfied = True
                elif flipped_value == 0 and negative_literal in clause.literals:
                    would_be_satisfied = True

            if not was_satisfied and would_be_satisfied:
                delta += 1
            elif was_satisfied and not would_be_satisfied:
                delta -= 1

        return delta

    def get_unsatisfied_clauses(self) -> List[Clause]:
        """
        Output:
            list: A list of unsatisfied clauses in the model.
        """
        return list(self.unsatisfied_clauses)

    def check_sat_clauses(self) -> int:
        """
        Check the number of satisfied clauses for verification purposes.
        
        This method is used by staff to verify the backend is running correctly.
        
        Returns:
            Number of satisfied clauses
        """
        num_sat_clauses = 0
        for clause in self.CNF.clauses:
            for literal in clause.literals:
                variable = literal.variable
                if (self.assignments[variable] == 1 and literal.is_positive) or \
                   (self.assignments[variable] == 0 and not literal.is_positive):
                    num_sat_clauses += 1
                    break

        return num_sat_clauses
            


    def __str__(self) -> str:
        return str(self.assignments)


if __name__ == "__main__":
    # Example usage
    cnf = CNF()
    cnf.add_clause(
        Clause([Literal(Variable("A"), True), Literal(Variable("B"), True)]))
    cnf.add_clause(
        Clause([Literal(Variable("A"), False), Literal(Variable("C"), True)]))
    cnf.add_clause(
        Clause([Literal(Variable("B"), False), Literal(Variable("C"), False)]))

    print(cnf)

    my_model = Model(cnf)
    print("Current Assignments", my_model)
    print("Is satisfied?", my_model.is_satisfied())
    print("Num satisfied", my_model.check_sat_clauses())
    print("Unsatisfied clauses:", my_model.get_unsatisfied_clauses())

    my_model.assign(Variable("B"), False)
    print("Current Assignments", my_model)
    print("Is satisfied?", my_model.is_satisfied())
    print("Num satisfied", my_model.check_sat_clauses())
    print("Unsatisfied clauses:", my_model.get_unsatisfied_clauses())

    my_model.assign(Variable("C"), True)
    my_model.assign(Variable("A"), True)
    print("Current Assignments", my_model)
    print("Is satisfied?", my_model.is_satisfied())
    print("Num satisfied", my_model.check_sat_clauses())
    print("Unsatisfied clauses:", my_model.get_unsatisfied_clauses())