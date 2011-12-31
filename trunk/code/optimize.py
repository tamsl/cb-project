from math import log
import re
from block_optimize import bbs_find

def remove(opt, expressions):
  # Original sequence | Replacement
  # mov $regA, $regB  | --- (remove)
  # (with $regA == $regB)
  if opt.checkCommand('opt'):
    if opt[0] == opt[1]:
      expressions.substitute(1, [])
      return 1

  # Original sequence       | Replacement
  # mov $regA, $regB        | instr $regA, $regB,...
  # instr $regA, $regA, ... |
def replace(opt, expressions):
  if opt.checkCommand('opt'):
    ex = expressions.readExpressionOffset()
    if ex and ((ex[0] and ex[1]) == opt[0]) and len(ex) > 1:
      ex[1] = opt[1]
      expressions.substitute(2, [ex])
      return 1

  # Original sequence | Replacement
  # instr $regA, ...  | instr $4, ...
  # mov $4, $regA     | jal XX
  # jal XX            |
def jal(opt, expressions):
  if opt.checkCommand() and len(opt) > 0:
    ex = expressions.readExpressionOffset(2)
    if len(ex) > 1:
      instr, jal = ex
      if opt[0] == instr[1] and instr.checkCommand('move'):
        if re.match('^\$[4-7]$', instr[0]) and jal.checkCommand('jal'):
          opt[0] = instr[0]
          expressions.substitute(2, [opt])
          return 1

  # Original sequence | Replacement
  # mov $regA, $regB  | move $regA, $regB
  # mov $regB, $regA  |
def move(opt, expressions):
  if opt.checkCommand('move'):
    mov = expressions.readExpressionOffset()
    if mov.checkCommand('move') and opt[1] == mov[0] and opt[0] == mov[1] :
      expressions.substitute(2, [opt])
      return 1

# Original sequence  | Replacement
#   beq/bne ..., $Lx |   bne/beq ..., $Ly
#   j $Ly            | $Lx:
# $Lx:
def beq_bne(expressions):
  prev = -1
  while prev != len(expressions):
    prev = len(expressions)
    while not expressions.checkPosition():
      e = expressions.readExpression()
      if e.checkCommand('beq', 'bne'):
        ex = expressions.readExpressionOffset(2)
        if len(ex) == 2:
          j, i = ex
          if j.checkCommand('j') and i.checkLabel(e[2]):
            if e.checkCommand('beq'):
              e.name = 'bne'
            else:
              e.name = 'beq'
            e[2] = j[0]
            expressions.substitute(3, [e, i])

# Original sequence | Replacement
# sw $regA, XX      |  sw $regA, XX
# ld $regA, XX
def optimize_ld(opt, expressions):
  if opt.checkCommand('sw'):
    load = expressions.readExpressionOffset()
    if load.args == opt.args and load.checkCommand('lw'):
      expressions.substitute(2, [opt])
      return 1

# Original sequence    | Replacement
# add $regA, $regA, X  | lw ..., X($regA)
# lw ..., 0($regA)
def optimize_lw(opt, expressions):
  if opt.checkCommand('addu') and opt[0] == opt[1] and isinstance(add[2], int):
    ex = expressions.readExpressionOffset()
    if lw.checkLoad() and ex[-1] == '0(%s)' % opt[0]:
      ex[-1] = '%s(%s)' % (opt[2], opt[0])
      expressions.substitute(2, [ex])
      return 1

# Original sequence     | Replacement
# shift $regA, $regA, 0 |  --- (remove)
# (shift = sll, sla, srl, sra)
def zero_shift(opt, expressions):
  if opt[0] == opt[1] and opt[2] == 0 and opt.checkShift():
    expressions.substitute(1, [])
    return 1

def getRidOfRedundancy(block):
  prev = -1
  switch = False
  funcs = [remove, replace, jal, move, optimize_ld, zero_shift, optimize_lw]

  while prev != len(block):
    prev = len(block)
    while not block.checkPosition():
      ex = block.readExpression()
      for func in funcs:
        if func(ex, block):
          switch = True
          break

    return switch
  """
  cmds = ['remove', 'replace', 'jal', 'move']

  while len(block) != prev:
    prev = len(block)
    while not block.checkPosition():
      ex = block.read()
      for cmd in cmds:
        if moves(ex, block, cmd):
          switch = True
          break
      for func in funcs:
        if func(ex, block):
          switch = True
          break

  return switch
  """
def optimize_block(block):
  """Optimize a basic block."""
  while getRidOfRedundancy(block):
    pass

def optimizer(expressions, verbose=0):
  """  lengths = []
  lengths1.append(len(expressions))
  beq_bne(expressions)
  lengths2.append(len(expressions))

  blocks = bbs_find(expressions)
  map(optimize_block, blocks)
  blockExpressions = map(lambda blck: blck.expressions, blocks)
  optimizedBlocks = reduce(lambda x, y: x + y, blockExpressions)
  lengths3.append(len(optimizedBlocks)) """
  o = len(expressions)
  beq_bne(expressions)
  g = len(expressions)

  # Optimize basic blocks
  blocks = bbs_find(expressions)
  map(optimize_block, blocks)
  block_statements = map(lambda b: b.expressions, blocks)
  opt_blocks = reduce(lambda a, b: a + b, block_statements)
  b = len(opt_blocks)

  if verbose:
    print 'Expressions:     %d' % o
    print 'Optimization:    %d' % g
    print 'BB optimization: %d' % b
  
  return opt_blocks
