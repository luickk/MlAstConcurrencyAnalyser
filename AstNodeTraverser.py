import sys
import clang.cindex

def main():
    clang.cindex.Config.set_library_path("/Library/Developer/CommandLineTools/usr/lib/")
    index = clang.cindex.Index.create()

    tu = index.parse(sys.argv[1])

    root_node = tu.cursor
    fork_calls = ast_traverse(root_node)

    print(fork_calls)

def ast_traverse(node):
    for child in node.get_children():
        ast_traverse(child)

    fork_calls = []
    if node.kind == clang.cindex.CursorKind.CALL_EXPR:
        print("Fork call with name: '" + node.displayname + "'/'" +  node.spelling + "' (Line/Col)" + str(node.location.line) + "/" + str(node.location.column) + " of type " + str(node.type));
        # fork_calls.append(node)

    
        
    return fork_calls


if __name__ == "__main__":
    main()
