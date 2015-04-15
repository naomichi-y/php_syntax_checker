import sublime, sublime_plugin
import re, sys, subprocess, shlex

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
      command = self.EXECUTE_COMMAND + " " + path
      shell = True

      if sublime.platform() == "windows":
        encoding = "sjis"
      else:
        encoding = "utf-8"

        if int(sublime.version()) >= 3000:
          shell = False

      if int(sublime.version()) >= 3000:
        params = shlex.split(command, False, False)
      else:
        params = [command]

      response = subprocess.Popen(
        params,
        shell=shell,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE).communicate()

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

