from math import log
import re
from block_optimize import bbs_find

import re

def remove(opt, expressions):
  # Original sequence | Replacement
  # mov $regA, $regB  | --- (remove)
  # (with $regA == $regB)
  if opt.is_command('opt'):
    if opt[0] == opt[1]:
      expressions.replace(1, [])
      return True

  # Original sequence       | Replacement
  # mov $regA, $regB        | instr $regA, $regB,...
  # instr $regA, $regA, ... |
def replace(opt, expressions):
  if opt.is_command('opt'):
    ex = expressions.peek()
    if ex and ((ex[0] and ex[1]) == opt[0]) and len(ex) > 1:
      ex[1] = opt[1]
      expressions.replace(2, [ex])
      return True

  # Original sequence | Replacement
  # instr $regA, ...  | instr $4, ...
  # mov $4, $regA     | jal XX
  # jal XX            |
def jal(opt, expressions):
  if opt.is_command() and len(opt) > 0:
    ex = expressions.peek(2)
    if len(ex) > 1:
      instr, jal = ex
      if instr.is_command('move') and opt[0] == instr[1]:
        if jal.is_command('jal') and re.match('^\$[4-7]$', instr[0]):
          opt[0] = instr[0]
          expressions.replace(2, [opt])
          return True

  # Original sequence | Replacement
  # mov $regA, $regB  | move $regA, $regB
  # mov $regB, $regA  |
def move(opt, expressions):
  if opt.is_command('move'):
    mov = expressions.peek()
    if mov.is_command('move') and opt[1] == mov[0] and opt[0] == mov[1] :
      expressions.replace(2, [opt])
      return True

# Original sequence  | Replacement
#   beq/bne ..., $Lx |   bne/beq ..., $Ly
#   j $Ly            | $Lx:
# $Lx:
def beq_bne(expressions):
  prev = -1
  while prev != len(expressions):
    prev = len(expressions)
    while not expressions.end():
      e = expressions.read()
      if e.is_command('beq', 'bne'):
        ex = expressions.peek(2)
        if len(ex) == 2:
          j, i = ex
          if j.is_command('j') and i.is_label(e[2]):
            e.name = 'bne' if e.is_command('beq') else 'beq'
            e[2] = j[0]
            expressions.replace(3, [e, i])

# Original sequence | Replacement
# sw $regA, XX      |  sw $regA, XX
# ld $regA, XX
def optimize_ld(opt, expressions):
  if opt.is_command('sw'):
    load = expressions.peek()
    if load.is_command('lw') and load.args == opt.args:
      expressions.replace(2, [opt])
      return True

# Original sequence    | Replacement
# add $regA, $regA, X  | lw ..., X($regA)
# lw ..., 0($regA)
def optimize_lw(opt, expressions):
  if opt.is_command('addu') and opt[0] == opt[1] and isinstance(opt[2], int):
    ex = expressions.peek()
    if lw.is_load() and ex[-1] == '0(%s)' % opt[0]:
      ex[-1] = '%s(%s)' % (opt[2], opt[0])
      expressions.replace(2, [ex])
      return True

# Original sequence     | Replacement
# shift $regA, $regA, 0 |  --- (remove)
# (shift = sll, sla, srl, sra)
def zero_shift(opt, expressions):
  if opt.is_shift() and opt[0] == opt[1] and opt[2] == 0:
    expressions.replace(1, [])
    return True

def getRidOfRedundancy(block):
  prev = -1
  switch = False
  funcs = [remove, replace, jal, move, optimize_ld, zero_shift, optimize_lw]

  while prev != len(block):
    prev = len(block)
    while not block.end():
      ex = block.read()
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

def optimize(expressions, verbose=0):
  lengths = []
  lengths.append(len(expressions))
  beq_bne(expressions)
  lengths.append(len(expressions))

  blocks = bbs_find(expressions)
  map(optimize_block, blocks)
  blockExpressions = map(lambda blck: blck.expressions, blocks)
  optimizedBlocks = reduce(lambda x, y: x + y, blockExpressions)
  lengths.append(len(optimizedBlocks))

  if verbose:
    print 'Expressions:     %d' % lengths[0]
    print 'Optimization:    %d' % lengths[1]
    print 'BB optimization: %d' % lengths[2]
  
  return optimizedBlocks
