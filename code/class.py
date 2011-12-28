class Line:
  def __init__(self, line):
    self.type = line[0]
    self.args = line[1]

  def jumpAvailable(self):
    if self.args[0][0] == 'j' and (not (self.args[0] == 'jal' and
       self.args[1][1] == '__main')):
      return 1
    else:
      return 0

  def branchAvailable(self):
    if self.args[0][0] == 'b':
      return 1
    else:
      return 0

  def __str__(self):
    return '%s' % self.args

class Instruct:
  def __init__(self, instruct):
    if instruc[0] != '.':
      self.cmd = instruct[0]
      self.args = instruct[1:]
    else:
      self.cmd = instruct
      self.args = []

  def __str__(self):
    return "%s\t%s\n" % (self.cmd, ','.join([i[1] for i in self.args]))

class Block:
  def __init__(self, label = ''):
    self.label = label
    self.curr_func = ''
    self.instructs = []
    self.targets = ['','']
    self.cpiler_directives = ['', '']

  def appendInstruct(self, instruct):
    self.instructs.append(Instruct (instruct))

  def exitJump(self, label):
    self.appendInstruct(['j', ('LABEL', '$31')])
    self.cpiler_directives[1] += '.end %s' % label

  def detectJump(self, jump = 'j'):
    return jump == self.instructs[-1].cmd[0] and self.instructs

  def noJump(self):
    return not (self.detectJump() or self.detectJump('b')) and self.instructs

  def detectLiveness(self):
    pass

  def optimize(self):
    for i in self.instructs:
      if i.cmd[:3] == 'add':
        self.optimizeAdd(i)
      elif i.cmd == 'sw':
        self.optimizeStore(i)
      elif i.cmd == 'move':
        self.optimizeMove(i)
      elif i.cmd == 'sll' or i.cmd == 'sla' or\
           i.cmd == 'srl' or i.cmd == 'sra':
        self.optimizeShift(i)

  def optimizeAdd(self, other):
    rA = other.args[0][1]
    rB = other.args[1][1]
    rC = other.args[2][1]
    offset = self.instructs.index(other)

    # Loop through all instructions unless there are jumps or jal.
    for n in self.instructs[offset:]:
      if len(n.args) == 1:
        if n.cmd == 'j':
          break
          
        if n.cmd != 'lw':
          for nA in next.args:
            if nA[1] == rB or nA[1] == rA:
              return 0
          
          continue
    
        if rA == n.args[-1][1][2:-1] and rA == rB and rC.find('$') == -1:
          self.instructs.remove(other)
          self.n.args[-1] = ('REGISTER_WITH_OFFSET', '%d(%s)' % (rC, rA))

  def optimizeStore(self, other):
    rA = other.args[0][1]
    offset = self.instructs.index(other)

    # Loop through all instructions unless there are jumps or jal.
    for n in self.instructs[offset:]:
      if len(n.args) == 1:
        if n.cmd == 'j':
          break
      
      if rA == n.args[0][1] and n.cmd == 'ld':
        self.instructs.remove(n)
      
      for nA in n.args:
        if nA[1] == rA:
          break

  def optimizeShift(self, instruct):
    rA = instruct.arguments[0][1]
    rB = instruct.arguments[1][1]
    rC = instruct.arguments[2][1]
    
    if rC == 0 and rB == rA:
      self.instructs.remove(instruct)
        
  def optimizeMove(self, other):
    rA = other.args[0][1]
    rB = other.args[1][1]
    
    if rB == rA:
      self.instrucs.remove(other)
      return 1
      
    self.optimizeMoveInstr(other, rA, rB)

  # In case there is a move and a jal instruction afterwards.
  def optimizeMoveJal(self, other, jal, rB):
    offset = self.instructs.index(other)
    
    # Search for register that is the same.
    for previous in reversed(self.instructs[:offset]):
      if previous.cmd[0] == 'j':
        break
        
      if not previous.args:
        continue

      # See if any other arguments are using the register that is looked for.
      if len(previous.args) >= 2:
        for pA in previous.args[1:]:
          if rB == pA[1]:
            return 0
             
      if rB == previous.args[0][1]:
        self.instructs.remove(other)
        previous.args[0] = ('REGISTER', '$4')
        return 1

    return 0

  def optimizeMoveInstr(self, other, rA, rB):
    offset = self.instructs.index(other) + 1

    # Loop through all instructions unless there are jumps or jal.
    for n in self.instructs[offset:]:
      if len(n.args) == 1:
        if n.cmd == 'j':
          break
          
        if rA == n.arguments[0][1]:
          break

        if rA == '$4' and n.cmd == 'jal':
          return self.optimizeMoveJal(other, n, rB)
              
      elif len(n.args) >= 2:      
        rAn = n.args[0][1]
        rBn = n.args[1][1]

        if rAn == rA or rBn == rA:
          if rAn == rBn:
            self.instructs.remove(other)
            n.args[1][1] = ('REGISTER', rB)
            return 1
          else:
            break
            
        if rB == rAn or rB == rAn:
          break
          
    return 0
