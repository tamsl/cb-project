import re

# Write the created assembly code in the file.
def writeAssemblyCodeInFile(fileName, expressions):
  theFile = open(fileName, 'w+')
  theFile.write(createAssemblyCode(expressions))
  theFile.close()

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

    if ex.is_directive() == True or ex.is_command() == True:
      line = '\t' + ex.name
      if ex.is_command() == True:
        if len(ex):
          if len(ex.name) >= 8:
            line = line + ' '
          else:
            line = line + '\t' 

          line = line + ','.join(ex.args)
    elif ex.is_comment() == True:
      line = '#' + ex.name
      if ex.is_inline_comment() == False:
        line = ('\t' * spacing) + line
      else:
        newLine = '\t' * (1 + int(ceil((24 - len(previous.expandtabs(4))) / 4.)))
    elif ex.is_label() == True:
      line = ex.name + ':'
      spacing = 1
    else:
      raise Exception

    assemblyCode = assemblyCode + (newLine + line)
    previous = line

  return (assemblyCode + '\n')

class Statement:
    sid = 1

    def __init__(self, stype, name, *args, **kwargs):
        self.stype = stype
        self.name = name
        self.args = list(args)
        self.options = kwargs

        # Assign a unique ID to each satement
        self.sid = Statement.sid
        Statement.sid += 1

    def __getitem__(self, n):
        """Get an argument."""
        return self.args[n]

    def __setitem__(self, n, value):
        """Set an argument."""
        self.args[n] = value

    def __eq__(self, other):
        """Check if two statements are equal by comparing their type, name and
        arguments."""
        return self.stype == other.stype and self.name == other.name \
               and self.args == other.args

    def __len__(self):
        return len(self.args)

    def __str__(self):  # pragma: nocover
        return '<Statement sid=%d type=%s name=%s args=%s>' \
                % (self.sid, self.stype, self.name, self.args)

    def __repr__(self):  # pragma: nocover
        return str(self)

    def is_comment(self):
        return self.stype == 'comment'

    def is_inline_comment(self):
        return self.is_comment() and self.options['inline']

    def is_directive(self):
        return self.stype == 'directive'

    def is_label(self, name=None):
        return self.stype == 'label' if name == None \
               else self.stype == 'label' and self.name == name

    def is_command(self, *args):
        return self.stype == 'command' and (not len(args) or self.name in args)

    def is_jump(self):
        """Check if the statement is a jump."""
        return self.is_command() \
               and re.match('^j|jal|beq|bne|blez|bgtz|bltz|bgez|bct|bcf$', \
                            self.name)

    def is_branch(self):
        """Check if the statement is a branch."""
        return self.is_command() \
               and re.match('^beq|bne|blez|bgtz|bltz|bgez|bct|bcf$', \
                            self.name)

    def is_shift(self):
        """Check if the statement is a shift operation."""
        return self.is_command() and re.match('^s(ll|rl|ra)$', self.name)

    def is_load(self):
        """Check if the statement is a load instruction."""
        return self.is_command() and self.name in ['lw', 'li', 'dlw', 'l.s', \
                                                   'l.d']
                                                   
    def is_arith(self):
        """Check if the statement is an arithmetic operation."""
        return self.is_command() \
               and re.match('^s(ll|rl|ra)'
                            + '|(mfhi|mflo|abs|neg|and|[xn]?or)'
                            + '|(add|sub|slt)u?'
                            + '|(add|sub|mult|div|abs|neg|sqrt|c)\.[sd]$', \
                            self.name)

    def is_monop(self):
        """Check if the statement is an unary operation."""
        return len(self) == 2 and self.is_arith()

    def is_binop(self):
        """Check if the statement is an binary operation."""
        return self.is_command() and len(self) == 3 and not self.is_jump()
        
    def is_load_non_immediate(self):
        """Check if the statement is a load statement."""
        return self.is_command() \
               and re.match('^l(w|a|b|bu|\.d|\.s)|dlw$', \
                            self.name)
    def is_logical(self):
        """Check if the statement is a logical operator."""
        return self.is_command() and re.match('^(xor|or|and)i?$', self.name)
    
    def is_double_aritmethic(self):
        """Check if the statement is a arithmetic .d operator."""
        return self.is_command() \
                and re.match('^(add|sub|div|mul)\.d$', self.name)
                
    def is_double_unary(self):
        """Check if the statement is a unary .d operator."""
        return self.is_command() and \
                re.match('^(abs|neg|mov)\.d$', self.name)
                
    def is_move_from_spec(self):
        """Check if the statement is a move from the result register."""
        return self.is_command() and self.name in ['mflo', 'mthi']
        
    def is_set_if_less(self):
        """Check if the statement is a shift if less then."""
        return self.is_command() and self.name in ['slt', 'sltu']
        
    def is_convert(self):
        """Check if the statement is a convert operator."""
        return self.is_command() and re.match('^cvt\.[a-z\.]*$', self.name)
        
    def is_truncate(self):
        """Check if the statement is a convert operator."""
        return self.is_command() and re.match('^trunc\.[a-z\.]*$', self.name)
        
    def jump_target(self):
        """Get the jump target of this statement."""
        if not self.is_jump():
            raise Exception('Command "%s" has no jump target' % self.name)

        return self[-1]
    
    def get_def(self):
        """Get the variable that this statement defines, if any."""
        instr = ['move', 'addu', 'subu', 'li', 'mtc1', 'dmfc1']
        
        if self.is_load_non_immediate() or self.is_arith() \
                or self.is_logical() or self.is_double_aritmethic() \
                or self.is_move_from_spec() or self.is_double_unary() \
                or self.is_set_if_less() or self.is_convert() \
                or self.is_truncate() or self.is_load() \
                or (self.is_command and self.name in instr):
            return self[0]

        return []

    def get_use(self):
        # TODO: Finish with ALL the available commands!
        use = []

        if self.is_binop():
            use += self[1:]
        elif self.is_command('move'):
            use.append(self[1])
        elif self.is_command('lw', 'sb', 'sw', 'dsw', 's.s', 's.d'):
            m = re.match('^\d+\(([^)]+)\)$', self[1])

            if m:
                use.append(m.group(1))

            # 'sw' also uses its first argument
            if self.name in ['sw', 'dsw']:
                use.append(self[0])
        elif len(self) == 2:  # FIXME: temporary fix, manually add all commands
            use.append(self[1])

        return use

    def defines(self, reg):
        """Check if this statement defines the given register."""
        return reg in self.get_def()

    def uses(self, reg):
        """Check if this statement uses the given register."""
        return reg in self.get_use()


class Block:
    def __init__(self, expressions=[]):
        self.expressions = expressions
        self.pointer = 0

    def __iter__(self):
        return iter(self.expressions)

    def __getitem__(self, n):
        return self.expressions[n]

    def __len__(self):
        return len(self.expressions)

    def read(self, count=1):
        """Read the statement at the current pointer position and move the
        pointer one position to the right."""
        s = self.expressions[self.pointer]
        self.pointer += 1

        return s

    def end(self):
        """Check if the pointer is at the end of the statement list."""
        return self.pointer == len(self)

    def peek(self, count=1):
        """Read the statements until an offset from the current pointer
        position."""
        if self.end():
            return Statement('empty', '') if count == 1 else []

        return self.expressions[self.pointer] if count == 1 \
               else self.expressions[self.pointer:self.pointer + count]

    def replace(self, count, replacement, start=None):
        """Replace the given range start-(start + count) with the given
        statement list, and move the pointer to the first statement after the
        replacement."""
        if self.pointer == 0:
            raise Exception('No statement have been read yet.')

        if start == None:
            start = self.pointer - 1

        before = self.expressions[:start]
        after = self.expressions[start + count:]
        self.expressions = before + replacement + after
        self.pointer = start + len(replacement)

    def insert(self, statement, index=None):
        if index == None:
            index = self.pointer

        self.expressions.insert(index, statement)

    def apply_filter(self, callback):
        """Apply a filter to the statement list. If the callback returns True,
        the statement will remain in the list.."""
        self.expressions = filter(callback, self.expressions)

    def reverse_statements(self):
        """Reverse the statement list and reset the pointer."""
        self.expressions = self.expressions[::-1]
        self.pointer = 0