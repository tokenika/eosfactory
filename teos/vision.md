# EOSFactory development

[Integrated development environments are designed to maximize programmer productivity by providing tight-knit components with similar user interfaces. IDEs present a single program in which all development is done.](#https://en.wikipedia.org/wiki/Integrated_development_environment#History)

Study existing IDEs to find most adequate features. **Temporary list of them**:

    * CMake interface:

        * compilation in-situ in order to find formal C++ errors;
        * building to WASM code;
        * cmake-assisted unit test:
            C++ Boost Unit Test Framework;
            Python unittest or doctest or any other, whichever most suitable;
        * cmake-assisted installation, here deployment to the local net.

    * Command-line:
        * creation of a skeleton template into the current directory:
            * standard folder structure;
            * cmake template included;
            * Visual Studio Code c_cpp_properties.json included (InteliSource configuration ready);
            * Visual Studio Code tasks.json included (VScode automatization);
        * all the cmake functionality (above) expressed in the form of c-l commands (Python).

    * Visual Studio Code extension providing GUI interface to the functionality listed above.

    * C++ helpers, for example:
        * logger;X
        * teos_lib library useful for Boost Unit Test Framework;X
        * smart-contract specific library with classes enveloping the low-level functionality available now.