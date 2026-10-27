import pandas as pd
import random
import unittest

from bayesian_network import BayesianNetwork, CPT
from heart_disease_network import create_heart_disease_network
from generate_car_dataset import create_car_diagnosis_network

class TestHeartDiseaseNetwork(unittest.TestCase):
    def test_get_probability_no_parents(self):
        
        cpt = CPT(node="Smoking", parents=[], table={"Yes": 0.2, "No": 0.8})
        self.assertAlmostEqual(cpt.get_probability("Yes"), 0.2)
        self.assertAlmostEqual(cpt.get_probability("No"), 0.8)
        self.assertAlmostEqual(cpt.get_probability("Maybe"), 0.0)  # Non-existent outcome
        
    def test_network_structure(self):
        network = create_heart_disease_network()
        
        # Correct number of CPTs
        self.assertEqual(len(network.cpts), 6)
        self.assertIn("Smoking", network.cpts)
        self.assertIn("Exercise", network.cpts)
        self.assertIn("BloodPressure", network.cpts)
        self.assertIn("Cholesterol", network.cpts)
        self.assertIn("HeartDiseaseRisk", network.cpts)
        self.assertIn("ECGResults", network.cpts)

        # Correct Format and values for Smoking (no parents)
        self.assertEqual(network.cpts["Smoking"].node, "Smoking")
        self.assertEqual(network.cpts["Smoking"].table, {"Yes": 0.20, "No": 0.80})
        self.assertEqual(network.cpts["Smoking"].parents, [])

        # Correct Format for node with parents
        self.assertEqual(network.cpts["BloodPressure"].node, "BloodPressure")
        self.assertEqual(network.cpts["BloodPressure"].parents, ["Smoking", "Exercise"])
        self.assertEqual(network.cpts["BloodPressure"].table, {
            ("No", "High"): {"High": 0.15, "Normal": 0.85},
            ("No", "Low"): {"High": 0.30, "Normal": 0.70},
            ("Yes", "High"): {"High": 0.25, "Normal": 0.75},
            ("Yes", "Low"): {"High": 0.50, "Normal": 0.50}
        })
    
    def test_estimate_probability(self):
        network = create_heart_disease_network()
        
        # P(Smoking=Yes) (Test with no evidence)
        self.assertAlmostEqual(network.estimate_probability("Smoking", "Yes", num_samples=10000), 0.20, delta=0.015)

        # P(HeartDiseaseRisk=High | Smoking=Yes, BloodPressure=Normal, Cholesterol=Normal) = 0.12
        self.assertAlmostEqual(network.estimate_probability("HeartDiseaseRisk", "High", evidence={"Smoking": "Yes", "BloodPressure": "Normal", "Cholesterol": "Normal"}, num_samples=100000), 0.12, delta=0.02)
        


class TestBayesianNetwork(unittest.TestCase):

    def test_cpt_get_probability_root(self):
        cpt = CPT(node="Smoking", parents=[], table={"Yes": 0.2, "No": 0.8})
        self.assertAlmostEqual(cpt.get_probability("Yes"), 0.2)
        # providing parent_values to a root CPT should raise ValueError 
        with self.assertRaises(ValueError):
            cpt.get_probability("Yes", {"SomeParent": "X"})

    def test_cpt_get_probability_with_parents(self):
        table = {("a", "b"): {"T": 0.6, "F": 0.4}}
        cpt = CPT(node="Child", parents=["P1", "P2"], table=table)
        prob = cpt.get_probability("T", {"P1": "a", "P2": "b"})
        self.assertAlmostEqual(prob, 0.6)
        # incomplete parent_values length -> ValueError
        with self.assertRaises(ValueError):
            cpt.get_probability("T", {"P1": "a"})

    def test_build_cpt_from_data_no_parents(self):
        bn = BayesianNetwork()
        bn.add_node("A", ["T", "F"])
        df = pd.DataFrame({"A": ["T", "F", "T"]})
        cpt = bn.build_cpt_from_data("A", df)
        self.assertEqual(cpt.node, "A")
        self.assertEqual(cpt.parents, [])
        self.assertAlmostEqual(cpt.table["T"], 2/3)
        self.assertAlmostEqual(cpt.table["F"], 1/3)

    def test_build_cpt_from_data_with_parent(self):
        bn = BayesianNetwork()
        bn.add_node("P", ["x", "y"])
        bn.add_node("C", ["1", "0"])
        bn.add_edge("P", "C")
        df = pd.DataFrame({"P": ["x", "x", "y"], "C": ["1", "1", "0"]})
        cpt = bn.build_cpt_from_data("C", df)
        self.assertEqual(cpt.node, "C")
        self.assertEqual(cpt.parents, ["P"])
        self.assertAlmostEqual(cpt.table[("x",)]["1"], 1.0)
        self.assertAlmostEqual(cpt.table[("y",)]["0"], 1.0)

    def test_estimate_probability_basic_prior(self):
        random.seed(42)
        bn = BayesianNetwork()
        bn.add_node("A", ["Yes", "No"])
        bn.cpts["A"] = CPT(node="A", parents=[], table={"Yes": 0.7, "No": 0.3})
        bn.node_domains["A"] = {"Yes", "No"}
        # with many samples estimate should be close to 0.7
        est = bn.estimate_probability("A", "Yes", evidence=None, num_samples=2000)
        self.assertAlmostEqual(est, 0.7, places=2)

    def test_estimate_probability_with_evidence_no_match(self):
        random.seed(1)
        bn = BayesianNetwork()
        # simple two-node network where evidence is impossible
        bn.add_node("A", ["X", "Y"])
        bn.add_node("B", ["u", "v"])
        bn.cpts["A"] = CPT(node="A", parents=[], table={"X": 1.0, "Y": 0.0})
        bn.cpts["B"] = CPT(node="B", parents=[], table={"u": 0.5, "v": 0.5})
        bn.node_domains["A"] = {"X", "Y"}
        bn.node_domains["B"] = {"u", "v"}
        est = bn.estimate_probability("B", "u", evidence={"A": "Y"}, num_samples=500)
        self.assertEqual(est, 0.0)

if __name__ == '__main__':
    unittest.main()