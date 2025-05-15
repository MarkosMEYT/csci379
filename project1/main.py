###=================================================
# This file is where you need to create a plan to reach the goal state from the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================

from state import State

class Plan:

    def __init__(self, initial_state, goal_state):
        """
        Initialize initial state and goal state
        :param initial_state: list of blocks in the initial state
        :type initial_state: list of block.Block objects
        :param goal_state: list of blocks in the goal state
        :type initial_state: list of block.Block objects
        """
        self.initial_state = initial_state
        self.goal_state = goal_state

    def putdown(self, block1):
        """
        Operator to put the block on the table
        :param block1: block1 to put on the table
        :type block1: Object of block.Block
        :return: None
        """

        # get table object from initial state
        table = State.find(self.initial_state, "table")

        if block1.air:
            block1.on = table
            block1.clear = True

    def unstack(self, block1, block2):
        """
        Operator to unstack block1 from block 2
        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """

        # if block1 is clear safe to unstack
        if block1.clear:

            # block1 should be in air
            # block1 should not be on block2
            # set block2 to clear (because block1 is in air)
            block1.clear = False
            block1.air = True
            block1.on = None

            block2.clear = True
    
    def pickup(self, block1):
        """
        Operator to pickup the block from the table
        :param block1: block1 to pickup from the table
        :type block1: Object of block.Block
        :return: None
        """

        if not block1.air and block1.clear:
            block1.air = True 
            block1.clear = False
            block1.on = None

    def stack(self, block1, block2):
        """
        Operator to stack block1 on block 2
        :param block1: block1 to stack on block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """
        
        if block1.air and block2.clear and block2.type != 2:
            block2.clear = False
            block1.air = False
            block1.clear = True
            block1.on = block2

    def move(self, block1, block2):
        """
        Dummy operator
        :param block1: block1 move to block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """
        pass


    def plan(self):
        goal_down = {}
        goal_up = {}
        goal_up['table'] = []
        for block in self.goal_state:
            if block.on != None:
                if str(block.on) == 'table':
                    goal_up['table'].append(str(block))
                else:
                    goal_up[str(block.on)] = str(block)
                goal_down[str(block)] = str(block.on)

        #move them to table
        moved = True
        while moved == True:
            moved = False
            for blocks in self.initial_state:
                block = State.find(self.initial_state, str(blocks))
                if block.type == 3:
                    continue
                if block.clear == True and block.on.type != 3:
                    if goal_down[str(block)] == 'table':
                        goal_down.pop(str(block))
                    action = f"unstack{block, block.on}"
                    self.unstack(block, block.on)
                    State.display(self.initial_state, message=action)
                    # print the state
                    action = f"putdown({block})"
                    self.putdown(block)
                    State.display(self.initial_state, message=action)
                    # print the state
                    moved = True
                    continue
                    
        for block in goal_up['table']:
            cur = block
            while goal_up.get(cur, False):
                current = State.find(self.initial_state, cur)
                move = State.find(self.initial_state, goal_up[cur])
                action = f"pickup({move})"
                self.pickup(move)
                State.display(self.initial_state, message=action)
                # print the state
                action = f"stack{move, current}"
                self.stack(move, current)
                # print the state
                State.display(self.initial_state, message=action)
                cur = goal_up[cur]
            




if __name__ == "__main__":

    # get the initial state
    initial_state = State()
    initial_state_blocks = initial_state.create_state_from_file("input.txt")

    #display initial state
    State.display(initial_state_blocks, message="Initial State")

    # get the goal state
    goal_state = State()
    goal_state_blocks = goal_state.create_state_from_file("goal.txt")

    #display goal state
    State.display(goal_state_blocks, message="Goal State")

    """
    Sample Plan
    """

    p = Plan(initial_state_blocks, goal_state_blocks)
    p.plan()
    
