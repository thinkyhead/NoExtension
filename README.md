# NoExtension

This Sublime Text plugin allows you to configure the syntax to use for files without an extension.

## Installation

Copy `NoExtension.sublime-plugin` into your Sublime Text `Packages` directory and enable with Package Control.

## Usage

- Whenever a file without any extension is opened the plugin automatically sets the syntax to your specified language.
- Use the command `NoExtension: Select Syntax` to set the syntax that will be used by default as a user preference.
- Override the user preference for a project by adding `default_syntax_file` to the project's settings array.
