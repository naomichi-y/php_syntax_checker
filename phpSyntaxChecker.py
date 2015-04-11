import sublime, sublime_plugin
import os, re, subprocess

class phpSyntaxCheckerCommand(sublime_plugin.EventListener):
  # Command refers to $PATH environment variable
  EXECUTE_COMMAND = "php -l"

  # If want to add other extensions, please add array elements.
  # [".php", ".twig", ...]
  TARGET_SUFFIXES = [".php"]

  def on_post_save(self, view):
    path = view.file_name()
    root, extension = os.path.splitext(path)

    if extension in self.TARGET_SUFFIXES:
      command = self.EXECUTE_COMMAND + " \"" + path + "\""
      proc = subprocess.Popen([command],
        shell = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

      response = proc.communicate()

      if int(sublime.version()) > 3000:
        stdout = self.sanitize(str(response[0]))
        stderr = self.sanitize(str(response[1]))

      else:
        stdout = str(response[0])
        stderr = str(response[1])

      if len(stderr):
        sublime.error_message("Execute error:\n" + stderr)

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

  def sanitize(self, data):
    data = re.sub(r'^b[\'"]', '', data)
    data = re.sub(r'[\'"]$', '', data)
    data = re.sub(r'\\n', "\n", data)

    return data

