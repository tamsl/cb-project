
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = "\xa3\x88\xa5\x1c\xa2\xce\xa8\x08'\xd7\x87\\9\x1d.\xe9"
    
_lr_action_items = {'NEWLINE':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,17,],[-1,-9,-6,9,-2,-7,10,-13,13,-3,-4,-8,-12,-5,-11,-10,]),'DIRECT':([0,1,4,9,10,13,],[-1,5,-2,-3,-4,-5,]),'NOTE':([0,1,2,3,4,5,7,9,10,11,12,13,15,17,],[-1,6,-6,8,-2,-7,-13,-3,-4,-8,-12,-5,-11,-10,]),'COLON':([7,],[11,]),'NUMB':([0,1,4,7,9,10,13,14,16,],[-1,7,-2,12,-3,-4,-5,15,17,]),'COMMA':([12,15,],[14,16,]),'$end':([0,1,4,9,10,13,],[-1,0,-2,-3,-4,-5,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'control':([1,],[2,]),'list':([1,],[4,]),'system':([0,],[1,]),'instr':([1,],[3,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> system","S'",1,None,None,None),
  ('system -> <empty>','system',0,'p_input','/home/tamara/Documenten/cb/code/parse_yacc.py',13),
  ('system -> system list','system',2,'p_input','/home/tamara/Documenten/cb/code/parse_yacc.py',14),
  ('list -> instr NEWLINE','list',2,'p_list_instr','/home/tamara/Documenten/cb/code/parse_yacc.py',20),
  ('list -> NOTE NEWLINE','list',2,'p_note','/home/tamara/Documenten/cb/code/parse_yacc.py',26),
  ('list -> instr NOTE NEWLINE','list',3,'p_note_newline','/home/tamara/Documenten/cb/code/parse_yacc.py',32),
  ('instr -> control','instr',1,'p_inst_command','/home/tamara/Documenten/cb/code/parse_yacc.py',38),
  ('instr -> DIRECT','instr',1,'p_direct','/home/tamara/Documenten/cb/code/parse_yacc.py',44),
  ('instr -> NUMB COLON','instr',2,'p_numb_colon','/home/tamara/Documenten/cb/code/parse_yacc.py',50),
  ('control -> <empty>','control',0,'p_control','/home/tamara/Documenten/cb/code/parse_yacc.py',56),
  ('control -> NUMB NUMB COMMA NUMB COMMA NUMB','control',6,'p_control','/home/tamara/Documenten/cb/code/parse_yacc.py',57),
  ('control -> NUMB NUMB COMMA NUMB','control',4,'p_control','/home/tamara/Documenten/cb/code/parse_yacc.py',58),
  ('control -> NUMB NUMB','control',2,'p_control','/home/tamara/Documenten/cb/code/parse_yacc.py',59),
  ('control -> NUMB','control',1,'p_control','/home/tamara/Documenten/cb/code/parse_yacc.py',60),
]
