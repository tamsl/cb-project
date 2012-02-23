from peep import Block

# Choosing head expressions considering a jump target
def head(expressions):
  heads = [0]
  tar = []
  for x, expr in enumerate(expressions[1:]):
    next = (x + 1)
    # Jump appended
    if expr.checkLabel() and next not in heads \
      and expr.name in tar:
      heads.append(next)
    # Target saved of expression
    if expr.checkJump():
      heads.append(x + 2)
      tar.append(expr[-1])
  heads.sort()
  return heads

# Finding basic blocks 
def bbs_find(expressions):
  heads = head(expressions)
  len_expr = len(head(expressions)) - 1
  bs_hd = expressions[heads[-1]:]
  bs = []
  # By means of a list of expressions
  for x in range(len_expr):
    bs_expr = expressions[heads[x]:heads[x + 1]]
    bs.append(bb(bs_expr))
    heads = head(expressions)
  bs.append(bb(bs_hd))
  return bs

# Class of basic blocks
class bb(Block):
  def __init__(self, expressions=[]):
    Block.__init__(self, expressions)
    self.force = []
    self.forced = []
    self.edges1 = []
    self.edges2 = []
    self.setKill = set([])
    self.setGen = set([])

  # The handling block
  def forcing(self, block):
    for1 = self.force
    for2 = self.forced
    if b not in for1:
      for1.append(b)
      for2.append(b)

  # Creating edges
  def edges(self, block):
    edge_i = self.edges1
    edge_o = self.edges2
    if b not in edge_o:
      edge_o.append(b)
      edge_i.append(b)

  # Producing kill and gen respectively
  def sets(self, definitions):
    handled_set = set()
    self.setKill = set()
    self.setGen = set()
    rev = reversed(self)
    defs = {}
    # Kill
    for id_expr, def_register in defs.iteritems():
      if def_register not in defs:
        c = id_expr
      else:
        c = id_expr - set([defs[def_register]])
      self.setKill |= c
    # Gen
    for ex in rev:
      for def_register in ex.checkDefinition():
        if def_register not in defs:
          defs[def_register] = ex.sid
          self.setGen.add(ex.sid)
