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
    fork_calls = []
    for child in node.get_children():
        ast_traverse(child)

    if node.type == clang.cindex.CursorKind.CALL_EXPR:
        if node.name == "pthread_create":
            print("Fork call with name: '" + node.displayname + "' (Line/Col)" + str(node.location.line) + "/" + str(node.location.column));
            fork_calls.append(node)
    
    return fork_calls


if __name__ == "__main__":
    main()
