# Semantic Checking

Team cake: `cji`, `ksmori`, `tkatz`

## Design

### AST

We created an `ASTNode` class to model our own syntax tree instead of using Antlr’s generated parse tree. This gives us greater control and easier access to the fields that we want to store for each node. Each node has a source location (useful for printing meaningful error messages) and overrides `Object.equals` to allow two ASTs to be checked for structural equality.

Here is a quick view of the hierarchy of our `ASTNode` class.

```
ASTNode
    Program
    Block
    Declaration
        FieldDeclaration
            ArrayFieldDeclaration
            ValueFieldDeclaration
        ImportDeclaration
        MethodDeclaration
    Statement
        AssignmentStatement
        BreakStatement
        ContinueStatement
        ForStatement
        IfStatement
        MethodCallStatement
        ReturnStatement
        UpdateStatement
        WhileStatement
    Argument
        StringLiteral
        Expression
            BinaryExpression
            BoolLiteral
            FieldExpression
                ArrayFieldExpression
                IdentifierFieldExpression
            IntLiteral
            LenExpression
            LogicalExpression
            MethodCallExpression
            TernaryExpression
            UnaryExpression
```

Each node implements a `traverse` method that we use with an `ASTVisitor`. This allows us to enter and exit each node during the symbol table creation and semantic checking phases.

### Symbol Table

The symbol table works by doing a single traversal of the AST, and creating three maps:

* Declaration ASTNode -> the declared `Symbol`
* AssignmentTarget ASTNode -> the `Symbol` being written
* FieldExpression ASTNode -> the `Symbol` being read

A `Symbol` is a globally-unique value which references a specific variable in the AST, and contains metadata about the variable (currently only the variable's type). When creating a `SymbolTable`, the constructor uses scopes and variable names in order to resolve variable references, but after the `SymbolTable` has been created, it does not retain information about scopes or variable names. Instead, the maps in the symbol table are used to directly translate AST nodes to Symbols.

We anticipate that we will need to enhance this API slightly when doing code generation, in order to get all the symbols that are declared in a particular method.

### Types

We created type objects for all of the static types we needed to semantically validate.

The hierarchy:

```
ArgumentType
    StringType
    SymbolType
        ArrayType
        DeclaredMethodType
        ImportedMethodType
        ValueResolutionType
            ErrorType
            ValueType
```

These types implement methods such as `isCallableWith(argTypes)` and `isAssignableTo(otherType)` so we can keep track of what properties each type has for later semantic checking.

For example:

* A `DeclaredMethodType` keeps track of its return type and parameter types.
* A `ValueType` is one of `BOOL` or `INT`, the two values types in the Decaf specification.

Each `Expression` AST node has a `getType` method, which computes the type of the expression using a given symbol table. Later, the semantic checker verifies variable assignments by ensuring that the Type of the assignment value is assignable to the Type of the assignment target.

### Semantic checking

The semantic checker uses the `ASTVisitor` to traverse our AST structure. Upon entering or exiting a node that could potentially need semantic checking, we gather the relevant fields for that node and check them in accordance with the rules outlined in the specification.

As an example:
```java
@Override
public void exit(final Program node) {
    if (!node.methods.stream().anyMatch(this::isMainMethod)) {
        errors.add(SemanticError.noMainMethod(node));
    }
}
```

When the semantic checker exits the `Program` node, we check if any of the method declarations of the `Program` match the necessary `void main()` declaration. We confirm that the name of the method is `main`, there is no return type, and there are no parameters. If no method matches, we add a semantic error representing the "Program does not contain a void main() method" message.

All of these errors are collected into a list, which can then be printed by the caller.

## Extras

* The special type `ErrorType` is created when an unknown variable is referenced or an illegal operation is performed on a variable, such as an array access on a variable which is not an array. Any operation can be performed on `ErrorType`. This is used to avoid duplicate errors from being reported for problems related to these illegal operations. For example, if `foo` is unresolved in the expression `1 + foo`, an error should be reported to indicate that `foo` is unresolved. However, no additional errors should be reported for the `1 + foo` expression, even though `foo` could not be resolved with type `int`. To prevent an additional error from being reported, `foo` is given the `ErrorType` type, which is allowed as a `BinaryExpression` operand.

    This is convenient for debugging programs, although it was clarified afterwards on Piazza that the semantic checker is actually not required to avoid these duplicate errors.

* We decided to switch to antlr4 for scanning and parsing, rather than using antlr2 from the Java skeleton. This made it easier to build a correct AST, because antlr4 statically generates methods for the expected children of a nonterminal in the parse tree. However, this ended up being a lot of work (we had to figure out how to update the build to use antlr4, and we had to make modifications to the grammar).
* We used JUnit to write unit tests for our code.

## Difficulties

* ANTLR4 produces different error messages from ANTLR2 in some cases. As a result, we fail some of the provided scanner tests (we produce a different message than expected, even though we detect the same errors).

## Contribution

For large elements of the project, we generally met in person to discuss design strategy. Afterwards, one person would start working on an implementation. The other people would add additional tests and continue the implementation if the original implementer didn't complete it in one sitting.

We created issues on GitHub to track smaller tasks for the project (e.g. bugfixes). Generally, someone would assign themselves to the issue on GitHub when they started working on it, and then push a commit to close the issue when they finished.

