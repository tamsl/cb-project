
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\x8b\x82Eo8r*\xa2\x90\x88\x11\xbf\x8f\xf4\xf4f'
    
_lr_action_items = {'COMMENT':([0,1,3,4,5,6,7,8,10,11,12,13,15,17,],[-1,2,9,-12,-7,-2,-6,-4,-3,-8,-11,-5,-10,-9,]),'WORD':([0,1,4,6,8,10,13,14,16,],[-1,4,12,-2,-4,-3,-5,15,17,]),'DIRECTIVE':([0,1,6,8,10,13,],[-1,5,-2,-4,-3,-5,]),'NEWLINE':([2,3,4,5,7,9,11,12,15,17,],[8,10,-12,-7,-6,13,-8,-11,-10,-9,]),'COLON':([4,],[11,]),'COMMA':([12,15,],[14,16,]),'$end':([0,1,6,8,10,13,],[-1,0,-2,-4,-3,-5,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'command':([1,],[7,]),'instruction':([1,],[3,]),'list':([1,],[6,]),'system':([0,],[1,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> system","S'",1,None,None,None),
  ('system -> <empty>','system',0,'p_input','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',14),
  ('system -> system list','system',2,'p_input','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',15),
  ('list -> instruction NEWLINE','list',2,'p_line_instruction','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',19),
  ('list -> COMMENT NEWLINE','list',2,'p_comment','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',23),
  ('list -> instruction COMMENT NEWLINE','list',3,'p_comment_newline','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',27),
  ('instruction -> command','instruction',1,'p_instruction','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',31),
  ('instruction -> DIRECTIVE','instruction',1,'p_directive','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',35),
  ('instruction -> WORD COLON','instruction',2,'p_word_colon','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',39),
  ('command -> WORD WORD COMMA WORD COMMA WORD','command',6,'p_command','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',43),
  ('command -> WORD WORD COMMA WORD','command',4,'p_command','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',44),
  ('command -> WORD WORD','command',2,'p_command','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',45),
  ('command -> WORD','command',1,'p_command','/home/alexandra/Desktop/cb-project/code/parse_yacc.py',46),
]
