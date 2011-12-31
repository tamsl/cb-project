from math import log
from block_optimize import bbs_find
import re

# Rewrite mov instruction, where reg A equals reg B
def remove(opt, expressions):
  if opt.checkControl('opt'):
    if opt[0] == opt[1]:
      expressions.substitute(1, [])
      return 1

# Rewrite mov -> instr instructions, where intr writes reg A
def substitute(opt, expressions):
  if opt.checkControl('opt'):
    ex = expressions.readExpressionsOffset()
    if ex and ((ex[0] and ex[1]) == opt[0]) and len(ex) > 1:
      ex[1] = opt[1]
      expressions.substitute(2, [ex])
      return 1

# Rewrite instr -> mov -> jal instructions, where instr writes reg A
def jal(opt, expressions):
  if opt.checkControl() and len(opt) > 0:
    ex = expressions.readExpressionsOffset(2)
    if len(ex) > 1:
      instr, jal = ex
      if instr.checkControl('move') and opt[0] == instr[1]:
        if jal.checkControl('jal') and re.match('^\$[4-7]$', instr[0]):
          opt[0] = instr[0]
          expressions.substitute(2, [opt])
          return 1

# Rewrite mov instructions where two registers are switched
def move(opt, expressions):
  if opt.checkControl('move'):
    mov = expressions.readExpressionsOffset()
    if mov.checkControl('move') and opt[1] == mov[0] and opt[0] == mov[1] :
      expressions.substitute(2, [opt])
      return 1

# Rewrite redundant branch instructions
def beq_bne(expressions):
  prev = -1
  while prev != len(expressions):
    prev = len(expressions)
    while not expressions.checkPosition():
      e = expressions.readExpression()
      if e.checkControl('beq', 'bne'):
        ex = expressions.readExpressionsOffset(2)
        if len(ex) == 2:
          j, i = ex
          if j.checkControl('j') and i.checkLabel(e[2]):
            if e.checkControl('beq'):
              e.name = 'bne'
            else:
              e.name = 'beq'
            e[2] = j[0]
            expressions.substitute(3, [e, i])

# Rewrite sw -> ld instructions
def optimize_ld(opt, expressions):
  if opt.checkControl('sw'):
    load = expressions.readExpressionsOffset()
    if load.checkControl('lw') and load.args == opt.args:
      expressions.substitute(2, [opt])
      return 1

# Rewrite add -> lw instructions
def optimize_lw(opt, expressions):
  if opt.checkControl('addu') and opt[0] == opt[1] and isinstance(opt[2], int):
    ex = expressions.readExpressionsOffset()
    if lw.is_load() and ex[-1] == '0(%s)' % opt[0]:
      ex[-1] = '%s(%s)' % (opt[2], opt[0])
      expressions.substitute(2, [ex])
      return 1

# Rewrite shift instruction
def zero_shift(opt, expressions):
  if opt.checkShift() and opt[0] == opt[1] and opt[2] == 0:
    expressions.substitute(1, [])
    return 1

# Removal of redundant instructions is organized here
def getRidOfRedundancy(block):
  prev = -1
  switch = False
  funcs = [remove, substitute, jal, move, optimize_ld, zero_shift, optimize_lw]

  while prev != len(block):
    prev = len(block)
    while not block.checkPosition():
      ex = block.readExpression()
      for func in funcs:
        if func(ex, block):
          switch = 1
          break

    return switch

# Optimize block by keep removing redundant instructions
def optimize_bb(block):
  while getRidOfRedundancy(block):
    pass

# Organize optimizations and print results
def optimize(expressions, var=0):
  lengths = []
  lengths.append(len(expressions))
  beq_bne(expressions)
  lengths.append(len(expressions))

  blocks = bbs_find(expressions)
  map(optimize_bb, blocks)
  blockExpressions = map(lambda blck: blck.expressions, blocks)
  optimizedBlocks = reduce(lambda x, y: x + y, blockExpressions)
  lengths.append(len(optimizedBlocks))

  if var:
    print 'Expressions:     %d' % lengths[0]
    print 'Optimization:    %d' % lengths[1]
    print 'BB optimization: %d' % lengths[2]
    print 'Optimization:    %d (%d%%)' \
                % (lengths[0] - lengths[2], int((lengths[0] - lengths[2]) / float(lengths[2]) * 1000))  
  return optimizedBlocks
