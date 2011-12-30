import re

def moves(opt, expr, t):
  # Original sequence | Replacement
  # mov $regA, $regB  | --- (remove)
  # (with $regA == $regB)
  if t == 'remove':
    if opt.checkCommand('opt'):
      if opt[0] == opt[1]:
        expr.substitute(1, [])
        return 1

  # Original sequence       | Replacement
  # mov $regA, $regB        | instr $regA, $regB,...
  # instr $regA, $regA, ... |
  elif t == 'replace':
    if opt.checkCommand('opt'):
      ex = expr.readExpressionOffset()
      if ex and ((ex[0] and ex[1]) == opt[0]) and len(ex) > 1:
        ex[1] = opt[1]
        expr.substitute(2, [ex])
        return 1

  # Original sequence | Replacement
  # instr $regA, ...  | instr $4, ...
  # mov $4, $regA     | jal XX
  # jal XX            |
  elif t == 'jal':
    if opt.checkCommand() and len(opt) > 0:
      ex = expr.readExpressionOffset(2)
      if len(ex) > 1:
        instr, jal = ex
        if opt[0] == instr[1] and instr.checkCommand('move'):
          if re.match('^\$[4-7]$', instr[0]) and jal.checkCommand('jal'):
            opt[0] = instr[0]
            expr.substitute(2, [opt])
            return 1

  # Original sequence | Replacement
  # mov $regA, $regB  | move $regA, $regB
  # mov $regB, $regA  |
  elif t == 'move':
    if opt.checkCommand('move'):
      mov = expr.readExpressionOffset()
      if mov.checkCommand('move') and opt[1] == mov[0] and opt[0] == mov[1] :
        expr.substitute(2, [opt])
        return 1

  else:
    return 0

# Original sequence  | Replacement
#   beq/bne ..., $Lx |   bne/beq ..., $Ly
#   j $Ly            | $Lx:
# $Lx:
def beq_bne(expr):
  prev = -1
  while prev != len(expr):
    prev = len(expr)
    while not expr.end():
      e = expr.read()
      if e.checkCommand('beq', 'bne'):
        ex = expr.readExpressionOffset(2)
        if len(ex) == 2:
          j, i = ex
          if j.checkCommand('j') and i.checkLabel(e[2]):
            if e.checkCommand('beq'):
              e.name = 'bne'
            else:
              e.name = 'beq'
            e[2] = j[0]
            expr.substitute(3, [e, i])

# Original sequence | Replacement
# sw $regA, XX      |  sw $regA, XX
# ld $regA, XX
def optimize_ld(opt, expr):
  if opt.checkCommand('sw'):
    load = expr.readExpressionOffset()
    if load.args == opt.args and load.checkCommand('lw'):
      expr.substitute(2, [opt])
      return 1

# Original sequence    | Replacement
# add $regA, $regA, X  | lw ..., X($regA)
# lw ..., 0($regA)
def optimize_lw(opt, expr):
  if opt.checkCommand('addu') and opt[0] == opt[1] and isinstance(add[2], int):
    ex = expr.readExpressionOffset()
    if lw.checkLoad() and ex[-1] == '0(%s)' % opt[0]:
      ex[-1] = '%s(%s)' % (opt[2], opt[0])
      expr.substitute(2, [ex])
      return 1

# Original sequence     | Replacement
# shift $regA, $regA, 0 |  --- (remove)
# (shift = sll, sla, srl, sra)
def zero_shift(opt, expr):
  if opt[0] == opt[1] and opt[2] == 0 and opt.checkShift():
    expr.substitute(1, [])
    return 1