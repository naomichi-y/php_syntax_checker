import sublime, sublime_plugin
import os, re, sys, subprocess

class phpSyntaxCheckerCommand(sublime_plugin.EventListener):
  # Command refers to $PATH environment variable
  EXECUTE_COMMAND = "php -l"

  def on_post_save(self, view):
    file_path = view.file_name()
    command_line = self.EXECUTE_COMMAND + " \"" + file_path + "\""
    syntax = view.settings().get("syntax")

    if syntax.find('PHP.tmLanguage') >= 0 or syntax.find('PHP.sublime-syntax') >= 0:
      response = subprocess.Popen(
        command_line,
        shell=True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE).communicate()

      encoding = sys.getfilesystemencoding()

      stdout = response[0].decode(encoding)
      stderr = response[1].decode(encoding)

      if len(stderr):
        sublime.error_message(stderr)

      else:
        rc = re.compile("Parse error.* on line (\d+)")
        match = rc.search(stdout)

        if match != None:
          sublime.error_message("PHP Syntax error:\n" + stdout)

          line = int(match.group(1)) - 1
          offset = view.text_point(line, 0)

          sel = view.sel()
          sel.clear()
          sel.add(sublime.Region(offset))

          view.show(offset)


