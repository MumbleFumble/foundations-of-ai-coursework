import unittest
from typing import Dict, Any

from energy_planning import build_and_solve_model


class EnergyTests(unittest.TestCase):
    """
    Test cases for energy planning optimization formulations.
    """

    def test_wind_and_solar(self) -> None:
        # Should pass if only wind and solar are used (not storage)
        self.test_wind_and_solar_1()
        self.test_wind_and_solar_2()
        self.test_wind_and_solar_3()

    def test_wind_and_solar_1(self) -> None:
        args: Dict[str, Any] = {}
        args["wind_cf"] = [1, 1, 0, 0]
        args["solar_cf"] = [0, 0, 1, 1]
        args["solar_cost"] = 1
        args["wind_cost"] = 2
        args["li_ion_cost"] = 1000
        args["metal_air_cost"] = 1000
        args["demand"] = [5, 5, 5, 5]
        args["battery_efficiency"] = 1.0
        args["metal_air_efficiency"] = 1.0

        results = build_and_solve_model(args)
        cost = results["total_cost"]
        wind_capacity = results["wind_capacity"]
        solar_capacity = results["solar_capacity"]

        # 5 units of wind at $2 each, 5 units of solar at $1 each
        self.assertAlmostEqual(wind_capacity, 5, 3)
        self.assertAlmostEqual(solar_capacity, 5, 3)
        self.assertAlmostEqual(cost, 15, 3)

    def test_wind_and_solar_2(self) -> None:
        args: Dict[str, Any] = {}
        args["wind_cf"] = [1, 1, 1, 1]
        args["solar_cf"] = [0, 0, 1, 1]
        args["solar_cost"] = 1
        args["wind_cost"] = 2
        args["li_ion_cost"] = 1000
        args["metal_air_cost"] = 1000
        args["demand"] = [4, 4, 4, 4]
        args["battery_efficiency"] = 1.0
        args["metal_air_efficiency"] = 1.0

        results = build_and_solve_model(args)
        cost = results["total_cost"]
        wind_capacity = results["wind_capacity"]
        solar_capacity = results["solar_capacity"]
        # Solar is not used
        self.assertAlmostEqual(wind_capacity, 4, 3)
        self.assertAlmostEqual(solar_capacity, 0, 3)
        self.assertAlmostEqual(cost, 8)

    def test_wind_and_solar_3(self) -> None:
        args: Dict[str, Any] = {}
        args["wind_cf"] = [1, 1, 0.5, 0.5]
        args["solar_cf"] = [0, 0, 1, 1]
        args["solar_cost"] = 1
        args["wind_cost"] = 2
        args["li_ion_cost"] = 1000
        args["metal_air_cost"] = 1000
        args["demand"] = [4, 4, 4, 4]
        args["battery_efficiency"] = 1.0
        args["metal_air_efficiency"] = 1.0


        results = build_and_solve_model(args)
        cost = results["total_cost"]
        wind_capacity = results["wind_capacity"]
        solar_capacity = results["solar_capacity"]

        # Solar is cheaper than wind for the last two hours
        self.assertAlmostEqual(wind_capacity, 4, 3)
        self.assertAlmostEqual(solar_capacity, 2, 3)
        self.assertAlmostEqual(cost, 10, 3)



    def test_zero_demand_zero_cost(self) -> None:
        """
        If there is no demand, model should build nothing and cost 0.
        """
        args: Dict[str, Any] = {}
        args["wind_cf"] = [1, 1, 1, 1]
        args["solar_cf"] = [1, 1, 1, 1]
        args["solar_cost"] = 1
        args["wind_cost"] = 1
        args["li_ion_cost"] = 1
        args["metal_air_cost"] = 1
        args["demand"] = [0, 0, 0, 0]
        args["battery_efficiency"] = 1.0
        args["metal_air_efficiency"] = 1.0

        results = build_and_solve_model(args)
        self.assertEqual(results["solar_capacity"], 0)
        self.assertEqual(results["wind_capacity"], 0)
        self.assertEqual(results["battery_capacity"], 0)
        self.assertEqual(results["metal_air_capacity"], 0)
        self.assertEqual(results["total_cost"], 0)



    def test_constant_demand_balanced_generation(self) -> None:
        """
        If wind and solar both constant, model should choose cheaper one.
        """
        args: Dict[str, Any] = {}
        args["wind_cf"] = [1, 1, 1, 1]
        args["solar_cf"] = [1, 1, 1, 1]
        args["solar_cost"] = 1
        args["wind_cost"] = 2
        args["li_ion_cost"] = 1000
        args["metal_air_cost"] = 1000
        args["demand"] = [10, 10, 10, 10]
        args["battery_efficiency"] = 1.0
        args["metal_air_efficiency"] = 1.0

        results = build_and_solve_model(args)
        self.assertAlmostEqual(results["solar_capacity"], 10, 2)
        self.assertAlmostEqual(results["wind_capacity"], 0, 2)
        self.assertLess(results["total_cost"], 20000)


    def test_storage_always_required(self) -> None:
        """
        Construct a scenario where generation and demand never overlap in time,
        so storage must exist no matter how large generation capacity is.
        """
        args: Dict[str, Any] = {}

  
        args["wind_cf"] = [1, 1, 0, 0, 0, 0]
        args["solar_cf"] = [0, 0, 1, 1, 0, 0]
        args["demand"] = [0, 0, 0, 0, 2, 2]  

        args["solar_cost"] = 1
        args["wind_cost"] = 1
        args["li_ion_cost"] = 0.1
        args["metal_air_cost"] = 0.1
        args["battery_efficiency"] = 1.0
        args["metal_air_efficiency"] = 1.0

        results = build_and_solve_model(args)

        total_storage = results["battery_capacity"] + results["metal_air_capacity"]
        self.assertGreater(total_storage, 0, "Storage should be required to meet delayed demand")

        total_gen = results["solar_capacity"] + results["wind_capacity"]
        self.assertGreater(total_gen, 0, "Model must build generation to charge storage")

        self.assertGreater(results["total_cost"], 0)
        self.assertLess(results["total_cost"], 1e9)

if __name__ == "__main__":
    unittest.main()