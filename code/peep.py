import re

class Block:
  def __init__(self, expressions = []):
    self.position = 0
    self.expressions = expressions

  def __iter__(self):
    return iter(self.expressions)

  def __getitem__(self, key):
    return self.expressions[key]

  def __len__(self):
    return len(self.expressions)

  # Read expression at the current position. Then move position one further.
  def readExpression(self, c = 1):
    self.position = self.position + 1
    return self.expressions[self.position - 1]

  # Returns false if the variable position is not at the end of the list of
  # expressions and true if it is at the end of the list of expressions.
  def checkPosition(self):
    if len(self) != self.position:
      return False
    else:
      return True

  # Using the present position read expressions until until an offset.
  def readExpressionsOffset(self, c = 1):
    if self.checkPosition() == True:
      if c != 1:
        return []
      else:
        return Expression('empty', '')

    if c != 1:
      return self.expressions[self.position : self.position + count]
    else:
      self.expressions[self.position]

  # Replace the current with a substitute list of expressions. 
  # Then adjust the position. 
  def substitute(self, c, sub, begin = None):
    if self.position != 0:
      if begin == None:
        begin = self.position - 1
    else:
      raise Exception('No expression has been read so far.')

    self.position = len(sub) + begin
    self.expressions = self.expressions[:begin] + sub + self.expressions[begin + c:]

  def putIn(self, expression, i = None):
    i = i if i != None else i = self.position
    self.expressions.insert(i, expression)

  def cleanUp(self, cb):
    self.expressions = filter(cb, self.expressions)

  # Reset position and reverse the list of expressions.
  def resetAndReverse(self):
    self.position = 0
    self.expressions.reverse()
