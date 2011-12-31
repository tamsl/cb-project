import ply.yacc as yacc
from parse_lex import tokens
from peep import Statement as S, Block


# Global statements administration
statements = []


# Parsing rules
begin = 'system'

def p_input(p):
    '''system :
             | system list'''
    pass

def p_line_instruction(p):
    'list : instruction NEWLINE'
    pass

def p_comment(p):
    'list : COMMENT NEWLINE'
    statements.append(S('comment', p[1], inline=False))

def p_comment_newline(p):
    'list : instruction COMMENT NEWLINE'
    statements.append(S('comment', p[2], inline=True))

def p_instruction(p):
    'instruction : command'
    pass

def p_directive(p):
    'instruction : DIRECTIVE'
    statements.append(S('directive', p[1]))

def p_word_colon(p):
    'instruction : WORD COLON'
    statements.append(S('label', p[1]))

def p_command(p):
    '''command : WORD WORD COMMA WORD COMMA WORD
               | WORD WORD COMMA WORD
               | WORD WORD
               | WORD'''
    statements.append(S('command', p[1], *list(p)[2::2]))

def p_error(p):
    print 'Syntax error at "%s" on line %d' % (p.value, lexer.lineno)


# Build YACC
yacc.yacc()


def parse_file(filename):
    """Parse a given Assembly file, return a Block with Statement objects
    containing the parsed instructions."""
    global statements

    statements = []

    try:
        content = open(filename).read()
        yacc.parse(content)
    except IOError:
        raise Exception('File "%s" could not be opened' % filename)

    return Block(statements)
