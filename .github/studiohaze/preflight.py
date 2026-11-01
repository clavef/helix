import ctypes, pathlib, tree_sitter
for lang, ext in [('topaz','tpz'),('lispex','lspx')]:
    lib = ctypes.CDLL(f'/tmp/{lang}.so')
    fn = getattr(lib, 'tree_sitter_'+lang)
    fn.restype = ctypes.c_void_p
    capsule = ctypes.pythonapi.PyCapsule_New
    capsule.restype = ctypes.py_object
    capsule.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p)
    language = tree_sitter.Language(capsule(fn(), b'tree_sitter.Language', None))
    for query in pathlib.Path('runtime/queries',lang).glob('*.scm'):
        tree_sitter.Query(language, query.read_text())
        print('QUERY_OK',lang,query.name)
    parser = tree_sitter.Parser(language)
    source = pathlib.Path(f'.github/studiohaze/{lang}.{ext}').read_bytes()
    tree = parser.parse(source)
    assert not tree.root_node.has_error, tree.root_node
    print('PARSE_OK',lang)
