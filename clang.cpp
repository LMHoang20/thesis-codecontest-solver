#include <iostream>
#include <clang-c/Index.h>

// Callback function to traverse the AST nodes
CXChildVisitResult visitor(CXCursor cursor, CXCursor parent, CXClientData client_data) {
    // Print the kind of the current cursor
    CXString cursor_kind = clang_getCursorKindSpelling(clang_getCursorKind(cursor));
    std::cout << clang_getCString(cursor_kind) << std::endl;
    clang_disposeString(cursor_kind);

    // Recursively visit children
    clang_visitChildren(cursor, visitor, nullptr);

    return CXChildVisit_Continue;
}

int main() {
    // Initialize Clang
    CXIndex index = clang_createIndex(0, 0);
    
    // Path to your C++ file
    const char* file_path = "/Users/hoangle/Other/thesis/thesis-codecontest-solver/tmp.cpp";
    
    // Parse the C++ file
    CXTranslationUnit tu = clang_parseTranslationUnit(index, file_path, nullptr, 0, nullptr, 0, CXTranslationUnit_None);
    
    // Get the root cursor
    CXCursor root_cursor = clang_getTranslationUnitCursor(tu);
    
    // Traverse the AST
    clang_visitChildren(root_cursor, visitor, nullptr);
    
    // Clean up
    clang_disposeTranslationUnit(tu);
    clang_disposeIndex(index);

    return 0;
}
