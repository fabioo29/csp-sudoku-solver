<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Solving sudoku with Artificial Intelligence</h3>

  <p align="center">
    Problem Solving Challenges :: Constraint Satisfaction Problems :: Fundamentals of AI 
    <br />
  </p>
  </br>
  <p align="center">
    <img src="images/start.png" alt="original wumpus world map" width="270" height="235" />
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li><a href="#about">About</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#simulation">Simulation</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About

|            Algorithm metrics (1/2)            |              Solved sudoku board (2/2)               |
| :-------------------------------------------: | :--------------------------------------------------: |
| ![Product Name Screen Shot](images/solve.png) | ![Product Name Screen Shot](images/solved_stage.png) |

<div style="text-align: justify">
  
**Motivation**: Develop a Sudoku Resolver using CSP. Try to build the CSP system as generic as possible. Note that constrains can be defined in code, or described as rules. Try to find the best solution for easily tweaking the constrains by a standard user.

**Implementation**: For this project we started to test a simple backtracking algorithm to check its performance on this environment. A backtracking algorithm is a recursive algorithm that tries to find a solution by exploring all possible combinations of values. The algorithm is called backtracking because it backtracks when it finds a solution, and tries to find a solution for the next value.
The time complexity of backtracking algorithm is exponential so it's quite expensive to solve a sudoku using this kind of algorithm.

In order to improve it we decided to implement CSP (Constraint Satisfaction Problems) technique into the backtracking algorithm. The CSP is a generalization of the problem of finding a solution to a problem with constraints. In this case we are trying to solve a sudoku board. The sudoku board is a 9x9 matrix of numbers from 1 to 9. The goal is to fill the board with numbers from 1 to 9 in such a way that each row, column and 3x3 box contains each number exactly once. So our constraint is that each row, column and 3x3 box must contain each number from 1 to 9.

To implement the CSP we defined the domain (possible remaining values) of each cell. The domain of each cell is a set of numbers from 1 to 9. The domain of a cell is the set of possible values that can be assigned to that cell.

This feature can improve the performance of the backtracking algorithm because before changing the value of a cell we can check if the new value is valid before the actual change just looking at the domain of the cell.

**_Tested with_** backtracking algorithm and CSP based backtracking algorithm.

**_Built With_** Python3.6 and tkinter package for the interface itself.

<!-- TESTING -->

## Testing

**Backtracking algorithm**

<!-- create a center table of metrics fro each algorithm-->
<table align="center" border="1" cellpadding="5" cellspacing="0" style="width:80%">
  <tr>
    <th>Board</th>
    <th>Iterations</th>
    <th>Solving time</th>
  </tr>
  <tr>
    <td>Clean Board</td>
    <td>391</td>
    <td>0.016 seconds</td>
  </tr>
  <tr>
    <td>Easy Board</td>
    <td>105</td>
    <td>0.005 seconds</td>
  </tr>
  <tr>
    <td>Medium Board</td>
    <td>3047</td>
    <td>0.107 seconds</td>
  </tr>
  <tr>
    <td>Hard Board</td>
    <td>103922</td>
    <td>3.843 seconds</td>
  </tr>
</table>

**CSP based backtracking algorithm**

<!-- create a center table of metrics fro each algorithm-->
<table align="center" border="1" cellpadding="5" cellspacing="0" style="width:80%">
  <tr>
    <th>Board</th>
    <th>Iterations</th>
    <th>Solving time</th>
  </tr>
  <tr>
    <td>Clean Board</td>
    <td>240</td>
    <td>0.907 seconds</td>
  </tr>
  <tr>
    <td>Easy Board</td>
    <td>65</td>
    <td>0.095 seconds</td>
  </tr>
  <tr>
    <td>Medium Board</td>
    <td>1443</td>
    <td>3.017 seconds</td>
  </tr>
  <tr>
    <td>Hard Board</td>
    <td>30391</td>
    <td>60.830 seconds</td>
  </tr>
</table>

After the tests we found out that the CSP based backtracking algorithm is not the best algorithm to solve sudoku boards if we need speed but, it is the most memory efficient algorithm as we can see through the iterations.

<!-- SIMULATION -->

## Simulation

```python
pip install -r requirements.txt # pygame and pyswip
python main.py # run the GUI
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

Fábio Oliveira - [LinkedIn](https://www.linkedin.com/in/fabioo29/) - fabiodiogo29@gmail.com

Project Link: [https://github.com/fabioo29/ai-wumpus-world](https://github.com/fabioo29/ai-wumpus-world)  
Project built as a Msc. Applied Artificial Intelligence Student.
