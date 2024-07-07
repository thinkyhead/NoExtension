#
# Sublime plugin to set the syntax of files without an extension to a specific syntax.
#
import os, sublime, sublime_plugin

default_syntax_file = 'Packages/Text/Plain text.tmLanguage'

def get_project_syntax(window):
    try:
        project_data = window.project_data()
        return project_data['settings']['default_syntax_file']
    except:
        return None

class SetNoExtensionSyntaxCommand(sublime_plugin.EventListener):
    def on_load(self, view):
        file_name = view.file_name()
        if file_name and not os.path.splitext(file_name)[1]:
            syntax = get_project_syntax(view.window())
            if syntax == None:
                settings = sublime.load_settings('Preferences.sublime-settings')
                syntax = settings.get('default_syntax_file', default_syntax_file)
            view.set_syntax_file(syntax)

            # Remove the Project root path from the file name, if it starts with it
            project_root = view.window().folders()[0]
            if file_name.startswith(project_root):
                file_name = file_name[len(project_root)+1:]

            print('Using syntax "{}" for "{}"'.format(syntax, file_name))

class SelectNoExtensionSyntaxCommand(sublime_plugin.WindowCommand):
    def syntax_basename(self, syntax_path):
        return os.path.basename(syntax_path).replace('.sublime-syntax', '').replace('.tmLanguage', '')

    def run(self):
        # Get a list of all available syntaxes in sublime
        syntaxes = sublime.find_resources("*.sublime-syntax") + sublime.find_resources("*.tmLanguage")

        # Get the basename of each syntax file
        syntax_names = [ self.syntax_basename(syntax) for syntax in syntaxes ]

        # Sort both the syntaxes and syntax_names according to the base names
        syntaxes, syntax_names = zip(*sorted(zip(syntaxes, syntax_names)))

        # Make available for the on_done method
        self.syntaxes = syntaxes

        # Show a quick panel with the list of syntaxes and set on_done as the callback
        self.window.show_quick_panel(syntax_names, self.on_done)

    def on_done(self, index):
        if index == -1: return
        selected_syntax = self.syntaxes[index]
        settings = sublime.load_settings('Preferences.sublime-settings')
        settings.set('default_syntax_file', selected_syntax)
        sublime.save_settings('Preferences.sublime-settings')
        message = 'Selected "{}" syntax for files with no extension.'.format(self.syntax_basename(selected_syntax))
        # Add a note to the message if a project setting is overriding this
        project_syntax = get_project_syntax(self.window)
        if project_syntax and selected_syntax != project_syntax:
            message += ' (Project setting overrides this)'
        sublime.message_dialog(message)
