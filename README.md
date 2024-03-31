# legv8sim - A LEG-V8 Simulator and Additional Tools for Debugging/Editing 

## [The Simulator]
### This is the legv8 assembly simulator for ECE 331 at UMass Amherst.

### Minimum Requirements
Python 3 [the script installs the remaining requisite libraries] Do not use Homebrew to install Python3.
Rust and Cargo [Rust's package manager. Install via [rustlang website](https://www.rust-lang.org/tools/install)]

In order to install the simulator and use it, use the Source code option to download the directory needed to build the application on your computer. 
<img width="114" alt="image" src="https://github.com/anvitha305/legv8sim/assets/44482134/7d6ca2f8-e5df-4a88-a800-ee5c9b165f78">

Once you unzip the source and navigate to its inner folder, run the following command with your terminal:
`sh run.sh`

This will install the requirements for the simulator and run PyInstaller to create an executable.

Once the script is finished, you can run the application file in the dist folder within this inner folder [i.e. `app.exe` for Windows, `app.app` for MacOS], and this will let you run the application. 

<img width="722" alt="image" src="https://github.com/anvitha305/legv8sim/assets/44482134/021d4e15-0c08-43d2-a480-0b793afeb7ad">

You can open files with the Open File option, and select a file with .s or .legv8 with valid LEGV8 assembly to run it. You can step or reset, and all the text entry fields let you add values for memory or registers in the respective views. Errors show up in the errors section on the simulator and deeper errors with the program go in the logfile that is in the dist directory after the app runs. You must hit return to confirm your edits to any registers or memory.
Note that you need to enter arrays in manually for running code on arrays, with addressing done manually. A config file system is planned for next release.

### Error Reporting
You can open an Issue on GitHub here and add screenshots of the simulator and logfiles or contact me at aramachandra[at]umass[dot]edu with this information if there's a deeper error with your code running with the simulator.

Check the [legv8sim.tex](https://github.com/anvitha305/legv8sim/blob/master/legv8sim.tex) file as an overview of the system's goals.

### [Version 1.0 Sublime Highlighting](https://github.com/anvitha305/legv8sim/releases/tag/sublime)
Not really a version of the simulator, but rather Sublime editor's highlighting syntax defined so that I can use a particular parsing library that got put into a package. Future verison(s) will include support for more code editors to have LEG-V8 syntax highlighting.

<img width="491" alt="legv8 syntax highlighting in sublime" src="https://user-images.githubusercontent.com/44482134/213086258-32fa6c3a-bd7b-419b-a254-2064baf17c8c.png">
[demo of version 1.0's syntax highlighting]

## [Version 1.1 Vim Highlighting 🥰](https://github.com/anvitha305/legv8sim/releases/tag/vim)
Vim syntax highlighting, to make legv8sim editor-agnostic in terms of development so that you can edit the files on most of the common editors but you run it all on the same simulator. To view the source for this part of the project, go to the legv8-vim branch as they needed to be separated for reducing the bulk of the plugin.

<img width="500" alt="image" src="https://user-images.githubusercontent.com/44482134/221989709-90eac815-2d9b-4449-98f2-c82d98d3bc87.png">
[demo of version 1.1's syntax highlighting]

## [Version 1.2 VSCode Highlighting](https://github.com/anvitha305/legv8sim/releases/tag/vs-code)
VSCode syntax highlighting brings another editor that is supported with the syntax highlighting grammar designed in this project. To view the source for this part of the project, go to the legv8-vscode branch.
<img width="755" alt="image" src="https://user-images.githubusercontent.com/44482134/221992519-c1748e6d-5b3b-4a74-8752-bb2cf95d8b55.png">

[demo of version 1.2's syntax highlighting]

## [Version 1.3 Nano Highlighting](https://github.com/anvitha305/legv8sim/releases/tag/nano)
Nano now supported! To view source, go to the legv8-nano branch.
![image](https://github.com/anvitha305/legv8sim/assets/44482134/07fb5585-f5ac-45e3-8cf8-42c938e0b189)
[demo of version 1.3's syntax highlighting]

## Libraries Used
- [Iced](https://iced.rs/)
- [Syntect](https://github.com/trishume/syntect)
- [Nom](https://github.com/rust-bakery/nom)

## References
- Huge thank you to [@generic-github-user](https://github.com/generic-github-user) for design advice (this would be substantively more ugly without your genius)
- [LEG-V8 Green Card](https://www.usna.edu/Users/cs/lmcdowel/courses/ic220/S20/resources/ARM-v8-Quick-Reference-Guide.pdf)
- [Computer Organization and Design: The Hardware/Software Interface ARM Edition](https://g.co/kgs/8cbQrC) by D. Patterson and J. Hennessy, Morgan Kaufmann, 2016. ISBN: 978-012-8017333.
