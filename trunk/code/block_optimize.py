from copy import copy
from statement import Block

class BasicBlock(Block):
    def __init__(self, statements=[]):
        Block.__init__(self, statements)
        self.edges_to = []
        self.edges_from = []

        self.dominates = []
        self.dominated_by = []
        self.in_set = set([])
        self.out_set = set([])
        self.gen_set = set([])
        self.kill_set = set([])

    def add_edge_to(self, block):
        if block not in self.edges_to:
            self.edges_to.append(block)
            block.edges_from.append(self)

    def set_dominates(self, block):
        if block not in self.dominates:
            self.dominates.append(block)
            block.dominated_by.append(self)

    def create_gen_kill(self, defs):
        used = set()
        self_defs = {}

        # Get the last of each definition series and put in in the `def' set
        self.gen_set = set()

        for s in reversed(self):
            for reg in s.get_def():
                if reg not in self_defs:
                    print 'Found def:', s
                    self_defs[reg] = s.sid
                    self.gen_set.add(s.sid)

        # Generate kill set
        self.kill_set = set()

        for reg, statement_ids in defs.iteritems():
            if reg in self_defs:
                add = statement_ids - set([self_defs[reg]])
            else:
                add = statement_ids

            self.kill_set |= add

def defs(blocks):
    # Collect definitions of all registers
    defs = {}

    for b in blocks:
        for s in b:
            for reg in s.get_def():
                if reg not in defs:
                    defs[reg] = set([s.sid])
                else:
                    defs[reg].add(s.sid)

    return defs

def find_basic_blocks(statements):
    """Divide a statement list into basic blocks. Returns a list of basic
    blocks, which are also statement lists."""
    leaders = find_leaders(statements)
    blocks = []

    for i in range(len(leaders) - 1):
        blocks.append(BasicBlock(statements[leaders[i]:leaders[i + 1]]))

    blocks.append(BasicBlock(statements[leaders[-1]:]))

    return blocks
