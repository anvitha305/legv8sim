# legv8sim - A LEG-V8 Simulator and Additional Tools for Debugging/Editing 

## [Version 1.0 Sublime Highlighting](https://github.com/anvitha305/legv8sim/releases/tag/sublime)
Not really a version of the simulator, but rather Sublime editor's highlighting syntax defined so that I can use a particular parsing library that got put into a package. Future verison(s) will include support for more code editors to have LEG-V8 syntax highlighting.

<img width="491" alt="legv8 syntax highlighting in sublime" src="https://user-images.githubusercontent.com/44482134/213086258-32fa6c3a-bd7b-419b-a254-2064baf17c8c.png">
[demo of version 1.0's syntax highlighting]

## [Version 1.1 Vim Highlighting 🥰](https://github.com/anvitha305/legv8sim/releases/tag/vim)
Vim syntax highlighting, to make legv8sim editor-agnostic in terms of development so that you can edit the files on most of the common editors but you run it all on the same simulator. To view the source for this part of the project, go to the legv8-vim branch as they needed to be separated for reducing the bulk of the plugin.

<img width="422" alt="image" src="https://user-images.githubusercontent.com/44482134/217743095-3406f13f-a8fa-4476-81d9-377056e51b88.png">
[demo of version 1.1's syntax highlighting]

## Libraries Used
- [Iced](https://iced.rs/)
- [Syntect](https://github.com/trishume/syntect)
- [Nom](https://github.com/rust-bakery/nom)

## References
- Huge thank you to [@generic-github-user](https://github.com/generic-github-user) for design advice (this would be substantively more ugly without your genius)
- [LEG-V8 Green Card](https://montcs.bloomu.edu/Information/ARMv8/legv8-green-card.compressed.pdf)
- [Computer Organization and Design: The Hardware/Software Interface ARM Edition](https://g.co/kgs/8cbQrC) by D. Patterson and J. Hennessy, Morgan Kaufmann, 2016. ISBN: 978-012-8017333.