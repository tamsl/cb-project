from peep import Block

def definitions(bs):
    def_bs = {}
    for block in bs: 
      for  def_set in block:
        for def_register in def_set.checkDefinition(): 
          if def_register in def_bs:
            defs_bs[def_register].add(def_set.sid)
          else:
            id_set = set([def_set.sid])
            defs_bs[def_register] = id_set
    return defs

def head(expressions):
    heads = [0]
    tar = []
    for x, expression in enumerate(expressions[1:]):
        next = (x + 1)
        if expression.checkLabel() and next not in heads \
                and expression.name in tar:
            heads.append(next)
        if expression.checkJump():
            heads.append(x + 2)
            tar.append(expression[-1])
    heads.sort()
    return heads

def bbs_find(expressions):
    heads = head(expressions)
    len_expr = len(head(expressions)) - 1
    bs_hd = expressions[heads[-1]:]
    bs = []
    for x in range(len_expr):
        bs_expr = expressions[heads[i]:heads[x + 1]]
        bs.append(bb(bs_expr))
        heads = head(expressions)
    bs.append(bb(bs_hd))
    return bs

class bb(Block):
    def __init__(self, expressions=[]):
        Block.__init__(self, expressions)
        self.force = []
        self.forced = []
        self.edges1 = []
        self.edges2 = []
        self.setKill = set([])
        self.setGen = set([])

    def forcing(self, block):
        for1 = self.force
        for2 = self.forced
        if b not in for1:
            for1.append(b)
            for2.append(b)

    def edges(self, block):
        edge_i = self.edges1
        edge_o = self.edges2
        if b not in edge_o:
            edge_o.append(b)
            edge_i.append(b)

    def sets(self, definitions):
        handled_set = set()
        self.setKill = set()
        self.setGen = set()
        rev = reversed(self)
        defs = {}
        for def_register, id_expr in defs.iteritems():
            if def_register not in defs:
                count = id_expr
            else:
                count = id_expr - set([defs[def_register]])
            self.setKill |= count
        for def_set in rev:
          for def_register in def_set.checkDefinition():
                if def_register not in defs:
                    print 'Found def:', def_set
                    defs[def_register] = def_set.sid
                    self.setGen.add(def_set.sid)

