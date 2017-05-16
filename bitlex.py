BIOP = 'BIOP'
UNIOP = 'UNIOP'
IOSTATE = 'IOSTATE'
ASOP = 'ASOP'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
CONDSTATE = 'CONDSTATE'
ENDCON = 'ENDCON'
LITERAL = 'LITERAL'
ID = 'ID'

tokens = [
	(r"(?m)(^/.*\n)|(/.*)", None),
	(r"\s", None),
	(r"(!?[+^&])|>>|<<|\.|@",BIOP),
	(r"[IHS]?[<>]",IOSTATE),
	(r"[!#'$£]", UNIOP),
	(r"[~\-*]", CONDSTATE),
	(r"\;", ENDCON),
	(r"=",ASOP),
	(r"\(", LPAREN),
	(r"\)", RPAREN),
	(r"[01]+", LITERAL),
	(r"([a-zA-Z]+)|\"", ID)
]