
# This file will test the astar.py file
import subprocess
import os 
import astar
import unittest
from unittest.mock import patch
import sys


class TestMyFunction(unittest.TestCase):
    @patch('builtins.input')
    def test_function(self, mock_input):
        result = astar.getRandomPuzzle()
        # self.assertEqual(result, "")

    @patch('builtins.input')
    
    
    def test_solvable(self, mock_input):
        result = astar.puzzleIsSolvable()
        # self.assertEqual(result, "")
        
        
# =====================================================================
#                               MAIN
# =====================================================================
if __name__ == '__main__':
    os.system('clear')
    # unittest.main()
    
    # initialFileString = "carlos-test"




    
    print("▊ TESTING INVERSIONS SOLVABILITY", end='')
    puzzle = astar.Node(state = [[1,2,4],[0,5,6],[8,3,7]])
    print(" ✅")
    print("▊ TESTING INVERSIONS SOLVABILITY", end='')
    puzzle = astar.Node(state = [[1,2,4],[0,5,6],[8,3,7]])
    print(" ✅")

    
    # puzzleInputSelection = 4
    
    # print("▊ TESTING PUZZLE NUMBER SELECTION")
    # try:
    #     for userSelection in range(puzzleInputSelection, 0, -1):
    #         print("▊ Testing user input: ", userSelection)
    #         try: 
    #             result = subprocess.run(
    #                 ["python3", "astar.py"],
    #                 input="f{userSelection}\n",
    #                 text=True,
    #                 capture_output=True
    #             )
    #             print("▊▊", "✅Succeeded" if result.returncode == 0 else "❌Failed")
    #         except:
    #             print("▊▊ ❌Failed")
    #             exit()
    # except: 
    #     print("▊INPUT PUZZLE NUMBER SELECTION FAILED")
    # print("▊ TESTING other")
    # print("▊ TESTING other")
    # print("▊ TESTING other")
    # print("▊ TESTING other")
    # # try:
    # #     print("▊ TESTING INPUT")
    # #     print("▊▊ Testing random input")
    # #     try: 
    # #         result = subprocess.run(
    # #             ["python3", "astar.py"], 
    # #             input="your input here\n", 
    # #             text=True, 
    # #             capture_output=True
    # #         )
    # #         print(result.stdout)
    # #     print("▊▊ Testing file input")
    # #     print("▊▊ Testing user input")
    # # except: 
    # #     print("▊INPUT FAILED")