import re

# Write the created assembly code in the file.
def writeAssemblyCodeInFile(fileName, expressions):
  file_func = open(fileName, 'w+')
  file_func.write(createAssemblyCode(expressions))
  file_func.close()

# Create assembly code using a list of expressions. 
def createAssemblyCode(expressions):
  assemblyCode = ''
  previous = ''
  spacing = 0

  for i, ex in enumerate(expressions):
    if not i:
      newLine = ''
    else:
      newLine = '\n'

    if ex.checkDirective() == True or ex.checkControl() == True:
      line = '\t' + ex.name
      if ex.checkControl() == True:
        if len(ex):
          if len(ex.name) >= 8:
            line = line + ' '
          else:
            line = line + '\t' 

          line = line + ','.join(ex.args)
    elif ex.checkNote() == True:
      line = '#' + ex.name
      if ex.checkNoteInline() == False:
        line = ('\t' * spacing) + line
      else:
        newLine = '\t' * (1 + int(ceil((24 - len(previous.expandtabs(4))) / 4.)))
    elif ex.checkLabel() == True:
      line = ex.name + ':'
      spacing = 1
    else:
      raise Exception

    assemblyCode = assemblyCode + (newLine + line)
    previous = line

  return (assemblyCode + '\n')

# Class of Block
class Block:
  def __init__(self, expressions=[]):
    self.expressions = expressions
    self.position = 0

  def __iter__(self):
    return iter(self.expressions)

  def __getitem__(self, key):
    return self.expressions[key]

  def __len__(self):
    return len(self.expressions)

  # Returns false if the variable position is not at the checkPosition of the list of
  # expressions and true if it is at the checkPosition of the list of expressions.
  def checkPosition(self):
    if len(self) != self.position:
      return False
    else:
      return True

  # Read expression at the current position. Then move position one further.
  def readExpression(self, c = 1):
    self.position = self.position + 1
    return self.expressions[self.position - 1]

  # Using the present position read expressions until until an offset.
  def readExpressionsOffset(self, c = 1):
    if self.checkPosition() == True:
      if c != 1:
        return []
      else:
        return Expression('empty', '')
    if c != 1:
      return self.expressions[self.position : self.position + c]
    else:
      return self.expressions[self.position]

  # Reset position and reverse the list of expressions.
  def resetAndReverse(self):
    self.position = 0
    self.expressions.reverse()
  
  # Adding expression
  def putIn(self, expression, i = None):
    i = i if i != None else self.position
    self.expressions.insert(i, expression)

  # Filter expressions
  def cleanUp(self, cb):
    expres = self.expressions
    self.expressions = filter(cb, expres)

  # Replace the current with a substitute list of expressions. 
  # Then adjust the position. 
  def substitute(self, c, sub, begin = None):
    if begin == None:
      begin = self.position - 1
    if self.position == 0:
      raise Exception()

    self.position = len(sub) + begin
    self.expressions = self.expressions[:begin] + sub + self.expressions[begin + c:]

# Class of Expression
class Expression:
  eID = 1
  def __init__(self, typeExpression, name, *args, **otherArgs):
    self.typeE = typeExpression
    self.name = name
    self.args = list(args)
    self.otherArgs = otherArgs
    self.eID = Expression.eID
    Expression.eID = 1 + Expression.eID

  def __getitem__(self, key):
    return self.args[key]

  def __setitem__(self, key, v):
    self.args[key] = v

  # Controlling equal expressions
  def __eq__(self, express):
    if express.name == self.name and express.typeE == self.typeE \
       and express.args == self.args:
      return True
    else:
      return False

  def __len__(self):
    return len(self.args)

  def __str__(self):
    details = '<Expression: eID = %d type = %s name = %s  args = %s>' \
               % (self.eID, self.typeE, self.name, self.args)
    return details

  def __repr__(self):
    return str(self)

 # Checking Note expression
  def checkNote(self):
    if self.typeE != 'note':
      return False
    else:
      return True

  # Checking Note Inline expression
  def checkNoteInline(self):
    if self.otherArgs['inline'] and self.typeE == 'note':
      return True
    else:
      return False

  # Checking Directive expression
  def checkDirective(self):
    if self.typeE != 'direct':
      return False
    else:
      return True

  # Checking Label expression
  def checkLabel(self, name = None):
    if name != None:
      if self.typeE == 'label' and self.name == name:
        return True
      else:
        return False
    else:
      if self.typeE != 'label':
        return False
      else:
        return True  

  # Checking Control expression
  def checkControl(self, *args):
    if (self.name in args or not len(args)) and self.typeE == 'control':
      return True
    else:
      return False

  # Checking Branch expression
  def checkBranch(self):
    if re.match('bne|beq|bgtz|bltz|bct|bgez|bcf|blez$', self.name) \
       and self.checkControl() == True:
      return True
    else:
      return False

  # Checking Jump expression
  def checkJump(self):
    if re.match('^bne|beq|jal|j|bgtz|bltz|bct|bgez|bcf|blez$', self.name) \
      and self.checkControl() == True:
      return True
    else:
      return False

  # Checking Target Jump expression
  def getTargetJump(self):
    if self.checkJump() == True:
      return self[-1]
    else:
      raise Exception('Command "%s" does not contain a target jump' % self.name)

  # Checking Shift expression
  def checkShift(self):
    if (re.match('^s(rl|ra|ll)$', self.name) and self.checkControl()) == True:
      return True
    else:
      return False

  # Checking Shift 'less then' expression
  def checkShift2(self):
    cmds = ['sltu', 'slt']
    for i in range(0, len(cmds)):
      if self.name == cmds[i] and self.checkControl() == True:
        return True
    return False

  # Checking Load argument expression
  def checkLoad(self):
    cmds = ['dlw', 'l.s', 'l.d', 'li', 'lw'] 
    for i in range(0, len(cmds)):
      if self.name == cmds[i] and self.checkControl() == True:
        return True
    return False  

  # Checking Load expression
  def checkLoad2(self):
    if re.match('^l(bu|a|w||\.s|b|\.d)|dlw$', self.name) \
       and self.checkControl() == True:
      return True
    else:
      return False  

  # Checking Arithmetic expression
  def checkArithmetic(self):
    if re.match('^s(rl|ra|ll)|(and|neg|mflo|mfhi|abs|[xn]?or)|(slt|add|sub)u?'
                + '|sqrt|neg|div|abs|mult|c|add|sub)\.[sd]$', self.name) \
       and self.checkControl() == True:
      return True
    else:
      return False

  # Checking Arithmetic controller expression
  def checkArithmeticD(self):
    if re.match('^(div|add|mul|sub)\.d$', self.name) \
       and self.checkControl() == True:
      return True
    else:
      return False

  # Checking Move expression
  def checkMove(self):
    cmds = ['mthi', 'mflo'] 
    for i in range(0, len(cmds)):
      if self.name == cmds[i] and self.checkControl() == True:
        return True
    return False

  # Checking Unary expression
  def checkMonop(self):
    if not (self.checkArithmetic() == True and len(self) == 2):
      return False
    else:
      return True

  # Checking Unary controller expression
  def checkUnaryD(self):
    if re.match('^(neg|abs|mov)\.d$', self.name) and self.checkControl() == True:
      return True
    else:
      return False

  # Checking Binary expression
  def checkBinop(self):
    if len(self) == 3 and self.checkJump() == False \
       and self.checkControl() == True:
      return True
    else:
      return False

  # Checking Truncate expression
  def checkTruncate(self):
    if re.match('^trunc\.[a-z\.]*$', self.name) and self.checkControl() == True:
      return True
    else:
      return False

  # Checking Convert expression
  def checkConvert(self):
    if re.match('^cvt\.[a-z\.]*$', self.name) and self.checkControl() == True:
      return True
    else:
      return False
 
  # Checking Logic expression
  def checkLogical(self):
    if re.match('^(and|xor|or)i?$', self.name) and self.checkControl() == True:
      return True
    else:
      return False

  # Checking definition of register using retrieve()
  def checkDefinition(self, register):
    definition = self.retrieve()
    return register in definition

  # Checking usage of register using retrieveUsage()
  def checkUsage(self, register):
    usage = self.retrieveUsage()
    return register in usage
  
  # Retrieve expression variables
  def retrieve(self):
    if self.checkLoad() == True or self.checkLogical() == True \
       or self.checkArithmetic() == True or self.checkArithmeticD() == True \
       or self.checkConvert() == True or self.checkTruncate() == True \
       or self.checkLoad2() == True or self.checkUnaryD() == True \
       or self.checkShift2() == True or self.checkMove() == True \
       or (self.name in ['addu', 'li', 'mtc1', 'move', 'dmfc1', 'subu'] \
           and self.checkControl() == True):
      return self[0]
    else:
      return []

  # Usage of retrieved expression variables 
  def retrieveUsage(self):
    retrieved = []
    
    if self.checkControl('move') == True or len(self) == 2:
      retrieved.append(self[1])
    elif self.checkControl('sw', 'sb', 'dsw', 's.d', 's.s', 'lw'):
      if re.match('^d+\(([^)]+)\)$', self[1]) == True:
        retrieved.append(re.match('^d+\(([^)]+)\)$', self[1]).group(1))
        cmds = ['dsw', 'sw']
        for i in range(0, len(cmds)):
          if self.name == cmds[i]:
            retrieved.append(self[0])
    elif self.checkBinop():
      retrieved = retrieved + self[1:]
    return retrieved

