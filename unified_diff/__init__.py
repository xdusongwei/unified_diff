import re
import difflib


def process(text, unified_diff_text, restore_text=True):
    at_regex = r'^@@\D+(?P<s_begin_line>\d+),(?P<s_end_line>\d+)\D+(?P<t_begin_line>\d+),(?P<t_end_line>\d+)\D+$'
    lines = text.splitlines(True)
    diff_lines = unified_diff_text.splitlines(True)
    s_begin_line = None
    for d_line in diff_lines[2:]:
        if m := re.match(at_regex, d_line):
            groups = m.groups()
            s_begin_line, s_end_line, _, _ = groups
            s_begin_line = int(s_begin_line)
            s_end_line = int(s_end_line)
            for line_no in range(s_begin_line - 1, s_begin_line + s_end_line - 1):
                lines[line_no] = None
            lines[s_begin_line - 1] = list()
        if d_line.startswith(' '):
            lines[s_begin_line - 1].append(d_line[1:])
        if d_line.startswith('+'):
            if restore_text:
                continue
            else:
                lines[s_begin_line - 1].append(d_line[1:])
        if d_line.startswith('-'):
            if restore_text:
                lines[s_begin_line - 1].append(d_line[1:])
            else:
                continue
    new_lines = list()
    for line in lines:
        if isinstance(line, list):
            new_lines.extend(line)
        elif line is None:
            continue
        else:
            new_lines.append(line)
    return ''.join(new_lines)


def restore(a: str, unified_diff_text: str) -> str:
    return process(a, unified_diff_text, True)


def apply(b: str, unified_diff_text: str) -> str:
    return process(b, unified_diff_text, False)


def unified_diff(a: str, b: str, fromfile='', tofile='', fromfiledate='',
                 tofiledate='', n=3, lineterm='\n') -> str:
    if not a.endswith('\n') or not b.endswith('\n'):
        raise ValueError()
    a = a.splitlines(True)
    b = b.splitlines(True)
    unified_diff_text = ''.join(difflib.unified_diff(a, b, fromfile, tofile, fromfiledate, tofiledate, n, lineterm))
    return unified_diff_text


__all__ = ['restore', 'apply', 'unified_diff', ]
