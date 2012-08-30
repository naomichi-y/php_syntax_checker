import sublime, sublime_plugin, os, commands, re

class PhpSyntaxChecker(sublime_plugin.EventListener):
  # Command refers to $PATH environment variable
  EXECUTE_COMMAND = "php -l"

  # If want to add other extensions, please add array elements.
  # [".php", ".twig", ...]
  TARGET_SUFFIXES = [".php"]

  def on_post_save(self, view):
    path = view.file_name()
    root, extension = os.path.splitext(path)

    if extension in self.TARGET_SUFFIXES:
      command = self.EXECUTE_COMMAND + " " + path
      response = commands.getoutput(command)

      r = re.compile("Parse error.* on line (\d+)")
      match = r.search(response)

      if match != None:
        line = int(match.group(1)) - 1

        offset = view.text_point(line, 0)
        view.sel().clear()
        view.sel().add(sublime.Region(offset))
        view.show(offset)

        sublime.error_message("PHP Syntax error\n" + response)
