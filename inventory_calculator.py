import Inventory
import Stack
import sys

if __name__ == "__main__":
    #inv = Inventory.Inventory()
    stk = Stack.Stack("tile19/StackHeight.csv")
    stk.plot_holeblock()




    config = "s101s"
    mcpsum = 48.5+48.5
    tolerance = [-1, -2]
    stk.solve_stack(inv, mcpsum, "s101s", tolerance)

