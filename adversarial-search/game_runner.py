import argparse
from cProfile import run
import time
from typing import List, Optional, Union

from adversarial_search_problem import AdversarialSearchProblem, GameUI
from adversarial_search import minimax, alpha_beta
from asps.ttt_problem import TTTProblem, TTTUI
from asps.connect_four_problem import ConnectFourProblem, Connect4GUI
from asps.heuristic_ttt_problem import HeuristicTTTProblem
from asps.heuristic_connect_four import HeuristicConnectFourProblem
from agents import MinimaxAgent, AlphaBetaAgent, GameAgent


########################################################
# You should not have to modify the code below,        #
# but it may be useful to see how games are simulated. #
########################################################


def run_game(asp: AdversarialSearchProblem, agents: List[Optional[GameAgent]], game_ui: Optional[GameUI] = None) -> Union[int, float]:
    """
    Runs a single game between the specified agents.
    
    Args:
        asp: An instance of the game separate from the agents to work from
        agents: A list of agents which determines the algorithm used for each player
        game_ui: Optional GameUI that visualizes ASPs and allows for direct input
                in place of a bot that is None
    
    Returns:
        The evaluation of the terminal state from player 0's perspective
    """

    # Ensure game_ui is present if a bot is None:
    if not game_ui and any(agent is None for agent in agents):
        raise ValueError(
            "A GameUI instance must be provided if any bot is None.")

    state = asp.get_start_state()
    if game_ui:
        game_ui.update_state(state)
        game_ui.render()

    while not (asp.is_terminal_state(state)):
        curr_bot = agents[state.player_to_move()]

        # Obtain decision from the bot itself, or from GameUI if bot is None:
        if curr_bot:
            decision, stats = curr_bot.get_move(state)
            # If the bot tries to make an invalid action,
            # returns any valid action:
            available_actions = asp.get_available_actions(state)
            if decision not in available_actions:
                decision = available_actions.pop()
        else:
            if game_ui:
                decision = game_ui.get_user_input_action()
        assert(decision is not None)
        result_state = asp.transition(state, decision)
        asp.set_start_state(result_state)
        state = result_state

        if game_ui:
            game_ui.update_state(state)
            game_ui.render()

    return asp.get_result(asp.get_start_state())


def main() -> None:
    """
    Main function that parses command line arguments and runs the game.
    
    Handles game setup, agent configuration, and game execution based on
    command line parameters.
    """
    # Setup parser; Default behavior is Tic-Tac-Toe, minimax, player vs. bot.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--game", choices=["ttt", "connect4"], default="ttt")
    parser.add_argument("--dimension", type=int, default=None)
    parser.add_argument(
        "--player1", choices=["self", "minimax", "ab"], default="self"
    )
    parser.add_argument(
        "--player2", choices=["self", "minimax", "ab"], default="minimax"
    )
    parser.add_argument("--cutoff", type=int, default=float('inf'))

    args = parser.parse_args()
    player_args = [args.player1, args.player2]

    game = args.game

    if game == 'ttt':
        if args.dimension is not None:
            if args.dimension < 3:
                parser.error("--dimension must be at least 3 for Tic-Tac-Toe")
            heuristic_problem = HeuristicTTTProblem(dim=args.dimension)
            game_ui = TTTUI(heuristic_problem)
        else:
            heuristic_problem = HeuristicTTTProblem()
            game_ui = TTTUI(heuristic_problem)

    elif game == 'connect4':
        if args.dimension is not None:
            if args.dimension < 3:
                parser.error("--dimension must be at least 4 for Connect Four")
            heuristic_problem = HeuristicConnectFourProblem(dims=(args.dimension, args.dimension))
            game_ui = Connect4GUI(heuristic_problem)
        else:
            heuristic_problem = HeuristicConnectFourProblem()
            game_ui = Connect4GUI(heuristic_problem)
    else:
        parser.error("--game must be a valid game: ttt or connect4")

    agents = [None, None]
    for i, player in enumerate(player_args):
        if player == 'minimax':
            agents[i] = MinimaxAgent(
                heuristic_problem, cutoff_depth=args.cutoff)

        elif player == 'ab':
            agents[i] = AlphaBetaAgent(
                heuristic_problem, cutoff_depth=args.cutoff)

        elif player == 'self':
            pass

        else:
            parser.error(
                f"--player{i+1} must be a valid algorithm: minimax or ab")

    # Run the game and print the final scores:
    print(f"PLAYERS: {args.player1} (P1) vs. {args.player2} (P2)")
    p1_score = run_game(heuristic_problem, agents, game_ui)
    p2_score = -1 * p1_score
    print(f"P1 score: {p1_score}, P2 score: {p2_score}")

    # time.sleep(10)  # (uncomment to keep GUI visible after end of game)


if __name__ == "__main__":
    main()