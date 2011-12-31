
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xa9RF^I\xbb4\xb0\xd6\xd9J@\xd1$%)'
    
_lr_action_items = {'COMMENT':([0,1,3,4,5,6,7,8,10,11,12,13,15,17,],[-1,2,9,-12,-7,-6,-2,-4,-3,-8,-11,-5,-10,-9,]),'WORD':([0,1,4,7,8,10,13,14,16,],[-1,4,12,-2,-4,-3,-5,15,17,]),'DIRECTIVE':([0,1,7,8,10,13,],[-1,5,-2,-4,-3,-5,]),'NEWLINE':([2,3,4,5,6,9,11,12,15,17,],[8,10,-12,-7,-6,13,-8,-11,-10,-9,]),'COLON':([4,],[11,]),'COMMA':([12,15,],[14,16,]),'$end':([0,1,7,8,10,13,],[-1,0,-2,-4,-3,-5,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'input':([0,],[1,]),'line':([1,],[7,]),'instruction':([1,],[3,]),'command':([1,],[6,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> input","S'",1,None,None,None),
  ('input -> <empty>','input',0,'p_input','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',72),
  ('input -> input line','input',2,'p_input','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',73),
  ('line -> instruction NEWLINE','line',2,'p_line_instruction','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',77),
  ('line -> COMMENT NEWLINE','line',2,'p_line_comment','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',81),
  ('line -> instruction COMMENT NEWLINE','line',3,'p_line_inline_comment','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',85),
  ('instruction -> command','instruction',1,'p_instruction_command','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',89),
  ('instruction -> DIRECTIVE','instruction',1,'p_instruction_directive','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',93),
  ('instruction -> WORD COLON','instruction',2,'p_instruction_label','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',97),
  ('command -> WORD WORD COMMA WORD COMMA WORD','command',6,'p_command','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',101),
  ('command -> WORD WORD COMMA WORD','command',4,'p_command','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',102),
  ('command -> WORD WORD','command',2,'p_command','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',103),
  ('command -> WORD','command',1,'p_command','/home/tamara/Documenten/compilerbouw/peephole/src/parser.py',104),
]